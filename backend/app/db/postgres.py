from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Corrected host to localhost so your local Python backend can talk to the Docker container
DATABASE_URL = (
    "postgresql://admin:admin@localhost:5432/ragdb"
)

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Dependency function to provide clean database sessions to your API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
