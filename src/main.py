from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.modules.rag.services import rag_service
from src.modules.rag.router import router as rag_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This block executes ON system startup
    print("Initializing RAG Pipeline dependencies...")
    await rag_service.initialize_pipeline()
    yield
    print("Shutting down application...")

app = FastAPI(
    title="Trackmail RAG API",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://trackmail.vercel.app",
    "https://trackmail.changmai.in" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],     
)

app.include_router(rag_router, prefix="/api/v1")

@app.get("/health", tags=["System Health"])
async def health_check():
    return {"status": "operational"}