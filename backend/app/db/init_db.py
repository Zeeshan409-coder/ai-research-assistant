from app.db.postgres import engine, Base
# Explicitly import all relational models to register them inside the Base metadata catalog
from app.models.workspace import Workspace
from app.models.document import Document  # 👈 Registered your new model
from app.models.conversation import Conversation, Message


def create_tables():
    print("--- Verifying/Creating PostgreSQL Database Tables ---")
    Base.metadata.create_all(bind=engine)
    print("--- Database Tables Verified/Created Successfully ---")
