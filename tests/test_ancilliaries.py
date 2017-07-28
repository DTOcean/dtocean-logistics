
import pytest

from dtocean_logistics.ancillaries.diff import differences


@pytest.mark.parametrize("test_input, expected", [
    ([], []),
    ([1], []),
    ([1,2], [1]),
    ([1,2,4], [1,2]),
    ([-1,1], [2]),
    ([1,-1], [-2]),
])
def test_differences(test_input, expected):
    
    result = differences(test_input)
    
    assert result == expected
