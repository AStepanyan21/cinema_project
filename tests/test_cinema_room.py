import pytest
from app.models.cinema import CinemaRoom

# Test fetching all cinema rooms
@pytest.mark.asyncio
async def test_get_cinema_rooms(test_app):
    """
    Test to fetch all cinema rooms.
    Verifies that the endpoint returns a list of rooms.
    """
    response = test_app.get("/cinema_rooms/")

    # Check that the response status is 200 OK
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Check that the response is a list
    assert isinstance(response.json(), list), "Expected response to be a list"


@pytest.mark.asyncio
async def test_get_cinema_room_by_id(test_app, db_session):
    """
    Test to fetch a specific cinema room by its ID.
    Creates a room, retrieves it by ID, and checks the response.
    """
    # Create a new cinema room directly in the database
    new_room = CinemaRoom(name="Room 1", column=1, row=1, seating="[[false]]")
    db_session.add(new_room)
    await db_session.commit()
    await db_session.refresh(new_room)

    # Request the created room by its ID
    response = test_app.get(f"/cinema_rooms/{new_room.id}")

    # Check that the response status is 200 OK
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Verify the room's name in the response
    assert response.json()["name"] == "Room 1", f"Expected room name 'Room 1', got {response.json()['name']}"


# Test fetching a non-existent cinema room
@pytest.mark.asyncio
async def test_get_nonexistent_cinema_room(test_app):
    """
    Test to ensure a 404 error is returned when trying to fetch a non-existent cinema room.
    """
    # Attempt to fetch a cinema room with an ID that does not exist
    response = test_app.get("/cinema_rooms/999")

    # Check that the response status is 404 Not Found
    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"

    # Validate the error message in the response
    assert response.json()["detail"] == "Cinema room not found", \
        f"Expected error detail 'Cinema room not found', got '{response.json()['detail']}'"
