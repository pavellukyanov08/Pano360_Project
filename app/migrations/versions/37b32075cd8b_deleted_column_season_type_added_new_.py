"""Deleted column 'season_type'. Added new model 'Season' and the link between 'Project' and 'Season' tables

Revision ID: 37b32075cd8b
Revises: a61042be53b1
Create Date: 2024-09-06 11:31:30.446571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37b32075cd8b'
down_revision = 'a61042be53b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seasons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('season_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_project_season', 'seasons', ['season_id'], ['id'])
        batch_op.drop_column('season_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('season_type', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.drop_constraint('fk_project_season', type_='foreignkey')
        batch_op.drop_column('season_id')

    op.drop_table('seasons')
    # ### end Alembic commands ###
