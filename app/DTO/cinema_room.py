from typing import List

from pydantic import BaseModel

from app.DTO.move import MoveDTO


class CinemaRoomsNamesDTO(BaseModel):
    id: int
    name: str


class CinemaRoomsNamesByIdDTO(CinemaRoomsNamesDTO):
    seating: str


class CinemaRoomDTO(BaseModel):
    name: str

class CinemaRoomResponseDTO(BaseModel):
    room: CinemaRoomDTO
    film: MoveDTO
    data: List[dict]
    session_id: int

class ReservationResponseDTO(BaseModel):
    message: str
    reservation: dict