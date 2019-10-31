"""sales table

Revision ID: 9fe365d5bdcc
Revises: c3b39bb63f12
Create Date: 2019-10-31 11:44:15.470215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fe365d5bdcc'
down_revision = 'c3b39bb63f12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sale',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('description', sa.String(length=512), nullable=True),
    sa.Column('post_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sale_name'), 'sale', ['name'], unique=False)
    op.create_index(op.f('ix_sale_post_date'), 'sale', ['post_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sale_post_date'), table_name='sale')
    op.drop_index(op.f('ix_sale_name'), table_name='sale')
    op.drop_table('sale')
    # ### end Alembic commands ###