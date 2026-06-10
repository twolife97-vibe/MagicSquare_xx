import pytest

from src.validate_lines import validate_lines


def test_ent_001_complete_grid_pass(grid_pass):
    # Given
    grid = grid_pass

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-ENT-001 — complete 4×4 grid → pass, failed_lines==[]")


def test_ent_002_fail_lists_only_wrong_lines(grid_fail_multi):
    # Given
    grid = grid_fail_multi

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-ENT-002 — no blanks, wrong sums → fail, failed_lines only D2/R3/C3"
    )


def test_ent_003_d1_ok_d2_fail_cannot_pass(grid_fail_d2):
    # Given
    grid = grid_fail_d2

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-ENT-003 — D1 ok, D2 fail → status!=pass, D1∉failed_lines, D2∈failed_lines"
    )


def test_ent_004_blank_line_incomplete(grid_incomplete_r3):
    # Given
    grid = grid_incomplete_r3

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-ENT-004 — blank at (2,1) → incomplete, failed_lines ⊇ {R3,C2,D1}"
    )


def test_ent_005_failed_lines_ids_and_order(grid_fail_multi):
    # Given
    grid = grid_fail_multi

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-ENT-005 — failed_lines ⊆ LINE_IDS, LINE_IDS order, no duplicates"
    )


def test_bnd_001_valid_grid_accepted(grid_pass):
    # Given
    grid = grid_pass

    # When
    _result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-BND-001 — valid 4×4 grid → dict with status and failed_lines keys"
    )
