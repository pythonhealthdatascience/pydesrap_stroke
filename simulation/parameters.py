"""
Stroke pathway simulation parameters.

It includes arrival rates, length of stay distributions, and routing
probabilities between different care settings.
"""

import json
import os
import time

from simulation.logging import SimLogger
from simulation.restrictattributes import RestrictAttributes


class Param(RestrictAttributes):
    """
    Default parameters for simulation.

    Attributes
    ----------
    dist_config : dict
        Dictionary containing distribution parameters loaded from the
        specified JSON file.
    warm_up_period : int
        Length of the warm-up period (days).
    data_collection_period : int
        Length of the data collection period (days).
    number_of_runs : int
        Number of simulation replications to perform.
    audit_interval : float
        Frequency of simulation audits in days.
    cores : int
        Number of CPU cores to use for parallel processing. Use -1 for all
        available cores; 1 for sequential execution.
    logger : SimLogger
        Logger object for managing logging outputs to console and/or file.
    """
    def __init__(
        self,
        parameter_file=None,
        warm_up_period=365*3,  # 3 years
        data_collection_period=365*5,  # 5 years
        number_of_runs=150,
        audit_interval=1,
        cores=1,
        log_to_console=False,
        log_to_file=False,
        log_file_path=("../outputs/logs/" +
                       f"{time.strftime("%Y-%m-%d_%H-%M-%S")}.log")
    ):
        """
        Initialise a parameter set for the simulation.

        Parameters
        ----------
        parameter_file : str
            JSON file containing parameters to load to sim-tools
            DistributionRegistry.
        warm_up_period : int
            Length of the warm-up period (days).
        data_collection_period : int
            Length of the data collection period (days).
        number_of_runs : int
            Number of simulation replications to perform.
        audit_interval : float
            Frequency of simulation audits in days.
        cores : int
            Number of CPU cores to use for parallel processing. Use -1 for all
        available cores; 1 for sequential execution.
        log_to_console : boolean
            Whether to print log messages to the console.
        log_to_file : boolean
            Whether to save log to a file.
        log_file_path : str
            Path to save log to file. Note, if you use an existing .log
            file name, it will append to that log.
        """
        # Get the default parameter_file path relative to this file
        if parameter_file is None:
            parameter_file = os.path.normpath(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "../inputs/parameters.json")
            )

        # Import distribution parameter dictionary
        with open(parameter_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        self.dist_config = config["simulation_parameters"]

        # Set parameters
        self.warm_up_period = warm_up_period
        self.data_collection_period = data_collection_period
        self.number_of_runs = number_of_runs
        self.audit_interval = audit_interval
        self.cores = cores

        # Set up logger
        self.logger = SimLogger(log_to_console=log_to_console,
                                log_to_file=log_to_file,
                                file_path=log_file_path)

    def check_param_validity(self):
        """
        Check the validity of the provided parameters.

        Validates all simulation parameters to ensure they meet requirements:
        - Warm-up period and data collection period must be >= 0
        - Number of runs and audit interval must be > 0
        - Arrival rates must be >= 0
        - Length of stay parameters must be >= 0
        - Routing probabilities must sum to 1 and be between 0 and 1

        Raises
        ------
        ValueError
            If any parameter fails validation with a descriptive error message.
        """
        # Validate parameters that must be >= 0
        for param in ["warm_up_period", "data_collection_period"]:
            self.validate_param(
                param, lambda x: x >= 0,
                "must be greater than or equal to 0")

        # Validate parameters that must be > 0
        for param in ["number_of_runs", "audit_interval"]:
            self.validate_param(
                param, lambda x: x > 0,
                "must be greater than 0")

    def validate_param(self, param_name, condition, error_msg):
        """
        Validate a single parameter against a condition.

        Parameters
        ----------
        param_name: str
            Name of the parameter being validated.
        condition: callable
            A function that returns True if the value is valid.
        error_msg: str
            Error message to display if validation fails.

        Raises
        ------
        ValueError:
            If the parameter fails the validation condition.
        """
        value = getattr(self, param_name)
        if not condition(value):
            raise ValueError(
                f"Parameter '{param_name}' {error_msg}, but is: {value}")
