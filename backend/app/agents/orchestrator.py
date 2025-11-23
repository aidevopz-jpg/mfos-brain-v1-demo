from typing import List
from app.models.types import AgentOutput, BrainRunResponse
from app.memory.memory_spine import search_memory, save_memory
from app.agents.architect import run_architect
from app.agents.reviewer import run_reviewer
from app.agents.challenger import run_challenger
from app.agents.coo import run_coo
from app.agents.scribe import run_scribe

async def run_brain(prompt: str) -> BrainRunResponse:
    # 1) Retrieve context from memory
    memory_results = search_memory(prompt, n_results=3)
    memory_snippets = "\n\n".join([m["text"] for m in memory_results])

    agent_outputs: List[AgentOutput] = []

    orchestrator_analysis = f"Interpreting request and routing: Architect → Reviewer → Challenger → COO → Scribe. Memory hits: {len(memory_results)}"
    agent_outputs.append(AgentOutput(name="orchestrator", content=orchestrator_analysis))

    # 2) Architect
    architect_output = await run_architect(prompt, memory_snippets)
    agent_outputs.append(AgentOutput(name="architect", content=architect_output))

    # 3) Reviewer
    reviewer_output = await run_reviewer(architect_output, prompt)
    agent_outputs.append(AgentOutput(name="reviewer", content=reviewer_output))

    # 4) Challenger
    challenger_output = await run_challenger(architect_output, prompt)
    agent_outputs.append(AgentOutput(name="challenger", content=challenger_output))

    # 5) COO
    coo_output = await run_coo(architect_output, reviewer_output, challenger_output, prompt)
    agent_outputs.append(AgentOutput(name="coo", content=coo_output))

    # 6) Scribe
    scribe_output = await run_scribe(prompt, architect_output, reviewer_output, challenger_output, coo_output)
    agent_outputs.append(AgentOutput(name="scribe", content=scribe_output))

    # 7) Save to Memory Spine
    mem_id = save_memory(scribe_output, tags=["demo", "blueprint"], source_agent="Scribe")

    # 8) Final orchestrator wrap-up
    final_note = f"MFOS Brain run complete. Stored integrated blueprint as memory id {mem_id}."
    agent_outputs.append(AgentOutput(name="orchestrator_final", content=final_note))

    return BrainRunResponse(
        prompt=prompt,
        agent_outputs=agent_outputs,
        final_output=scribe_output,
        memory_entry_id=mem_id
    )
