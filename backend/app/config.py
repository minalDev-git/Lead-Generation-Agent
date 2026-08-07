from dotenv import load_dotenv
import os
from rich.console import Console

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT", "8000"))

DEBUG = os.getenv("DEBUG") == "True"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
GROQ_LIGHT_MODEL = os.getenv("GROQ_LIGHT_MODEL")

HEADLESS = os.getenv("HEADLESS") == "True"

OUTPUT_DIR = os.getenv("OUTPUT_DIR")

CONSOLE = Console()