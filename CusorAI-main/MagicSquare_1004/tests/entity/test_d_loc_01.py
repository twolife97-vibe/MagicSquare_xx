from src.entity.find_blank_coords import find_blank_coords
from tests._approval import assert_matches_golden, format_coord_list

GOLDEN_D_LOC_01 = "d_loc_01_g1_blank_coords.approved.txt"


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자 (0이 2개)
    # When: find_blank_coords(grid_g1) 호출
    # Then: [(2,3),(4,4)] — golden 1-index row-major (I6)
    actual = find_blank_coords(grid_g1)
    assert_matches_golden(format_coord_list(actual), GOLDEN_D_LOC_01)
