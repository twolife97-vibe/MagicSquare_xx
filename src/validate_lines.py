# --- Entity ---

MAGIC_CONSTANT = 34

LINE_IDS = (
    "R1", "R2", "R3", "R4",
    "C1", "C2", "C3", "C4",
    "D1", "D2",
)


# --- Control / Boundary: validate_lines(grid) -> dict ---

def validate_lines(grid) -> dict:
    """
    4×4 격자의 10선(행·열·대각) 합을 검증한다.

    Returns:
        {"status": "pass" | "fail" | "incomplete", "failed_lines": [...]}
    """
    pass
