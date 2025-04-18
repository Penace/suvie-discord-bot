from sqlalchemy import Column, Integer, String, Text, BigInteger, Boolean
from bot.utils.database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(BigInteger, index=True)
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
    downloaded = Column(Boolean, default=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "guild_id": self.guild_id,
            "title": self.title,
            "year": self.year,
            "genre": self.genre,
            "plot": self.plot,
            "poster": self.poster,
            "imdb_url": self.imdb_url,
            "imdb_id": self.imdb_id,
            "imdb_rating": self.imdb_rating,
            "director": self.director,
            "actors": self.actors,
            "type": self.type,
            "season": self.season,
            "episode": self.episode,
            "timestamp": self.timestamp,
            "filepath": self.filepath,
            "status": self.status,
            "downloaded": self.downloaded,
        }