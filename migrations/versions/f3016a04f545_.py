"""empty message

Revision ID: f3016a04f545
Revises: 5d39d4ca596a
Create Date: 2020-10-12 23:49:42.726296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3016a04f545'
down_revision = '5d39d4ca596a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clustering_result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Lat', sa.Float(), nullable=True),
    sa.Column('Lon', sa.Float(), nullable=True),
    sa.Column('Count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clustering_result_Count'), 'clustering_result', ['Count'], unique=False)
    op.create_index(op.f('ix_clustering_result_Lat'), 'clustering_result', ['Lat'], unique=False)
    op.create_index(op.f('ix_clustering_result_Lon'), 'clustering_result', ['Lon'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_clustering_result_Lon'), table_name='clustering_result')
    op.drop_index(op.f('ix_clustering_result_Lat'), table_name='clustering_result')
    op.drop_index(op.f('ix_clustering_result_Count'), table_name='clustering_result')
    op.drop_table('clustering_result')
    # ### end Alembic commands ###
