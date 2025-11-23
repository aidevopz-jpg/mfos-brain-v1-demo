from app.agents.base_llm import call_openai

REVIEWER_SYSTEM_PROMPT = """
You are the MFOS Reviewer agent. You review content for:

- logical coherence,
- completeness,
- consistency with the MFOS Constitution (tenant stability, vendor dignity, non-coercion),
- terminology alignment with MFOS ontology.

You DO NOT rewrite the full text.
You output:
- bullet-point corrections,
- missing pieces,
- ethical alignment notes.
"""

async def run_reviewer(architect_output: str, prompt: str) -> str:
    user_prompt = f"""
Original user request:
{prompt}

Architect's proposal:
{architect_output}

Review and list:
1) Logical issues
2) Missing considerations
3) Ethical/alignment concerns
4) Suggested fixes (short).
"""
    return await call_openai(REVIEWER_SYSTEM_PROMPT, user_prompt, temperature=0.3)
