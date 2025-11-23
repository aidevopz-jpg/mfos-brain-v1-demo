import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

if OPENAI_API_KEY is None:
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables.")
