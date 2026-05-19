"""FastAPI entry point for the LVSHAGNT platform."""
from __future__ import annotations
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.orchestrator.orchestrator import Orchestrator

orchestrator = Orchestrator(llm_provider=os.getenv("LLM_PROVIDER", "openai"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await orchestrator.startup()
    yield
    await orchestrator.shutdown()


app = FastAPI(title="LVSHAGNT API", version="1.0.0", lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"
    session_id: str = "default"


class AgentRequest(BaseModel):
    agent: str
    task_type: str
    payload: dict = {}


@app.get("/health")
async def health():
    return {"status": "ok", "agents": ["enchantedagent", "lvshopagent", "lvshplanagent", "lvshgenagent", "database_agent"]}


@app.post("/chat")
async def chat(req: ChatRequest):
    response = await orchestrator.chat(req.message, req.user_id, req.session_id)
    return {"response": response, "session_id": req.session_id}


@app.post("/agent/run")
async def run_agent(req: AgentRequest):
    payload = {"task_type": req.task_type, **req.payload}
    result = await orchestrator.handle(req.agent, payload)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return {"success": True, "data": result.data, "agent": result.agent}
