import json

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cinema import CinemaRoom, Session
from app.repositories.cinema_room_repository import (get_all_cinema_rooms, get_cinema_room_by_id,
                                                     get_cinema_room_by_name, create_occupied_seat, update_seating,
                                                     get_session_by_id, get_session_by_room_and_film,
                                                     create_session)


def generate_seating(column: int, row: int) -> str:
    """
    Generates a seating matrix as a JSON string based on the given number of columns and rows.

    Args:
        column (int): The number of columns.
        row (int): The number of rows.

    Returns:
        str: A JSON string representing the seating arrangement.
    """
    return json.dumps([[False] * column for _ in range(row)])


@pytest.mark.asyncio
async def test_get_all_cinema_rooms(db_session: AsyncSession):
    # Create test data with seating initialized
    room1 = CinemaRoom(name="Room 1", column=10, row=10, seating=generate_seating(10, 10))
    room2 = CinemaRoom(name="Room 2", column=15, row=15, seating=generate_seating(15, 15))
    db_session.add_all([room1, room2])
    await db_session.commit()

    # Fetch all rooms
    rooms = await get_all_cinema_rooms(db_session)
    assert len(rooms) == 2
    assert rooms[0].name == "Room 1"
    assert rooms[1].name == "Room 2"


@pytest.mark.asyncio
async def test_get_cinema_room_by_id(db_session: AsyncSession):
    # Create a test room with seating initialized
    room = CinemaRoom(name="Test Room", column=5, row=5, seating=generate_seating(5, 5))
    db_session.add(room)
    await db_session.commit()

    # Fetch the room by ID
    fetched_room = await get_cinema_room_by_id(db_session, room.id)
    assert fetched_room is not None
    assert fetched_room.name == "Test Room"
    assert fetched_room.seating == generate_seating(5, 5)


@pytest.mark.asyncio
async def test_get_cinema_room_by_name(db_session: AsyncSession):
    # Create a test room with seating initialized
    room = CinemaRoom(name="Unique Room", column=8, row=8, seating=generate_seating(8, 8))
    db_session.add(room)
    await db_session.commit()

    # Fetch the room by name
    fetched_room = await get_cinema_room_by_name(db_session, "Unique Room")
    assert fetched_room is not None
    assert fetched_room.name == "Unique Room"
    assert fetched_room.seating == generate_seating(8, 8)


@pytest.mark.asyncio
async def test_create_session(db_session: AsyncSession):
    # Create test data with seating initialized
    room = CinemaRoom(name="Session Room", column=10, row=10, seating=generate_seating(10, 10))
    db_session.add(room)
    await db_session.commit()

    # Create a session
    session = await create_session(db_session, cinema_room_id=room.id, move_id=1, move_time_id=1)
    assert session is not None
    assert session.cinema_room_id == room.id


@pytest.mark.asyncio
async def test_create_occupied_seat(db_session: AsyncSession):
    # Create a cinema room with seating initialized
    room = CinemaRoom(name="Occupied Room", column=10, row=10, seating=generate_seating(10, 10))
    db_session.add(room)
    await db_session.commit()

    # Create a session linked to the created room
    session = Session(cinema_room_id=room.id, move_id=1, move_time_id=1)
    db_session.add(session)
    await db_session.commit()

    # Create an occupied seat
    occupied_seat = await create_occupied_seat(db_session, session, row=1, column=1)
    assert occupied_seat is not None
    assert occupied_seat.row == 1
    assert occupied_seat.column == 1

    # Test seat already occupied
    with pytest.raises(ValueError, match="This seat is already occupied."):
        await create_occupied_seat(db_session, session, row=1, column=1)



@pytest.mark.asyncio
async def test_update_seating():
    # Test seating update function
    initial_seating = "[[false, false], [false, false]]"
    updated_seating = await update_seating(initial_seating, row=1, column=1)
    assert updated_seating == "[[true, false], [false, false]]"


@pytest.mark.asyncio
async def test_get_session_by_room_and_film(db_session: AsyncSession):
    # Create a cinema room with seating initialized
    room = CinemaRoom(name="Session Test Room", column=10, row=10, seating=generate_seating(10, 10))
    db_session.add(room)
    await db_session.commit()

    # Create a session linked to the created room
    session = Session(cinema_room_id=room.id, move_id=1, move_time_id=1)
    db_session.add(session)
    await db_session.commit()

    # Fetch the session by room and film
    fetched_session = await get_session_by_room_and_film(db_session, cinema_room_id=room.id, move_id=1)
    assert fetched_session is not None
    assert fetched_session.cinema_room_id == room.id
    assert fetched_session.move_id == 1


@pytest.mark.asyncio
async def test_get_session_by_id(db_session: AsyncSession):
    # Create test data
    session = Session(cinema_room_id=1, move_id=1, move_time_id=1)
    db_session.add(session)
    await db_session.commit()

    # Fetch the session by ID
    fetched_session = await get_session_by_id(db_session, session.id)
    assert fetched_session is not None
    assert fetched_session.id == session.id
