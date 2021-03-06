"""empty message

Revision ID: cd29c0ee1eda
Revises: a2876a0d1cdb
Create Date: 2020-11-07 22:14:43.197819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd29c0ee1eda'
down_revision = 'a2876a0d1cdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clustering_result_180',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Lat', sa.Float(), nullable=True),
    sa.Column('Lon', sa.Float(), nullable=True),
    sa.Column('Count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clustering_result_180_Count'), 'clustering_result_180', ['Count'], unique=False)
    op.create_index(op.f('ix_clustering_result_180_Lat'), 'clustering_result_180', ['Lat'], unique=False)
    op.create_index(op.f('ix_clustering_result_180_Lon'), 'clustering_result_180', ['Lon'], unique=False)
    op.create_table('clustering_result_40',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Lat', sa.Float(), nullable=True),
    sa.Column('Lon', sa.Float(), nullable=True),
    sa.Column('Count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clustering_result_40_Count'), 'clustering_result_40', ['Count'], unique=False)
    op.create_index(op.f('ix_clustering_result_40_Lat'), 'clustering_result_40', ['Lat'], unique=False)
    op.create_index(op.f('ix_clustering_result_40_Lon'), 'clustering_result_40', ['Lon'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_clustering_result_40_Lon'), table_name='clustering_result_40')
    op.drop_index(op.f('ix_clustering_result_40_Lat'), table_name='clustering_result_40')
    op.drop_index(op.f('ix_clustering_result_40_Count'), table_name='clustering_result_40')
    op.drop_table('clustering_result_40')
    op.drop_index(op.f('ix_clustering_result_180_Lon'), table_name='clustering_result_180')
    op.drop_index(op.f('ix_clustering_result_180_Lat'), table_name='clustering_result_180')
    op.drop_index(op.f('ix_clustering_result_180_Count'), table_name='clustering_result_180')
    op.drop_table('clustering_result_180')
    # ### end Alembic commands ###
