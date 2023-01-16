"""empty message

Revision ID: f21bd34e9616
Revises: d86aa89d65dc
Create Date: 2023-01-16 16:26:46.219039

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f21bd34e9616'
down_revision = 'd86aa89d65dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ownerSource', sa.String(), nullable=True),
    sa.Column('ownerId', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('symbol', sa.String(), nullable=True),
    sa.Column('resolution', sa.String(), nullable=True),
    sa.Column('lastModified', sa.DateTime(timezone=True), nullable=True),
    sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chart_id'), 'chart', ['id'], unique=False)
    op.create_index(op.f('ix_chart_ownerId'), 'chart', ['ownerId'], unique=False)
    op.create_index(op.f('ix_chart_ownerSource'), 'chart', ['ownerSource'], unique=False)
    op.create_table('drawingtemplate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ownerSource', sa.String(), nullable=True),
    sa.Column('ownerId', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('tool', sa.String(), nullable=True),
    sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_drawingtemplate_id'), 'drawingtemplate', ['id'], unique=False)
    op.create_index(op.f('ix_drawingtemplate_ownerId'), 'drawingtemplate', ['ownerId'], unique=False)
    op.create_index(op.f('ix_drawingtemplate_ownerSource'), 'drawingtemplate', ['ownerSource'], unique=False)
    op.create_table('studytemplate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ownerSource', sa.String(), nullable=True),
    sa.Column('ownerId', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_studytemplate_id'), 'studytemplate', ['id'], unique=False)
    op.create_index(op.f('ix_studytemplate_ownerId'), 'studytemplate', ['ownerId'], unique=False)
    op.create_index(op.f('ix_studytemplate_ownerSource'), 'studytemplate', ['ownerSource'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_studytemplate_ownerSource'), table_name='studytemplate')
    op.drop_index(op.f('ix_studytemplate_ownerId'), table_name='studytemplate')
    op.drop_index(op.f('ix_studytemplate_id'), table_name='studytemplate')
    op.drop_table('studytemplate')
    op.drop_index(op.f('ix_drawingtemplate_ownerSource'), table_name='drawingtemplate')
    op.drop_index(op.f('ix_drawingtemplate_ownerId'), table_name='drawingtemplate')
    op.drop_index(op.f('ix_drawingtemplate_id'), table_name='drawingtemplate')
    op.drop_table('drawingtemplate')
    op.drop_index(op.f('ix_chart_ownerSource'), table_name='chart')
    op.drop_index(op.f('ix_chart_ownerId'), table_name='chart')
    op.drop_index(op.f('ix_chart_id'), table_name='chart')
    op.drop_table('chart')
    # ### end Alembic commands ###