"""empty message

Revision ID: 57713483ed75
Revises: 40649bf0ed6e
Create Date: 2022-09-04 13:46:07.127884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57713483ed75'
down_revision = '40649bf0ed6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'category',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'questions', 'categories', ['category'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'questions', type_='foreignkey')
    op.alter_column('questions', 'category',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
