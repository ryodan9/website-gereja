"""create data

Revision ID: b199c3fde42e
Revises: 
Create Date: 2022-06-12 17:56:08.631414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b199c3fde42e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profil', sa.Column('kartukeluarga_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'profil', 'kartukeluarga', ['kartukeluarga_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profil', type_='foreignkey')
    op.drop_column('profil', 'kartukeluarga_id')
    # ### end Alembic commands ###
