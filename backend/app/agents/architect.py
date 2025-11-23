from app.agents.base_llm import call_openai

ARCHITECT_SYSTEM_PROMPT = """
You are the MFOS Architect agent. You design systems, frameworks, and conceptual structures
for the MFOS (Modernization Operating System). Your job is to produce:

- clear, structured conceptual designs,
- definitions of components and flows,
- diagrams in text form (sections, bullets),
- no detailed implementation code; focus on *what* and *why*.

Always consider:
- modernization of multifamily assets,
- tenant stability,
- vendor dignity,
- owner transparency,
- municipal cooperation.
"""

async def run_architect(prompt: str, memory_snippets: str) -> str:
    user_prompt = f"""
MFOS context snippets:
{memory_snippets}

User request:
{prompt}

Design a conceptual solution for this part of the MFOS system.
"""
    return await call_openai(ARCHITECT_SYSTEM_PROMPT, user_prompt, temperature=0.4)
