"""
Unit tests
"""

import pytest

from simulation.parameters import (
    ASUArrivals, RehabArrivals, ASULOS, RehabLOS,
    ASURouting, RehabRouting, Param)


@pytest.mark.parametrize('class_to_test', [
    ASUArrivals, RehabArrivals, ASULOS, RehabLOS,
    ASURouting, RehabRouting, Param])
def test_new_attribute(class_to_test):
    """
    Confirm that it's impossible to add new attributes to the classes.

    Arguments:
        class_to_test (class):
            The class to be tested for attribute immutability.
    """
    # Create an instance of the class
    instance = class_to_test()

    # Attempt to add a new attribute
    with pytest.raises(AttributeError,
                       match='only possible to modify existing attributes'):
        setattr(instance, 'new_entry', 3)
