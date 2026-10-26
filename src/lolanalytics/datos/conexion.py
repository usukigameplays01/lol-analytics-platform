from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lolanalytics import config

url = config.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)