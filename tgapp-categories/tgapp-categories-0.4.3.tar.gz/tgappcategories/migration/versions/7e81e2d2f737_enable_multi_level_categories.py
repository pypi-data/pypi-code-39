"""enable multi level categories"""

revision = '7e81e2d2f737'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('tgappcategories_categories', sa.Column('path', sa.Unicode(255), nullable=True, index=True))
    op.add_column('tgappcategories_categories', sa.Column('depth', sa.Integer))

def downgrade():
    op.drop_column('tgappcategories_categories', 'path')
    op.drop_column('tgappcategories_categories', 'depth')

