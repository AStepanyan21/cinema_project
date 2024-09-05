import json

from app.DTO.cinema_room import CinemaRoomDTO
from app.DTO.move import MoveDTO
from app.models.cinema import Session, CinemaRoom


def process_cinema_room_and_film(room: CinemaRoom, session: Session, film) -> dict:
    """
    Processes cinema room and film data, including seating and occupied seats.

    Args:
        room (CinemaRoom): The cinema room object.
        session (Session): The session object that contains occupied seats information.
        film: The movie object associated with the session.

    Returns:
        dict: A dictionary containing the processed data for cinema room and film.
    """
    # Extract reserved seats from the session
    occupied_seats = [{"row": seat.row, "column": seat.column} for seat in session.occupied_seats]

    # Process seating matrix for the cinema room
    seating = json.loads(room.seating) if room.seating else []
    # Mark reserved seats in the seating matrix
    for seat in session.occupied_seats:
        seating[seat.row - 1][seat.column - 1] = True  # Mark the seat as reserved

    room_column = list(range(1, room.column + 1))
    room_row = list(range(1, room.row + 1))
    data = [{'row': r, 'seats': s} for r, s in zip(room_row, seating)]

    # Prepare the response data with DTOs
    return {
        "room": CinemaRoomDTO(
            name=room.name,
            columns=room_column,
            rows=room_row,
        ),
        "film": MoveDTO(
            id=film.id,
            name=film.name,
            movie_cover=film.movie_cover
        ),
        "data": data,
        "occupied_seats": occupied_seats,
        "session_id": session.id
    }
