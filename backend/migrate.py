#!/usr/bin/env python3
"""Database migration script for Phase III chat functionality."""

import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from alembic.config import Config
from alembic import command

def run_migrations():
    """Run Alembic migrations to upgrade database to latest version."""
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    
    # Path to alembic.ini
    alembic_cfg_path = script_dir / "alembic.ini"
    
    if not alembic_cfg_path.exists():
        print(f"Error: alembic.ini not found at {alembic_cfg_path}")
        sys.exit(1)
    
    # Create Alembic configuration
    alembic_cfg = Config(str(alembic_cfg_path))
    
    try:
        print("Running database migrations...")
        command.upgrade(alembic_cfg, "head")
        print("✅ Database migrations completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()