"""FR-IN-01 (워크북) — 격자 입력 검증. 에러 코드는 boundary 전담."""

from __future__ import annotations

from typing import TypedDict

from src.entity.constants import BLANK_CELL, MAX_CELL_VALUE

ERROR_NONE_GRID = "E003"
ERROR_INVALID_VALUE = "E002"


class InputResult(TypedDict):
    error_code: str | None


class InputHandler:
    def validate(self, grid: list[list[int]] | None) -> InputResult:
        if grid is None:
            return {"error_code": ERROR_NONE_GRID}

        for row in grid:
            for cell in row:
                if cell != BLANK_CELL and not (1 <= cell <= MAX_CELL_VALUE):
                    return {"error_code": ERROR_INVALID_VALUE}

        return {"error_code": None}
