"""create data

Revision ID: 252a1f18dfc3
Revises: 
Create Date: 2022-06-14 00:32:53.140145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '252a1f18dfc3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('daftarbaptis', sa.Column('no_kk', sa.String(length=50), nullable=True))
    op.add_column('daftarbaptis', sa.Column('alamat', sa.Text(), nullable=True))
    op.add_column('daftarbaptis', sa.Column('telepon', sa.String(length=15), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('daftarbaptis', 'telepon')
    op.drop_column('daftarbaptis', 'alamat')
    op.drop_column('daftarbaptis', 'no_kk')
    # ### end Alembic commands ###
