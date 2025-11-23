from app.agents.base_llm import call_openai

SCRIBE_SYSTEM_PROMPT = """
You are the MFOS Scribe agent. You integrate multi-agent outputs into:

- a clean, coherent, well-structured chapter or section
- that could be placed into the MFOS blueprint.

You DO NOT add new ideas; you integrate what Architect, Reviewer, Challenger, and COO produced.

Your output should be:
- readable,
- clearly sectioned with headings,
- ready for storage in the Memory Spine.
"""

async def run_scribe(prompt: str, architect_output: str, reviewer_output: str, challenger_output: str, coo_output: str) -> str:
    user_prompt = f"""
Original user request:
{prompt}

Architect:
{architect_output}

Reviewer:
{reviewer_output}

Challenger:
{challenger_output}

COO:
{coo_output}

Integrate the above into a single, coherent blueprint section.
Use headings and bullet points as needed.
"""
    return await call_openai(SCRIBE_SYSTEM_PROMPT, user_prompt, temperature=0.2)
