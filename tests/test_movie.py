import pytest
from app.models.cinema import Move

# Test fetching all movies
@pytest.mark.asyncio
async def test_get_all_movies(test_app, db_session):
    """
    Test to fetch all movies.
    Creates a movie in the database, then retrieves all movies via the API.
    """
    # Create a movie directly in the database
    new_movie = Move(name="Movie 1", move_time_length=120, movie_cover="cover.png")
    db_session.add(new_movie)
    await db_session.commit()
    await db_session.refresh(new_movie)

    # Fetch all movies through the API
    response = test_app.get("/movies/")

    # Check that the response status is 200 OK
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Ensure the response is a list
    assert isinstance(response.json(), list), "Expected response to be a list"

    # Check that the created movie is present in the response
    movies = response.json()
    assert any(movie["name"] == "Movie 1" for movie in movies), \
        "Expected to find the movie 'Movie 1' in the response"
