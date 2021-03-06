"""empty message

Revision ID: 190076dd4c3a
Revises: 9fe365d5bdcc
Create Date: 2019-10-31 12:46:46.320138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '190076dd4c3a'
down_revision = '9fe365d5bdcc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('description', sa.String(length=512), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('sale_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sale_id'], ['sale.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_description'), 'item', ['description'], unique=False)
    op.create_index(op.f('ix_item_name'), 'item', ['name'], unique=False)
    op.create_index(op.f('ix_item_price'), 'item', ['price'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_price'), table_name='item')
    op.drop_index(op.f('ix_item_name'), table_name='item')
    op.drop_index(op.f('ix_item_description'), table_name='item')
    op.drop_table('item')
    # ### end Alembic commands ###
