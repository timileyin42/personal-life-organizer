"""Add tasks with goal relationship

Revision ID: 55beea6ae111
Revises: f241e5a4bc25
Create Date: 2025-01-22 09:23:36.263610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55beea6ae111'
down_revision = 'f241e5a4bc25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('goal_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'goal', ['goal_id'], ['id'])
        batch_op.drop_column('completed')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('goal_id')
        batch_op.drop_column('status')
        batch_op.drop_column('description')

    # ### end Alembic commands ###
