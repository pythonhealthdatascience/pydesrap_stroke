"""
Unit tests

Unit tests are a type of functional testing that focuses on individual
components (e.g. methods, classes) and tests them in isolation to ensure they
work as intended.
"""

from io import StringIO
import logging
import os
from unittest.mock import patch, MagicMock

import numpy as np
import pytest
from sim_tools.distributions import Exponential, Lognormal, Discrete

from simulation.parameters import (
    ASUArrivals, RehabArrivals, ASULOS, RehabLOS,
    ASURouting, RehabRouting, Param)
from simulation.model import Model
from simulation.runner import Runner
from simulation.logging import SimLogger


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


def test_param_valid():
    """
    Check that all default model parameters are valid.
    """
    try:
        Param().check_param_validity()
    # pylint: disable=broad-exception-caught
    except Exception as exc:
        pytest.fail(
            f"check_param_validity() raised an unexpected exception: {exc}")


@pytest.mark.parametrize("param, value, msg", [
    ("warm_up_period", -1,
     "Parameter 'warm_up_period' must be greater than or equal to 0"),
    ("data_collection_period", -5,
     "Parameter 'data_collection_period' must be greater than or equal to 0"),
    ("number_of_runs", 0,
     "Parameter 'number_of_runs' must be greater than 0"),
    ("audit_interval", -2,
     "Parameter 'audit_interval' must be greater than 0")])
def test_param_errors(param, value, msg):
    """
    Check that `check_param_validity()` catches parameter issues.
    """
    model_param = Param()
    setattr(model_param, param, value)
    with pytest.raises(ValueError, match=msg):
        model_param.check_param_validity()


def test_arrival_params():
    """
    Test validation of arrival parameters.
    """
    model_param = Param(asu_arrivals=ASUArrivals(stroke=-5))
    with pytest.raises(
        ValueError,
        match="Parameter 'stroke' from 'asu_arrivals' must be greater than 0"
    ):
        model_param.check_param_validity()


def test_los_params():
    """
    Test validation of length of stay parameters.
    """
    model_param = Param(asu_los=ASULOS(neuro_mean=-2, neuro_sd=1))
    with pytest.raises(
        ValueError,
        match=("Parameter 'mean' for 'neuro' in 'asu_los' must be greater " +
               "than 0")
    ):
        model_param.check_param_validity()


def test_routing_sum():
    """
    Test validation of routing probabilities sum.
    """
    model_param = Param(asu_routing=ASURouting(
        tia_rehab=0.6, tia_esd=0.2, tia_other=0.1))
    with pytest.raises(
        ValueError,
        match=("Routing probabilities for 'tia' in 'asu_routing' should sum " +
               "to apx. 1")
    ):
        model_param.check_param_validity()


def test_routing_range():
    """
    Test validation of routing probability ranges.
    """
    model_param = Param(asu_routing=ASURouting(
        neuro_rehab=1.1, neuro_esd=0.1, neuro_other=-0.2))
    with pytest.raises(ValueError, match="must be between 0 and 1"):
        model_param.check_param_validity()


# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------

def test_create_distributions():
    """
    Check that distributions are all the correct type.
    """
    param = Param()
    model = Model(param, run_number=42)

    # Check that all arrival distributions are Exponential
    for _, unit_dict in model.arrival_dist.items():
        for patient_type in unit_dict:
            assert isinstance(unit_dict[patient_type], Exponential)

    # Check that all length of stay distributions are Lognormal
    for _, unit_dict in model.los_dist.items():
        for patient_type in unit_dict:
            assert isinstance(unit_dict[patient_type], Lognormal)

    # Check that all routing distributions are Discrete
    for _, unit_dict in model.routing_dist.items():
        for patient_type in unit_dict:
            assert isinstance(unit_dict[patient_type], Discrete)


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


# -----------------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------------

def test_get_occupancy_freq():
    """
    Test the `get_occupancy_freq` method works as expected.

    Notes
    -----
    Inspired by `test_result_processing_1` and `test_result_processing_2` in
    github.com/pythonhealthdatascience/llm_simpy/.
    """
    # Create test data
    audit_list = []
    for count, value in [(4, 1), (3, 2), (2, 3), (1, 4)]:
        for _ in range(count):
            audit_list.append({"asu_occupancy": value,
                               "rehab_occupancy": value + 1})

    # Define expected values for our test data
    expected_beds = [1, 2, 3, 4]
    expected_freq = [4, 3, 2, 1]
    expected_pct = [0.4, 0.3, 0.2, 0.1]
    expected_c_pct = [0.4, 0.7, 0.9, 1.0]
    expected_prob_delay = [1.0, 0.3/0.7, 0.2/0.9, 0.1/1.0]

    # Create a Runner instance
    runner = Runner(None)

    # Call the method
    result_df = runner.get_occupancy_freq(audit_list, "asu")

    # Check the structure of the DataFrame
    assert list(result_df.columns) == [
        "beds", "freq", "pct", "c_pct", "prob_delay"]

    # Check the values
    assert list(result_df["beds"]) == expected_beds
    assert list(result_df["freq"]) == expected_freq
    assert np.allclose(result_df["pct"], expected_pct)
    assert np.allclose(result_df["c_pct"], expected_c_pct)

    # Check prob_delay calculation
    assert np.allclose(result_df["prob_delay"], expected_prob_delay)


# -----------------------------------------------------------------------------
# SimLogger
# -----------------------------------------------------------------------------

def test_log_to_console():
    """
    Confirm that logger.log() prints the provided message to the console.

    Notes
    -----
    Test from github.com/pythonhealthdatascience/rap_template_python_des.
    """
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        logger = SimLogger(log_to_console=True)
        logger.log(sim_time=None, msg="Test console log")
        # Check if console output matches
        assert "Test console log" in mock_stdout.getvalue()


def test_log_to_file():
    """
    Confirm that logger.log() would output the message to a .log file at the
    provided file path.

    Notes
    -----
    Test from github.com/pythonhealthdatascience/rap_template_python_des.
    """
    # Mock the file open operation
    with patch('builtins.open', new_callable=MagicMock) as mock_open:
        # Create the logger and log a simple example
        logger = SimLogger(log_to_file=True, file_path="test.log")
        logger.log(sim_time=None, msg="Log message")

        # Check that the file was opened in write mode at the absolute path
        mock_open.assert_called_with(
            os.path.abspath("test.log"), "w", encoding="locale", errors=None)

        # Verify a FileHandler is attached to the logger
        assert (any(isinstance(handler, logging.FileHandler)
                    for handler in logger.logger.handlers))


def test_invalid_path():
    """
    Ensure there is appropriate error handling for an invalid file path.
    """
    with pytest.raises(ValueError):
        SimLogger(log_to_file=True, file_path="/invalid/path/to/log.log")


def test_invalid_file_extension():
    """
    Ensure there is appropriate error handling for an invalid file extension.
    """
    with pytest.raises(ValueError):
        SimLogger(log_to_file=True, file_path="test.txt")
