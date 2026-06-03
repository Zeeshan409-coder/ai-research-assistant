from app.db.postgres import engine, Base
# Explicitly import models to register them inside the Base metadata catalog
from app.models.conversation import Conversation, Message


def create_tables():
    print("--- Verifying/Creating PostgreSQL Database Tables ---")
    # This single call automatically scans and constructs all missing registered schemas
    Base.metadata.create_all(bind=engine)
    print("--- Database Tables Verified/Created Successfully ---")
