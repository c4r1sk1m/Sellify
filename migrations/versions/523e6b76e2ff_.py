"""empty message

Revision ID: 523e6b76e2ff
Revises: 190076dd4c3a
Create Date: 2019-10-31 13:16:14.979240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '523e6b76e2ff'
down_revision = '190076dd4c3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
