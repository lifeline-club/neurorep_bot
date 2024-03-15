from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine

load_dotenv()
POSTGRES_CONN = getenv("POSTGRES_CONN")

if not POSTGRES_CONN:
    raise ValueError("Incomplete environment variables.")

engine = create_engine(
    POSTGRES_CONN,
    echo=True,
)
