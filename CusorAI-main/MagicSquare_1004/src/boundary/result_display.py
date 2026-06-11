"""검증 결과 표시 위젯 — Boundary ResultDisplay 프로토타입."""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from src.boundary.input_handler import ERROR_INVALID_VALUE, ERROR_NONE_GRID
from src.validate_lines import ValidationResult

_STATUS_STYLES = {
    "pass": ("통과", "color: #1b7a3d; font-weight: bold;"),
    "fail": ("실패", "color: #c0392b; font-weight: bold;"),
    "incomplete": ("미완성", "color: #b8860b; font-weight: bold;"),
}

_INPUT_ERROR_MESSAGES = {
    ERROR_NONE_GRID: "E003 — 격자가 없습니다.",
    ERROR_INVALID_VALUE: "E002 — 0 또는 1~16만 입력할 수 있습니다.",
}


class ResultDisplay(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._status_label = QLabel("검증 버튼을 눌러 10선 합을 확인하세요.")
        self._failed_label = QLabel("")
        self._failed_label.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self._status_label)
        layout.addWidget(self._failed_label)

    def show_input_error(self, error_code: str) -> None:
        message = _INPUT_ERROR_MESSAGES.get(error_code, f"{error_code} — 입력 오류")
        self._status_label.setText(message)
        self._status_label.setStyleSheet("color: #c0392b; font-weight: bold;")
        self._failed_label.setText("")

    def show_validation(self, result: ValidationResult) -> None:
        status = result["status"]
        label, style = _STATUS_STYLES.get(status, (status, ""))
        self._status_label.setText(f"결과: {label}")
        self._status_label.setStyleSheet(style)

        failed_lines = result["failed_lines"]
        if failed_lines:
            self._failed_label.setText(f"실패 줄: {', '.join(failed_lines)}")
        else:
            self._failed_label.setText("")
