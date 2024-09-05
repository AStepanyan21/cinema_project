import json
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cinema import CinemaRoom, Session, OccupiedSeat


async def get_all_cinema_rooms(db: AsyncSession) -> List[CinemaRoom]:
    """
    Fetches all cinema rooms from the database.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[CinemaRoom]: A list of all cinema rooms.
    """
    result = await db.execute(select(CinemaRoom))
    return result.scalars().all()

async def get_cinema_room_by_id(db: AsyncSession, room_id: int) -> Optional[CinemaRoom]:
    """
    Fetches a cinema room by its ID.

    Args:
        db (AsyncSession): The database session.
        room_id (int): The ID of the cinema room.

    Returns:
        Optional[CinemaRoom]: The cinema room object if found, else None.
    """
    result = await db.execute(select(CinemaRoom).where(CinemaRoom.id == room_id))
    return result.scalar_one_or_none()

async def get_cinema_room_by_name(db: AsyncSession, name: str) -> Optional[CinemaRoom]:
    """
    Fetches a cinema room by its name.

    Args:
        db (AsyncSession): The database session.
        name (str): The name of the cinema room.

    Returns:
        Optional[CinemaRoom]: The cinema room object if found, else None.
    """
    result = await db.execute(select(CinemaRoom).where(CinemaRoom.name == name))
    return result.scalar_one_or_none()

async def get_all_sessions(db: AsyncSession) -> List[Session]:
    """
    Fetches all sessions from the database.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[Session]: A list of all sessions.
    """
    result = await db.execute(select(Session).options(select))
    return result.scalars().all()

async def get_session_by_id(db: AsyncSession, session_id: int) -> Optional[Session]:
    """
    Fetches a session by its ID.

    Args:
        db (AsyncSession): The database session.
        session_id (int): The ID of the session.

    Returns:
        Optional[Session]: The session object if found, else None.
    """
    result = await db.execute(select(Session).where(Session.id == session_id))
    return result.scalar_one_or_none()

async def create_session(db: AsyncSession, cinema_room_id: int, move_id: int, move_time_id: int) -> Session:
    """
    Creates a new session linking a cinema room, movie, and showtime.

    Args:
        db (AsyncSession): The database session.
        cinema_room_id (int): The ID of the cinema room.
        move_id (int): The ID of the movie.
        move_time_id (int): The ID of the showtime.

    Returns:
        Session: The created session object.
    """
    session = Session(cinema_room_id=cinema_room_id, move_id=move_id, move_time_id=move_time_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

async def create_occupied_seat(db: AsyncSession, session: Session, row: int, column: int) -> OccupiedSeat:
    """
    Creates a record for an occupied seat within a session.

    Args:
        db (AsyncSession): The database session.
        session (Session): The session object.
        row (int): The row number of the seat.
        column (int): The column number of the seat.

    Raises:
        ValueError: If the seat is already occupied.

    Returns:
        OccupiedSeat: The created occupied seat object.
    """
    # Check if the seat is already occupied
    occupied_seat = await db.execute(select(OccupiedSeat).where(
        OccupiedSeat.session_id == session.id,
        OccupiedSeat.row == row,
        OccupiedSeat.column == column
    ))
    if occupied_seat.scalar_one_or_none():
        raise ValueError("This seat is already occupied.")

    new_occupied_seat = OccupiedSeat(session=session, row=row, column=column)
    db.add(new_occupied_seat)
    await db.commit()
    await db.refresh(new_occupied_seat)
    return new_occupied_seat

async def update_seating(seating: str, row: int, column: int) -> str:
    """
    Updates the seating matrix to mark a seat as reserved.

    Args:
        seating (str): The seating matrix in JSON format.
        row (int): The row number of the seat.
        column (int): The column number of the seat.

    Returns:
        str: The updated seating matrix in JSON format.
    """
    seating = json.loads(seating)
    seating[row - 1][column - 1] = True
    seating = json.dumps(seating)
    return seating

async def get_session_by_room_and_film(db: AsyncSession, cinema_room_id: int, move_id: int) -> Optional[Session]:
    """
    Fetches a session by room and film ID with preloaded occupied seats.

    Args:
        db (AsyncSession): The database session.
        cinema_room_id (int): The ID of the cinema room.
        move_id (int): The ID of the movie.

    Returns:
        Optional[Session]: The session object if found, else None.
    """
    result = await db.execute(
        select(Session)
        .options(selectinload(Session.occupied_seats))
        .where(Session.cinema_room_id == cinema_room_id)
        .where(Session.move_id == move_id)
    )
    return result.scalar_one_or_none()

async def get_session_by_id(db: AsyncSession, session_id: int) -> Optional[Session]:
    """
    Fetches a session by its ID with preloaded related cinema room.

    Args:
        db (AsyncSession): The database session.
        session_id (int): The ID of the session.

    Returns:
        Optional[Session]: The session object with preloaded cinema room if found, else None.
    """
    result = await db.execute(
        select(Session)
        .options(selectinload(Session.cinema_room))
        .where(Session.id == session_id)
    )
    return result.scalar_one_or_none()
