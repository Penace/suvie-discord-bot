from dotenv import load_dotenv
load_dotenv()

from bot.utils.database import Base, engine
from bot.models.movie import Movie

Base.metadata.create_all(bind=engine)
print("✅ Tables created.")