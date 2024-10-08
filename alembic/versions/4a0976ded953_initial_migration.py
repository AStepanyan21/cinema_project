"""Initial migration

Revision ID: 4a0976ded953
Revises: 
Create Date: 2024-09-04 17:55:03.117900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a0976ded953'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cinema_rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('column', sa.Integer(), nullable=True),
    sa.Column('row', sa.Integer(), nullable=True),
    sa.Column('seating', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cinema_rooms_id'), 'cinema_rooms', ['id'], unique=False)
    op.create_table('move_times',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_move_times_id'), 'move_times', ['id'], unique=False)
    op.create_table('moves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('move_time_id', sa.Integer(), nullable=True),
    sa.Column('move_time_length', sa.Float(), nullable=False),
    sa.Column('movie_cover', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['move_time_id'], ['move_times.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_moves_id'), 'moves', ['id'], unique=False)
    op.create_table('cinema_room_move',
    sa.Column('cinema_room_id', sa.Integer(), nullable=True),
    sa.Column('move_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cinema_room_id'], ['cinema_rooms.id'], ),
    sa.ForeignKeyConstraint(['move_id'], ['moves.id'], )
    )
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cinema_room_id', sa.Integer(), nullable=False),
    sa.Column('move_id', sa.Integer(), nullable=False),
    sa.Column('move_time_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cinema_room_id'], ['cinema_rooms.id'], ),
    sa.ForeignKeyConstraint(['move_id'], ['moves.id'], ),
    sa.ForeignKeyConstraint(['move_time_id'], ['move_times.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sessions_id'), 'sessions', ['id'], unique=False)
    op.create_table('occupied_seats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('row', sa.Integer(), nullable=False),
    sa.Column('column', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_occupied_seats_id'), 'occupied_seats', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_occupied_seats_id'), table_name='occupied_seats')
    op.drop_table('occupied_seats')
    op.drop_index(op.f('ix_sessions_id'), table_name='sessions')
    op.drop_table('sessions')
    op.drop_table('cinema_room_move')
    op.drop_index(op.f('ix_moves_id'), table_name='moves')
    op.drop_table('moves')
    op.drop_index(op.f('ix_move_times_id'), table_name='move_times')
    op.drop_table('move_times')
    op.drop_index(op.f('ix_cinema_rooms_id'), table_name='cinema_rooms')
    op.drop_table('cinema_rooms')
    # ### end Alembic commands ###
