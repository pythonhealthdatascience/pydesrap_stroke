"""
Unit tests
"""

from collections import namedtuple
import numpy as np
import pytest
from sim_tools.distributions import Exponential

from simulation.parameters import (
    ASUArrivals, RehabArrivals, ASULOS, RehabLOS,
    ASURouting, RehabRouting, Param)
from simulation.model import Model


# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("class_to_test", [
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
                       match="only possible to modify existing attributes"):
        setattr(instance, "new_entry", 3)


# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------

def test_create_distributions():
    """
    Test that distributions are created correctly for all units and patient
    types specified.
    """
    param = Param(
        asu_arrivals=namedtuple(
            "ASUArrivals", ["stroke", "tia", "neuro", "other"])(
            stroke=5, tia=7, neuro=10, other=15),
        rehab_arrivals=namedtuple(
            "RehabArrivals", ["stroke", "tia", "other"])(
            stroke=8, tia=12, other=20))
    model = Model(param, run_number=42)

    # Check ASU arrival distributions
    assert len(model.arrival_dist["asu"]) == 4
    assert "stroke" in model.arrival_dist["asu"]
    assert "tia" in model.arrival_dist["asu"]
    assert "neuro" in model.arrival_dist["asu"]
    assert "other" in model.arrival_dist["asu"]

    # Check Rehab arrival distributions
    assert len(model.arrival_dist["rehab"]) == 3
    assert "stroke" in model.arrival_dist["rehab"]
    assert "tia" in model.arrival_dist["rehab"]
    assert "other" in model.arrival_dist["rehab"]
    assert "neuro" not in model.arrival_dist["rehab"]

    # Check that all arrival distributions are Exponential
    for _, unit_dict in model.arrival_dist.items():
        for patient_type in unit_dict:
            assert isinstance(unit_dict[patient_type], Exponential)


def test_sampling_seed_reproducibility():
    """
    Test that using the same seed produces the same results when sampling
    from one of the arrival distributions.
    """
    param = Param()

    # Create two models with the same seed
    model1 = Model(param, run_number=123)
    model2 = Model(param, run_number=123)

    # Sample from a distribution in both models
    samples1 = [model1.arrival_dist["asu"]["stroke"].sample()
                for _ in range(10)]
    samples2 = [model2.arrival_dist["asu"]["stroke"].sample()
                for _ in range(10)]

    # Check that the samples are the same
    np.testing.assert_array_almost_equal(samples1, samples2)


def test_run_time():
    """
    Check that the run length is correct with varying warm-up and data
    collection periods.
    """
    param = Param(warm_up_period=10, data_collection_period=20)

    # Test with zero warm-up period
    param.warm_up_period = 0
    model = Model(param, run_number=42)
    model.run()
    assert model.env.now == param.data_collection_period

    # Test with zero data collection period
    param.warm_up_period = 10
    param.data_collection_period = 0
    model = Model(param, run_number=42)
    model.run()
    assert model.env.now == 10
    # assert len(model.patients) == 0

    # Test with warm-up and data collection period
    param.warm_up_period = 12
    param.data_collection_period = 9
    model = Model(param, run_number=42)
    model.run()
    assert model.env.now == 21
    assert len(model.patients) > 0
