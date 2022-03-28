"""create codes table

Revision ID: 04232aa97761
Revises: 
Create Date: 2022-03-22 05:06:00.199927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04232aa97761'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'codes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('added_at', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('user_id', sa.String, nullable=False),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('first_name', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('code_type', sa.String, nullable=False),
        sa.Column('code', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('codes')
