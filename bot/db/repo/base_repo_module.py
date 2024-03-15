from enum import Enum
from sqlalchemy import CursorResult, text

from bot.db.settings import engine

class operationStatus(Enum):
    OK = 1
    NOT_FOUND = -1


class BaseRepoModule:
    operation_status = operationStatus

    engine = engine

    def execute_command(self, request: str) -> CursorResult:
        with self.engine.connect() as conn:
            return conn.execute(text(request))


    def get_from_db(self, request: str) -> list[dict]:
        raw_result = self.execute_command(request)
        return [q._asdict() for q in raw_result.all()]
