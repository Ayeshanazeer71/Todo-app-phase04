#!/usr/bin/env python3
"""Reset database and alembic version for fresh start."""

import psycopg2
import os
from urllib.parse import urlparse

def reset_database():
    """Reset the database to a clean state."""
    
    # Parse the database URL
    db_url = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_6pnj0kDRsFgT@ep-sweet-grass-ah7vyrq5-pooler.c-3.us-east-1.aws.neon.tech/neondb')
    parsed = urlparse(db_url)
    
    print(f"Connecting to database: {parsed.hostname}")
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            sslmode='require'
        )
        
        cur = conn.cursor()
        
        # Check existing tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [t[0] for t in cur.fetchall()]
        print(f"Existing tables: {tables}")
        
        # Check if alembic_version exists
        if 'alembic_version' in tables:
            cur.execute('SELECT version_num FROM alembic_version')
            version = cur.fetchone()
            if version:
                print(f"Current alembic version: {version[0]}")
            
            # Clear alembic version
            cur.execute('DELETE FROM alembic_version')
            conn.commit()
            print("✅ Cleared alembic version table")
        
        # Drop Phase III tables if they exist (to start fresh)
        phase3_tables = ['message', 'conversation']
        for table in phase3_tables:
            if table in tables:
                cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE')
                print(f"✅ Dropped table: {table}")
        
        # Drop enum types
        cur.execute('DROP TYPE IF EXISTS messagerole CASCADE')
        print("✅ Dropped enum type: messagerole")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("✅ Database reset complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    reset_database()