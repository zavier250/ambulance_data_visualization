"""empty message

Revision ID: 449202edffb8
Revises: eb91838dfff4
Create Date: 2020-09-11 18:21:24.449172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '449202edffb8'
down_revision = 'eb91838dfff4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ampds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('EARF_Number', sa.Integer(), nullable=False),
    sa.Column('AMPDS_Code', sa.String(length=100), nullable=True),
    sa.Column('Protocol', sa.Integer(), nullable=False),
    sa.Column('Priority', sa.String(length=100), nullable=True),
    sa.Column('Sub_Category', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ampds_AMPDS_Code'), 'ampds', ['AMPDS_Code'], unique=False)
    op.create_index(op.f('ix_ampds_EARF_Number'), 'ampds', ['EARF_Number'], unique=False)
    op.create_index(op.f('ix_ampds_Priority'), 'ampds', ['Priority'], unique=False)
    op.create_index(op.f('ix_ampds_Protocol'), 'ampds', ['Protocol'], unique=False)
    op.create_index(op.f('ix_ampds_Sub_Category'), 'ampds', ['Sub_Category'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ampds_Sub_Category'), table_name='ampds')
    op.drop_index(op.f('ix_ampds_Protocol'), table_name='ampds')
    op.drop_index(op.f('ix_ampds_Priority'), table_name='ampds')
    op.drop_index(op.f('ix_ampds_EARF_Number'), table_name='ampds')
    op.drop_index(op.f('ix_ampds_AMPDS_Code'), table_name='ampds')
    op.drop_table('ampds')
    # ### end Alembic commands ###
