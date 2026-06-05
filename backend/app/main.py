from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router
from app.api.search import router as search_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router
from app.api.streaming_chat import router as streaming_chat_router
from app.api.workspaces import router as workspaces_router
from app.api.auth import router as auth_router  
from app.api.users import router as users_router  # 👈 Imported your new SaaS profile manager router
from app.services.qdrant_service import create_collection
from app.db.init_db import create_tables

app = FastAPI(title="AI Research Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    try:
        create_tables()
    except Exception as e:
        print(f"--- Warning during PostgreSQL startup table initialization: {e} ---")

    try:
        create_collection()
        print("--- Qdrant Collection Verified/Created Successfully ---")
    except Exception as e:
        print(f"--- Warning during Qdrant startup collection check: {e} ---")


app.include_router(upload_router)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(streaming_chat_router)
app.include_router(workspaces_router)
app.include_router(auth_router)  
app.include_router(users_router)  # 👈 Mounted your secure user profiles endpoints tracker
