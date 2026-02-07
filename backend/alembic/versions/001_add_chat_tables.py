"""Add chat tables for conversations and messages

Revision ID: 001
Revises: 
Create Date: 2024-01-24 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversations table
    op.create_table('conversation',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for conversations table
    op.create_index('ix_conversation_id', 'conversation', ['id'], unique=False)
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'], unique=False)
    op.create_index('ix_conversation_updated_at', 'conversation', ['updated_at'], unique=False)
    
    # Create messages table
    op.create_table('message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', name='messagerole'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for messages table
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'], unique=False)
    op.create_index('ix_message_created_at', 'message', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop indexes first
    op.drop_index('ix_message_created_at', table_name='message')
    op.drop_index('ix_message_conversation_id', table_name='message')
    
    # Drop messages table
    op.drop_table('message')
    
    # Drop conversation indexes
    op.drop_index('ix_conversation_updated_at', table_name='conversation')
    op.drop_index('ix_conversation_user_id', table_name='conversation')
    op.drop_index('ix_conversation_id', table_name='conversation')
    
    # Drop conversations table
    op.drop_table('conversation')
    
    # Drop the enum type
    op.execute('DROP TYPE IF EXISTS messagerole')