from sqlalchemy import Column, Integer, String, ForeignKey, Float, Time
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CinemaRoom(Base):
    __tablename__ = 'cinema_rooms'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    column = Column(Integer, default=10)
    row = Column(Integer, default=10)
    seating = Column(String)

    def __str__(self):
        return self.name


class MoveTime(Base):
    __tablename__ = 'move_times'
    id = Column(Integer, primary_key=True, index=True)
    time = Column(Time, nullable=False)

    def __str__(self):
        return str(self.time)


class Move(Base):
    __tablename__ = 'moves'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    move_time_length = Column(Float, nullable=False)
    movie_cover = Column(String)

    def __str__(self):
        return self.name


class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, index=True)
    cinema_room_id = Column(Integer, ForeignKey('cinema_rooms.id'), nullable=False)
    move_id = Column(Integer, ForeignKey('moves.id'), nullable=False)
    move_time_id = Column(Integer, ForeignKey('move_times.id'), nullable=False)

    cinema_room = relationship('CinemaRoom', backref='sessions')
    move = relationship('Move', backref='sessions')
    move_time = relationship('MoveTime', backref='sessions')

    def __str__(self):
        return f"{self.move.name} in {self.cinema_room.name} at {self.move_time.time}"


class OccupiedSeat(Base):
    __tablename__ = 'occupied_seats'
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    row = Column(Integer, nullable=False)
    column = Column(Integer, nullable=False)

    session = relationship('Session', backref=backref('occupied_seats', cascade='all, delete-orphan'))

    def __str__(self):
        return f"Seat at row {self.row}, column {self.column} for session {self.session_id}"


