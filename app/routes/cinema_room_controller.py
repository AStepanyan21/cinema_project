from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.DTO.cinema_room import (
    CinemaRoomsNamesDTO, CinemaRoomsNamesByIdDTO, CinemaRoomResponseDTO,
    ReservationResponseDTO
)
from app.DTO.move import MoveDTO
from app.repositories.cinema_room_repository import (
    get_all_cinema_rooms, get_cinema_room_by_id, get_session_by_id, create_occupied_seat,
    get_session_by_room_and_film
)
from app.repositories.move_repository import (
    get_move_by_id, get_all_moves, get_moves_by_cinema_room
)
from app.utils.depends import get_db
from app.utils.helpers import process_cinema_room_and_film


class CinemaRoomController:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/cinema_rooms/", self.get_cinema_rooms, methods=["GET"],
                                  response_model=list[CinemaRoomsNamesDTO])
        self.router.add_api_route("/cinema_rooms/{room_id}", self.get_cinema_room_by_id, methods=["GET"],
                                  response_model=CinemaRoomsNamesByIdDTO)
        self.router.add_api_route("/movies/", self.get_all_movies, methods=["GET"],
                                  response_model=list[MoveDTO])
        self.router.add_api_route("/cinema_rooms/{room_id}/movies", self.get_movies_by_cinema_room, methods=["GET"],
                                  response_model=list[MoveDTO])
        self.router.add_api_route("/cinema_rooms/{room_id}/films/{film_id}", self.get_cinema_room_and_film,
                                  methods=["GET"],
                                  response_model=CinemaRoomResponseDTO)
        self.router.add_api_route("/cinema_rooms/{room_id}/reserve", self.create_seat_reservation, methods=["POST"],
                                  response_model=ReservationResponseDTO)

    async def get_cinema_rooms(self, db: AsyncSession = Depends(get_db)):
        return await get_all_cinema_rooms(db)

    async def get_cinema_room_by_id(self, room_id: int, db: AsyncSession = Depends(get_db)):
        room = await get_cinema_room_by_id(db, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Cinema room not found")
        return room

    async def get_all_movies(self, db: AsyncSession = Depends(get_db)):
        movies = await get_all_moves(db)
        return movies

    async def get_movies_by_cinema_room(self, room_id: int, db: AsyncSession = Depends(get_db)):
        """Get all movies for a specific cinema room."""
        room = await get_cinema_room_by_id(db, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Cinema room not found")
        movies = await get_moves_by_cinema_room(db, room.id)
        return movies

    async def get_cinema_room_and_film(self, room_id: int, film_id: int, db: AsyncSession = Depends(get_db)):
        """Get cinema room and film details along with reserved seats for a specific session."""
        room = await get_cinema_room_by_id(db, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Cinema room not found")

        film = await get_move_by_id(db, film_id)
        if not film:
            raise HTTPException(status_code=404, detail="Film not found")

        # Get the session by room and film IDs
        session = await get_session_by_room_and_film(db, room.id, film.id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found for the given room and film")

        # Use helper to process cinema room and film data
        response_data = process_cinema_room_and_film(room, session, film)

        return CinemaRoomResponseDTO(**response_data)

    async def create_seat_reservation(self, session_id: int, row: int, column: int, db: AsyncSession = Depends(get_db)):
        """Reserve a seat for a specific session."""
        # Fetch session by session_id
        session = await get_session_by_id(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Validate seating boundaries based on the cinema room associated with the session
        room = session.cinema_room
        if row > room.row or column > room.column:
            raise HTTPException(status_code=400, detail="Invalid row or column for reservation")

        try:
            # Create an occupied seat for the session
            occupied_seat = await create_occupied_seat(db, session, row, column)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return ReservationResponseDTO(
            message="Reservation created successfully",
            reservation={
                "row": occupied_seat.row,
                "column": occupied_seat.column
            }
        )
