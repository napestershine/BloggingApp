"""Add moderation fields to posts and comments

Revision ID: 472c34150ac4
Revises: cbcef27823ba
Create Date: 2025-09-06 10:45:40.126438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '472c34150ac4'
down_revision: Union[str, Sequence[str], None] = 'cbcef27823ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    post_status_enum = postgresql.ENUM(
        'DRAFT', 'PENDING', 'PUBLISHED', 'REJECTED', 'SCHEDULED',
        name='poststatus'
    )
    comment_status_enum = postgresql.ENUM(
        'PENDING', 'APPROVED', 'REJECTED', 'SPAM',
        name='commentstatus'
    )

    post_status_enum.create(op.get_bind(), checkfirst=True)
    comment_status_enum.create(op.get_bind(), checkfirst=True)

    # Use temporary server defaults so the migration can succeed on populated tables.
    op.add_column(
        'blog_posts',
        sa.Column(
            'status',
            post_status_enum,
            nullable=False,
            server_default='PUBLISHED',
        ),
    )
    op.add_column('blog_posts', sa.Column('moderated_by', sa.Integer(), nullable=True))
    op.add_column('blog_posts', sa.Column('moderated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('blog_posts', sa.Column('rejection_reason', sa.Text(), nullable=True))
    op.add_column('blog_posts', sa.Column('featured', sa.Boolean(), nullable=True))
    op.add_column('blog_posts', sa.Column('scheduled_publish', sa.DateTime(timezone=True), nullable=True))
    op.add_column('blog_posts', sa.Column('views', sa.Integer(), nullable=True))
    op.add_column('blog_posts', sa.Column('tags', sa.Text(), nullable=True))
    op.add_column('blog_posts', sa.Column('meta_description', sa.Text(), nullable=True))
    op.create_foreign_key(None, 'blog_posts', 'users', ['moderated_by'], ['id'])
    op.add_column(
        'comments',
        sa.Column(
            'status',
            comment_status_enum,
            nullable=False,
            server_default='APPROVED',
        ),
    )
    op.add_column('comments', sa.Column('moderated_by', sa.Integer(), nullable=True))
    op.add_column('comments', sa.Column('moderated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('comments', sa.Column('is_spam', sa.Boolean(), nullable=True))
    op.create_foreign_key(None, 'comments', 'users', ['moderated_by'], ['id'])
    op.alter_column('blog_posts', 'status', server_default=None)
    op.alter_column('comments', 'status', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    post_status_enum = postgresql.ENUM(name='poststatus')
    comment_status_enum = postgresql.ENUM(name='commentstatus')

    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'is_spam')
    op.drop_column('comments', 'moderated_at')
    op.drop_column('comments', 'moderated_by')
    op.drop_column('comments', 'status')
    op.drop_constraint(None, 'blog_posts', type_='foreignkey')
    op.drop_column('blog_posts', 'meta_description')
    op.drop_column('blog_posts', 'tags')
    op.drop_column('blog_posts', 'views')
    op.drop_column('blog_posts', 'scheduled_publish')
    op.drop_column('blog_posts', 'featured')
    op.drop_column('blog_posts', 'rejection_reason')
    op.drop_column('blog_posts', 'moderated_at')
    op.drop_column('blog_posts', 'moderated_by')
    op.drop_column('blog_posts', 'status')
    comment_status_enum.drop(op.get_bind(), checkfirst=True)
    post_status_enum.drop(op.get_bind(), checkfirst=True)
