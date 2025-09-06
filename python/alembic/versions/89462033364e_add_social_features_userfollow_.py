"""Add social features: UserFollow, Notification, Bookmark models

Revision ID: 89462033364e
Revises: 
Create Date: 2025-09-06 12:07:43.722571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '89462033364e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add social features tables."""
    
    # Create NotificationType enum
    notification_type_enum = postgresql.ENUM(
        'follow', 'post_like', 'post_comment', 'comment_reply', 
        'post_mention', 'comment_mention', 
        name='notificationtype'
    )
    notification_type_enum.create(op.get_bind(), checkfirst=True)
    
    # Create user_follows table
    op.create_table(
        'user_follows',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('follower_id', sa.Integer(), nullable=False),
        sa.Column('following_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['following_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('follower_id', 'following_id', name='unique_follow')
    )
    op.create_index(op.f('ix_user_follows_id'), 'user_follows', ['id'], unique=False)
    
    # Create notifications table  
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', notification_type_enum, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('related_user_id', sa.Integer(), nullable=True),
        sa.Column('related_post_id', sa.Integer(), nullable=True),
        sa.Column('related_comment_id', sa.Integer(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['related_comment_id'], ['comments.id'], ),
        sa.ForeignKeyConstraint(['related_post_id'], ['blog_posts.id'], ),
        sa.ForeignKeyConstraint(['related_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'], unique=False)
    
    # Create bookmarks table
    op.create_table(
        'bookmarks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['post_id'], ['blog_posts.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'post_id', name='unique_bookmark')
    )
    op.create_index(op.f('ix_bookmarks_id'), 'bookmarks', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema - Remove social features tables."""
    
    # Drop tables in reverse order
    op.drop_index(op.f('ix_bookmarks_id'), table_name='bookmarks')
    op.drop_table('bookmarks')
    
    op.drop_index(op.f('ix_notifications_id'), table_name='notifications')
    op.drop_table('notifications')
    
    op.drop_index(op.f('ix_user_follows_id'), table_name='user_follows')
    op.drop_table('user_follows')
    
    # Drop the enum type
    notification_type_enum = postgresql.ENUM(name='notificationtype')
    notification_type_enum.drop(op.get_bind(), checkfirst=True)
