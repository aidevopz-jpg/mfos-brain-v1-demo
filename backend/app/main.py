from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.types import BrainRunRequest, BrainRunResponse
from app.agents.orchestrator import run_brain
from app.memory.memory_spine import list_memory, search_memory, load_initial_memory

app = FastAPI(title="MFOS Brain V1 API")

origins = ["*"]  # tighten for prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    load_initial_memory()

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/run-brain", response_model=BrainRunResponse)
async def api_run_brain(req: BrainRunRequest):
    return await run_brain(req.prompt)

@app.get("/api/memory")
async def api_list_memory():
    items_raw = list_memory(50)
    return items_raw

@app.get("/api/memory/search")
async def api_search_memory(q: str):
    items_raw = search_memory(q, n_results=10)
    return items_raw
