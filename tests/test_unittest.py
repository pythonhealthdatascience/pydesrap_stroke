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
from sim_tools.distributions import Exponential, Lognormal, DiscreteEmpirical

from simulation import Model, Param, Runner, SimLogger


# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------

def test_new_attribute():
    """
    Confirm that it's impossible to add new attributes.
    """
    param = Param()
    with pytest.raises(AttributeError,
                       match="only possible to modify existing attributes"):
        setattr(param, "new_entry", 3)


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


# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------

def test_create_distributions():
    """
    Check that distributions are all the correct type.
    """
    param = Param()
    model = Model(param, run_number=42)

    # Check that all arrival distributions are exponential
    for _, unit_dict in model.dist["arrival"].items():
        for patient_type in unit_dict:
            assert isinstance(unit_dict[patient_type], Exponential)

    # Check that all length of stay distributions are lognormal
    for _, unit_dict in model.dist["los"].items():
        for patient_type in unit_dict:
            assert isinstance(unit_dict[patient_type], Lognormal)

    # Check that all routing distributions are discrete
    for _, unit_dict in model.dist["routing"].items():
        for patient_type in unit_dict:
            assert isinstance(unit_dict[patient_type], DiscreteEmpirical)


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
    samples1 = [model1.dist["arrival"]["asu"]["stroke"].sample()
                for _ in range(10)]
    samples2 = [model2.dist["arrival"]["asu"]["stroke"].sample()
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
    expected_1_in_n_delay = [1, 2, 4, 10]

    # Create a Runner instance
    runner = Runner(None)

    # Call the method
    result_df = runner.get_occupancy_freq(audit_list, "asu")

    # Check the structure of the DataFrame
    assert list(result_df.columns) == [
        "beds", "freq", "pct", "c_pct", "prob_delay", "1_in_n_delay"]

    # Check the values
    assert list(result_df["beds"]) == expected_beds
    assert list(result_df["freq"]) == expected_freq
    assert np.allclose(result_df["pct"], expected_pct)
    assert np.allclose(result_df["c_pct"], expected_c_pct)

    # Check prob_delay and 1 in n delay calculations
    assert np.allclose(result_df["prob_delay"], expected_prob_delay)
    assert np.allclose(result_df["1_in_n_delay"], expected_1_in_n_delay)


# -----------------------------------------------------------------------------
# SimLogger
# -----------------------------------------------------------------------------

def test_log_to_console():
    """
    Confirm that logger.log() prints the provided message to the console.

    Notes
    -----
    Test from github.com/pythonhealthdatascience/pydesrap_mms.
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
    Test from github.com/pythonhealthdatascience/pydesrap_mms.
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
