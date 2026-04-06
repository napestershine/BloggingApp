"""Harden notifications and follows: add indexes, constraints, and cascading deletes

Revision ID: 4f6e6df5c9af
Revises: 89462033364e
Create Date: 2025-02-28 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f6e6df5c9af'
down_revision: Union[str, Sequence[str], None] = '89462033364e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add indexes and constraints for notifications and follows."""

    # Drop and recreate user_follows table foreign keys with ON DELETE CASCADE.
    op.drop_constraint('user_follows_follower_id_fkey', 'user_follows', type_='foreignkey')
    op.drop_constraint('user_follows_following_id_fkey', 'user_follows', type_='foreignkey')

    op.create_foreign_key(
        'user_follows_follower_id_fkey',
        'user_follows',
        'users',
        ['follower_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'user_follows_following_id_fkey',
        'user_follows',
        'users',
        ['following_id'],
        ['id'],
        ondelete='CASCADE'
    )

    op.create_index(
        'ix_user_follows_follower_following',
        'user_follows',
        ['follower_id', 'following_id'],
        unique=False
    )

    # Drop and recreate notifications table foreign keys with ON DELETE CASCADE.
    op.drop_constraint('notifications_user_id_fkey', 'notifications', type_='foreignkey')
    op.drop_constraint('notifications_related_user_id_fkey', 'notifications', type_='foreignkey')
    op.drop_constraint('notifications_related_post_id_fkey', 'notifications', type_='foreignkey')
    op.drop_constraint('notifications_related_comment_id_fkey', 'notifications', type_='foreignkey')

    op.create_foreign_key(
        'notifications_user_id_fkey',
        'notifications',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'notifications_related_user_id_fkey',
        'notifications',
        'users',
        ['related_user_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'notifications_related_post_id_fkey',
        'notifications',
        'blog_posts',
        ['related_post_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'notifications_related_comment_id_fkey',
        'notifications',
        'comments',
        ['related_comment_id'],
        ['id'],
        ondelete='CASCADE'
    )

    op.create_index(
        'ix_notifications_user_created',
        'notifications',
        [sa.text('user_id'), sa.desc('created_at')],
        unique=False
    )

    op.create_index(
        'ix_notifications_user_unread',
        'notifications',
        ['user_id'],
        unique=False,
        postgresql_where=sa.text('is_read = false')
    )

    # Update bookmarks table foreign keys and add a composite lookup index.
    op.drop_constraint('bookmarks_user_id_fkey', 'bookmarks', type_='foreignkey')
    op.drop_constraint('bookmarks_post_id_fkey', 'bookmarks', type_='foreignkey')

    op.create_foreign_key(
        'bookmarks_user_id_fkey',
        'bookmarks',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'bookmarks_post_id_fkey',
        'bookmarks',
        'blog_posts',
        ['post_id'],
        ['id'],
        ondelete='CASCADE'
    )

    op.create_index(
        'ix_bookmarks_user_post',
        'bookmarks',
        ['user_id', 'post_id'],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema - Remove indexes and restore original foreign keys."""

    op.drop_index('ix_bookmarks_user_post', table_name='bookmarks')
    op.drop_index('ix_notifications_user_unread', table_name='notifications')
    op.drop_index('ix_notifications_user_created', table_name='notifications')
    op.drop_index('ix_user_follows_follower_following', table_name='user_follows')

    op.drop_constraint('bookmarks_post_id_fkey', 'bookmarks', type_='foreignkey')
    op.drop_constraint('bookmarks_user_id_fkey', 'bookmarks', type_='foreignkey')

    op.create_foreign_key(
        'bookmarks_user_id_fkey',
        'bookmarks',
        'users',
        ['user_id'],
        ['id']
    )
    op.create_foreign_key(
        'bookmarks_post_id_fkey',
        'bookmarks',
        'blog_posts',
        ['post_id'],
        ['id']
    )

    op.drop_constraint('notifications_related_comment_id_fkey', 'notifications', type_='foreignkey')
    op.drop_constraint('notifications_related_post_id_fkey', 'notifications', type_='foreignkey')
    op.drop_constraint('notifications_related_user_id_fkey', 'notifications', type_='foreignkey')
    op.drop_constraint('notifications_user_id_fkey', 'notifications', type_='foreignkey')

    op.create_foreign_key(
        'notifications_user_id_fkey',
        'notifications',
        'users',
        ['user_id'],
        ['id']
    )
    op.create_foreign_key(
        'notifications_related_user_id_fkey',
        'notifications',
        'users',
        ['related_user_id'],
        ['id']
    )
    op.create_foreign_key(
        'notifications_related_post_id_fkey',
        'notifications',
        'blog_posts',
        ['related_post_id'],
        ['id']
    )
    op.create_foreign_key(
        'notifications_related_comment_id_fkey',
        'notifications',
        'comments',
        ['related_comment_id'],
        ['id']
    )

    op.drop_constraint('user_follows_following_id_fkey', 'user_follows', type_='foreignkey')
    op.drop_constraint('user_follows_follower_id_fkey', 'user_follows', type_='foreignkey')

    op.create_foreign_key(
        'user_follows_follower_id_fkey',
        'user_follows',
        'users',
        ['follower_id'],
        ['id']
    )
    op.create_foreign_key(
        'user_follows_following_id_fkey',
        'user_follows',
        'users',
        ['following_id'],
        ['id']
    )
