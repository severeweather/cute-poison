from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

from dotenv import load_dotenv
load_dotenv()

import os
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL env variable not set")

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)