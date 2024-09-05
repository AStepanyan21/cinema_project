from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cinema import Move, CinemaRoom


async def get_all_moves(db: AsyncSession) -> List[Move]:
    """
    Fetches all movies from the database.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[Move]: A list of all movies.
    """
    result = await db.execute(select(Move))
    return result.scalars().all()

async def get_move_by_id(db: AsyncSession, move_id: int) -> Move:
    """
    Fetches a movie by its ID.

    Args:
        db (AsyncSession): The database session.
        move_id (int): The ID of the movie.

    Returns:
        Move: The movie object if found, else None.
    """
    result = await db.execute(select(Move).where(Move.id == move_id))
    return result.scalar_one_or_none()

async def get_moves_by_cinema_room(db: AsyncSession, room_id: int) -> List[Move]:
    """
    Fetches all movies associated with a specific cinema room.

    Args:
        db (AsyncSession): The database session.
        room_id (int): The ID of the cinema room.

    Returns:
        List[Move]: A list of movies associated with the specified cinema room.
    """
    # Select movies that are associated with the given cinema room ID
    result = await db.execute(
        select(Move)
        .where(CinemaRoom.id == room_id)
    )
    return result.scalars().all()
