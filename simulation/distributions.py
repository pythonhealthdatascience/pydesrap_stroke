"""
Distributions.

Acknowledgements:
    > Heather, A. Monks, T. (2025). Python DES RAP Template.
    https://github.com/pythonhealthdatascience/rap_template_python_des (MIT).
    > Monks, T. (2021) sim-tools: fundamental tools to support the simulation
    process in python. https://github.com/TomMonks/sim-tools. (MIT).
"""

import math
import numpy as np


class Exponential:
    """
    Generate samples from an exponential distribution.

    This class is from Heather and Monks 2025, who adapted from Monks 2021.
    """
    def __init__(self, mean, random_seed=None):
        """
        Initialises a new distribution.

        Arguments:
            mean (float):
                Mean of the exponential distribution.
            random_seed (int|None):
                Random seed to control sampling.
        """
        if mean <= 0:
            raise ValueError('Exponential mean must be greater than 0.')

        self.mean = mean
        self.rand = np.random.default_rng(random_seed)

    def sample(self, size=None):
        """
        Generate sample.

        Arguments:
            size (int|None):
                Number of samples to return. If set to none, then returns a
                single sample.

        Returns:
            float or numpy.ndarray:
                A single sample if size is None, or an array of samples if
                size is specified.
        """
        return self.rand.exponential(self.mean, size=size)


class LogNormal:
    """
    Generate samples from a lognormal distribution.

    This class is adapted from Monks 2021.
    """
    def __init__(self, mean, stdev, random_seed=None):
        """
        Initialises a new distribution.

        Arguments:
            mean (float):
                Mean of the lognormal distribution.
            stdev (float):
                Standard deviation of the lognormal distribution.
            random_seed (int|None):
                Random seed to control sampling.
        """
        self.mu, self.sigma = (
            self.normal_moments_from_lognormal(m=mean, v=stdev**2))
        self.rand = np.random.default_rng(random_seed)

    def normal_moments_from_lognormal(self, m, v):
        """
        Calculate mu and sigma of normal distribution underlying a lognormal
        with mean m and variance v. Source: https://blogs.sas.com/content/iml/2
        014/06/04/simulate-lognormal-data-with-specified-mean-and-variance.html

        Arguments:
            m (float):
                Mean of the lognormal distribution.
            v (float):
                Variance of the lognormal distribution.

        Returns:
            float, float
                Mu and sigma.
        """
        phi = math.sqrt(v + m**2)
        mu = math.log(m**2 / phi)
        sigma = math.sqrt(math.log(phi**2 / m**2))
        return mu, sigma

    def sample(self, size=None):
        """
        Generate sample.

        Arguments:
            size (int|None):
                Number of samples to return. If set to none, then returns a
                single sample.

        Returns:
            float or numpy.ndarray:
                A single sample if size is None, or an array of samples if
                size is specified.
        """
        return self.rand.lognormal(self.mu, self.sigma, size=size)


class Discrete:
    """
    Generate samples from a discrete distribution.

    This class is adapted from Monks 2021.
    """
    def __init__(self, values, freq, random_seed=None):
        """
        Initialises a new distribution.

        Arguments:
            values (array-like):
                List of sample values. Must be equal length to freq.
            freq (array-like):
                List of observed frequencies. Must be equal length to values.
            random_seed (int|None):
                Random seed to control sampling.
        """
        if len(values) != len(freq):
            raise ValueError(
                'values and freq arguments must be of equal length')
        self.values = np.asarray(values)
        self.freq = np.asarray(freq)
        self.probabilities = self.freq / self.freq.sum()
        self.rand = np.random.default_rng(random_seed)

    def sample(self, size=None):
        """
        Generate sample.

        Arguments:
            size (int|None):
                Number of samples to return. If set to none, then returns a
                single sample.

        Returns:
            float or numpy.ndarray:
                A single sample if size is None, or an array of samples if
                size is specified.
        """
        sample = self.rand.choice(self.values, p=self.probabilities, size=size)

        if size is None:
            return sample.item()
        return sample
