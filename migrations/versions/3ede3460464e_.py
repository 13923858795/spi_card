"""empty message

Revision ID: 3ede3460464e
Revises: 
Create Date: 2020-07-22 16:44:42.356573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ede3460464e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=500), nullable=True),
    sa.Column('date', sa.Text(), nullable=True),
    sa.Column('intent', sa.Text(), nullable=True),
    sa.Column('company_url', sa.Text(), nullable=True),
    sa.Column('is_ok', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('crm_employee_id', sa.String(length=80), nullable=True),
    sa.Column('nickname', sa.String(length=80), nullable=True),
    sa.Column('english_name', sa.String(length=200), nullable=True),
    sa.Column('abbreviation_name', sa.String(length=200), nullable=True),
    sa.Column('office', sa.String(length=80), nullable=True),
    sa.Column('superior_account', sa.String(length=200), nullable=True),
    sa.Column('position_type', sa.String(length=200), nullable=True),
    sa.Column('portrait_image', sa.String(length=200), nullable=True),
    sa.Column('password', sa.Binary(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('roles', sa.Integer(), nullable=True),
    sa.Column('is_leave', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('crm_employee_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    op.drop_table('users')
    op.drop_table('cards')
    # ### end Alembic commands ###
