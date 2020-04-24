"""empty message

Revision ID: 74342684fefe
Revises: beee24c1fa07
Create Date: 2020-04-23 19:04:19.013958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74342684fefe'
down_revision = 'beee24c1fa07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('periodic_task', sa.Column('date_changed', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('periodic_task', 'date_changed')
    # ### end Alembic commands ###
