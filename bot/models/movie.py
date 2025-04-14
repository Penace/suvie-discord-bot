from sqlalchemy import Column, Integer, String, Text
from bot.utils.database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, index=True)
    title = Column(String, index=True)
    year = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    plot = Column(Text, nullable=True)
    poster = Column(String, nullable=True)
    imdb_url = Column(String, nullable=True)
    imdb_id = Column(String, nullable=True)
    imdb_rating = Column(String, nullable=True)
    director = Column(String, nullable=True)
    actors = Column(String, nullable=True)
    type = Column(String, default="movie")
    season = Column(Integer, nullable=True)
    episode = Column(Integer, nullable=True)    
    timestamp = Column(String, nullable=True)
    filepath = Column(String, nullable=True)
    status = Column(String, index=True)