"""Initial migration

Revision ID: 40649bf0ed6e
Revises: 
Create Date: 2022-09-04 13:44:51.656056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40649bf0ed6e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('category', 'questions', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('category', 'questions', 'categories', ['category'], ['id'], onupdate='CASCADE', ondelete='SET NULL')
    # ### end Alembic commands ###