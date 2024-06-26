"""post table

Revision ID: ee2b3865d2d0
Revises: 82684acb0ae6
Create Date: 2024-04-29 23:04:48.235651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee2b3865d2d0'
down_revision = '82684acb0ae6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_type', sa.String(length=8), nullable=False),
    sa.Column('item_name', sa.String(length=32), nullable=False),
    sa.Column('desc', sa.String(length=256), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_user_id'))
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))

    op.drop_table('post')
    # ### end Alembic commands ###
