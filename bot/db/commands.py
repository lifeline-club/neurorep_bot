from sqlalchemy import text

from bot.db.settings import engine


def create_tables():
    with engine.connect() as conn:
        conn.execute(
            text("""--sql
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    state INTEGER DEFAULT 0,
    meta TEXT
)
""")
        )
        conn.commit()
