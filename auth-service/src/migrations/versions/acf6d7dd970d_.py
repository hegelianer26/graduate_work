"""empty message

Revision ID: acf6d7dd970d
Revises: 6bc68f6c9544
Create Date: 2024-02-14 00:46:05.310283

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'acf6d7dd970d'
down_revision: Union[str, None] = '6bc68f6c9544'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_unique_constraint(None, 'refresh_token', ['uuid'])
    op.create_foreign_key(None, 'refresh_token', 'users', ['user_id'], ['uuid'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'roles', ['uuid'])
    op.create_unique_constraint(None, 'user_roles', ['uuid'])
    op.create_foreign_key(None, 'user_roles', 'users', ['user_id'], ['uuid'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'users_sign_in', ['uuid'])
    op.create_foreign_key(None, 'users_sign_in', 'users', ['user_id'], ['uuid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_sign_in', type_='foreignkey')
    op.drop_constraint(None, 'users_sign_in', type_='unique')
    op.drop_constraint(None, 'user_roles', type_='foreignkey')
    op.drop_constraint(None, 'user_roles', type_='unique')
    op.drop_constraint(None, 'roles', type_='unique')
    op.drop_constraint(None, 'refresh_token', type_='foreignkey')
    op.drop_constraint(None, 'refresh_token', type_='unique')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
