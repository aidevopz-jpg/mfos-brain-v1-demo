from app.agents.base_llm import call_openai

CHALLENGER_SYSTEM_PROMPT = """
You are the MFOS Challenger agent. You attack assumptions and surface:

- failure modes,
- perverse incentives,
- political/legal risks,
- adoption bottlenecks,
- potential harms to tenants, vendors, or owners if misused.

You are adversarial but constructive.
Output a structured list of risks and edge cases.
"""

async def run_challenger(architect_output: str, prompt: str) -> str:
    user_prompt = f"""
Original user request:
{prompt}

Architect's proposal:
{architect_output}

Identify critical risks and edge cases. Be blunt, specific, and practical.
"""
    return await call_openai(CHALLENGER_SYSTEM_PROMPT, user_prompt, temperature=0.5)
