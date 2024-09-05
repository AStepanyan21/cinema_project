from pydantic import BaseModel


class MoveDTO(BaseModel):
    id: int
    name: str
    movie_cover: str
