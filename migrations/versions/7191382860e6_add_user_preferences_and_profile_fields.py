"""Add user preferences and profile fields

Revision ID: 7191382860e6
Revises: 5764acceed04
Create Date: 2025-01-27 11:47:43.764701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7191382860e6'
down_revision = '5764acceed04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('notification_email', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('notification_in_app', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('dark_mode', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('dark_mode')
        batch_op.drop_column('notification_in_app')
        batch_op.drop_column('notification_email')
        batch_op.drop_column('profile_picture')

    # ### end Alembic commands ###
