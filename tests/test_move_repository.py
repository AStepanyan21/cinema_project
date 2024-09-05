import json

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cinema import Move, CinemaRoom
from app.repositories.cinema_room_repository import create_session
from app.repositories.move_repository import get_all_moves, get_move_by_id, get_moves_by_cinema_room


@pytest.mark.asyncio
async def test_get_all_moves(db_session: AsyncSession):
    """
    Test fetching all movies from the database.
    Verifies that all movies are returned correctly.
    """
    # Create and add multiple movie records to the database
    movie1 = Move(name="Movie 1", move_time_length=120, movie_cover="cover1.png")
    movie2 = Move(name="Movie 2", move_time_length=150, movie_cover="cover2.png")
    db_session.add_all([movie1, movie2])
    await db_session.commit()

    # Fetch all movies using the repository function
    movies = await get_all_moves(db_session)

    # Verify that the correct number of movies is fetched
    assert len(movies) == 2
    assert movies[0].name == "Movie 1"
    assert movies[1].name == "Movie 2"


@pytest.mark.asyncio
async def test_get_move_by_id(db_session: AsyncSession):
    """
    Test fetching a movie by its ID.
    Verifies that the correct movie is returned when queried by ID.
    """
    # Create and add a movie record to the database
    movie = Move(name="Test Movie", move_time_length=100, movie_cover="cover.png")
    db_session.add(movie)
    await db_session.commit()
    await db_session.refresh(movie)

    # Fetch the movie by ID using the repository function
    fetched_movie = await get_move_by_id(db_session, movie.id)

    # Verify that the fetched movie matches the created movie
    assert fetched_movie is not None
    assert fetched_movie.id == movie.id
    assert fetched_movie.name == "Test Movie"


@pytest.mark.asyncio
async def test_get_moves_by_cinema_room(db_session: AsyncSession):
    """
    Test fetching movies associated with a specific cinema room.
    Verifies that movies linked to the specified cinema room are returned.
    """
    # Create a cinema room
    room = CinemaRoom(name="Room 1", column=10, row=10, seating=json.dumps([[False] * 10 for _ in range(10)]))
    db_session.add(room)
    await db_session.commit()
    await db_session.refresh(room)

    # Create and add movie records to the database
    movie1 = Move(name="Movie 1", move_time_length=120, movie_cover="cover1.png")
    movie2 = Move(name="Movie 2", move_time_length=150, movie_cover="cover2.png")
    db_session.add_all([movie1, movie2])
    await db_session.commit()

    # Associate the movies with the cinema room using session creation
    session1 = await create_session(db_session, cinema_room_id=room.id, move_id=movie1.id, move_time_id=1)
    session2 = await create_session(db_session, cinema_room_id=room.id, move_id=movie2.id, move_time_id=2)

    # Fetch movies associated with the cinema room
    movies = await get_moves_by_cinema_room(db_session, room_id=room.id)

    # Verify that the correct movies are fetched
    assert len(movies) == 2
    assert movies[0].name == "Movie 1"
    assert movies[1].name == "Movie 2"
