
import pytest

from dtocean_logistics.phases.install.shared import get_burial_equip


@pytest.mark.parametrize("test_input, expected", [
    ('ploughing', 'plough'),
    ('jetting', 'jetter'),
    ('cutting', 'cutter'),
    ('dredging', 'dredge'),
    ('no burial', None),
    ('no data', 'plough'),
    (None, 'plough')
])
def test_get_burial_equip(test_input, expected):
    
    result = get_burial_equip(test_input)
    
    assert result == expected
