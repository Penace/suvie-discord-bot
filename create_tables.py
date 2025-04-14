import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv
load_dotenv()

from bot.utils.database import Base, engine
from bot.models.movie import Movie

Base.metadata.create_all(bind=engine)
print("✅ Tables created.")