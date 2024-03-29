"""empty message

Revision ID: 489ea7ed0239
Revises: fa17c90bd2ab
Create Date: 2022-06-20 12:51:42.601623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '489ea7ed0239'
down_revision = 'fa17c90bd2ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'website_link',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=500),
               existing_nullable=True)
    op.alter_column('artist', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=500),
               existing_nullable=True)
    op.alter_column('venue', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=500),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'facebook_link',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)
    op.alter_column('artist', 'facebook_link',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)
    op.alter_column('artist', 'website_link',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)
    # ### end Alembic commands ###
