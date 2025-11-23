from app.agents.base_llm import call_openai

COO_SYSTEM_PROMPT = """
You are the MFOS COO agent. You convert conceptual designs into:

- implementation plans,
- architecture outlines,
- epics and stories for engineers,
- file structures,
- rough timelines and milestones.

Optimize for:
- minimal MVP scope,
- clear sequencing,
- cost and time efficiency,
- extensibility.

Respect the MFOS Constitution at all times.
"""

async def run_coo(architect_output: str, reviewer_output: str, challenger_output: str, prompt: str) -> str:
    user_prompt = f"""
Original user request:
{prompt}

Architect's proposal:
{architect_output}

Reviewer notes:
{reviewer_output}

Challenger risks:
{challenger_output}

Create an actionable implementation plan for a 4–8 week MVP effort, including:
- main components,
- key endpoints or services,
- epics and tasks,
- approximate sequencing.
"""
    return await call_openai(COO_SYSTEM_PROMPT, user_prompt, temperature=0.35)
