"""
Unit tests
"""

import numpy as np
import pytest

from simulation.parameters import (
    ASUArrivals, RehabArrivals, ASULOS, RehabLOS,
    ASURouting, RehabRouting, Param)
from simulation.distributions import Exponential, LogNormal, Discrete


# -----------------------------------------------------------------------------
# Parameter classes
# -----------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------
# Distributions
# -----------------------------------------------------------------------------

@pytest.mark.parametrize('dist_class, params, expected_mean, expected_type', [
    (Exponential, {'mean': 5}, 5, float),
    (LogNormal, {'mean': 1, 'stdev': 0.5}, 1, float),
    (Discrete, {'values': [1, 2, 3], 'freq': [0.2, 0.5, 0.3]}, 2.1, int)
])
def test_samples(dist_class, params, expected_mean, expected_type):
    """
    Test that generated samples match the expected mean and requested size,
    and that the random seed is working.

    Arguments:
        dist_class (class):
            Distribution class to test.
        params (dict):
            Parameters for initialising the distribution.
        expected_mean (float):
            Expected mean of the distribution.
        expected_type (type):
            Expected type of the sample (float for continuous distributions,
            int for discrete).
    """
    # Initialise the distribution
    dist = dist_class(random_seed=42, **params)

    # Check that sample is a float
    x = dist.sample()
    assert isinstance(x, expected_type), (
        f'Expected sample() to return a {expected_type} - instead: {type(x)}'
    )

    # Check that the mean of generated samples is close to the expected mean
    samples = dist.sample(size=10000)
    assert np.isclose(np.mean(samples), expected_mean, rtol=0.1)

    # Check that the sample size matches the requested size
    assert len(samples) == 10000

    # Check that the same seed returns the same sample
    sample1 = dist_class(random_seed=5, **params).sample(size=5)
    sample2 = dist_class(random_seed=5, **params).sample(size=5)
    assert np.array_equal(sample1, sample2), (
        'Samples with the same random seeds should be equal.'
    )

    # Check that different seeds return different samples
    sample3 = dist_class(random_seed=89, **params).sample(size=5)
    assert not np.array_equal(sample1, sample3), (
        'Samples with different random seeds should not be equal.'
    )


def test_invalid_exponential():
    """
    Ensure that Exponential distribution cannot be created with a negative
    or zero mean.
    """
    # Negative mean
    with pytest.raises(ValueError):
        Exponential(mean=-5, random_seed=42)

    # Zero mean
    with pytest.raises(ValueError):
        Exponential(mean=0, random_seed=42)

    # Check that no negative values are sampled
    d = Exponential(mean=10, random_seed=42)
    bigsample = d.sample(size=100000)
    assert all(x > 0 for x in bigsample), (
        'Sample contains non-positive values.'
    )


def test_lognormal_moments():
    """
    Test the calculation of normal distribution parameters (mu, sigma) from
    lognormal parameters.

    This test verifies that:
    1. The normal_moments_from_lognormal method correctly converts lognormal
    parameters (mean, variance) to normal distribution parameters (mu, sigma).
    2. The calculated values match the expected mathematical formulas.
    """
    # Define lognormal parameters
    mean, stdev = 2.0, 0.5

    # Initialise distribution and get calculated parameters
    dist = LogNormal(mean=mean, stdev=stdev, random_seed=42)
    calculated_mu, calculated_sigma = (
        dist.normal_moments_from_lognormal(mean, stdev**2))

    # Verify calculated parameters match expected mathematical formulas
    # Formula for mu: ln(mean²/√(stdev² + mean²))
    assert np.isclose(calculated_mu,
                      np.log(mean**2 / np.sqrt(stdev**2 + mean**2)),
                      rtol=1e-5)
    # Formula for sigma: √ln(1 + stdev²/mean²)
    assert np.isclose(calculated_sigma,
                      np.sqrt(np.log(1 + stdev**2 / mean**2)),
                      rtol=1e-5)


def test_discrete_probabilities():
    """
    Test correct calculation of probabilities for Discrete distribution.

    This test verifies that:
    1. The Discrete class correctly normalizes frequency values to
    probabilities.
    2. The sum of probabilities equals 1
    3. The relative proportions match the input frequencies
    """
    # Define discrete distribution parameters
    values = [1, 2, 3]
    freq = [10, 20, 30]

    # Initialise distribution
    dist = Discrete(values=values, freq=freq, random_seed=42)

    # Calculate expected probabilities by normalising frequencies
    expected_probs = np.array(freq) / np.sum(freq)

    # Verify calculated probabilities match expected values
    assert np.allclose(dist.probabilities, expected_probs, rtol=1e-5)

    # Verify probabilities sum to 1
    assert np.isclose(np.sum(dist.probabilities), 1.0, rtol=1e-10)


def test_discrete_value_error():
    """
    Test if Discrete raises ValueError for mismatched inputs.

    This test verifies that the Discrete class correctly validates that
    the values and frequencies arrays have the same length.
    """
    # Attempt to initialise with mismatched array lengths
    with pytest.raises(ValueError):
        Discrete(values=[1, 2], freq=[0.5], random_seed=42)


def test_invalid_input_types():
    """
    Test error handling for invalid string input types.

    This test verifies that appropriate errors are raised when
    string values are provided instead of numeric values for
    distribution parameters.
    """
    with pytest.raises(TypeError):
        Exponential(mean='5')
    with pytest.raises(TypeError):
        LogNormal(mean='4', stdev=1)
    with pytest.raises(TypeError):
        Discrete(values=[1, 2, 3], freq=['0.2', '0.5', '0.3'])


def test_discrete_uneven_probabilities():
    """
    Test behavior of Discrete distribution with highly uneven probabilities.

    This test verifies that when one probability is much larger than another,
    the sampling correctly reflects this imbalance by rarely selecting the
    low-probability value.
    """
    # Create distribution with extremely uneven probabilities
    dist = Discrete(values=[1, 2], freq=[1, 1e-10], random_seed=42)

    # Generate a large sample
    samples = dist.sample(size=10000)

    # Verify that the low-probability value (2) appears very rarely
    # With p ≈ 1e-10, we expect virtually no occurrences of value 2
    assert np.sum(samples == 2) < 5
