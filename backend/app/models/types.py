from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AgentOutput(BaseModel):
    name: str
    content: str
    metadata: Dict[str, Any] = {}

class BrainRunRequest(BaseModel):
    prompt: str

class BrainRunResponse(BaseModel):
    prompt: str
    agent_outputs: List[AgentOutput]
    final_output: str
    memory_entry_id: Optional[str] = None

class MemoryItem(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any]
