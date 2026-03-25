from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.models import UserInput
from api.pipeline.pipeline import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/status")
def read_status():
    return {"status": "API is online"}


@app.post("/api/rag/question")
async def ask_question(body: UserInput):
    return await pipeline(body.question)
