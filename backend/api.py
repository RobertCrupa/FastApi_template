from fastapi import FastAPI
from pathlib import Path

app = FastAPI()

PROJECT_ROOT = Path(__file__).parent.parent