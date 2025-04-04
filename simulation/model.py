"""
Code for the simulation.
"""

import numpy as np
import simpy
from sim_tools.distributions import Exponential


class Patient:
    """
    Represents a patient.

    Attributes
    ----------
    patient_id: int, float or str
        Unique patient identifier.
    patient_type: str
        Patient type ("stroke", "tia", "neuro" or "other").
    arrival_time: float
        Arrival time for the patient (in days).
    """
    def __init__(self, patient_id, patient_type):
        """
        Parameters
        ----------
        patient_id: int, float or str
            Unique patient identifier.
        patient_type: str
            Patient type ("stroke", "tia", "neuro" or "other").
        """
        self.patient_id = patient_id
        self.patient_type = patient_type
        self.arrival_time = np.nan


class Model:
    """
    Simulation model.

    Attributes
    ----------
    param: Param
        Run parameters.
    run_number: int
        Replication / run number.
    env: simpy.Environment
        Simulation environment.
    patients: list
        Stores the Patient objects.
    distributions: dictionary
        Contains the sampling distributions.
    """
    def __init__(self, param, run_number):
        """
        Parameters
        ----------
        param: Param
            Run parameters.
        run_number: int
            Replication / run number.
        """
        # Set parameters
        self.param = param
        self.run_number = run_number

        # Create SimPy environment
        self.env = simpy.Environment()

        # Create attributes to store results
        # The patients list will store a reference to the patient objects, so
        # any updates to the patient attributes after they are saved to the
        # list, will be reflected in the list as well
        self.patients = []

        # Create seeds
        ss = np.random.SeedSequence(entropy=self.run_number)
        seed_generator = iter(ss.spawn(20))

        # Create distributions
        self.create_distributions(seed_generator)

    def create_distributions(self, seed_generator):
        """
        Creates distributions for sampling arrivals for all units and patient
        types.

        Parameters
        ----------
        seed_generator: Iterator
            Iterator that generates random seeds.
        """
        # Create dictionary to store distributions
        self.distributions = {}

        # Loop through each unit
        for unit, unit_param in [("asu", self.param.asu_arrivals),
                                 ("rehab", self.param.rehab_arrivals)]:

            # Make sub-dictionary to store that unit's distributions
            self.distributions[unit] = {}

            # Get a list of the patients in that unit (ignore other attributes)
            patient_types = [attr for attr in dir(unit_param) if attr in
                             ["stroke", "tia", "neuro", "other"]]

            for patient_type in patient_types:

                # Create distributions for each patient type in that unti
                self.distributions[unit][patient_type] = Exponential(
                    mean=getattr(unit_param, patient_type),
                    random_seed=next(seed_generator)
                )

    def patient_generator(self, patient_type, distribution, unit):
        """
        Generic patient generator for any patient type and unit.

        Parameters
        ----------
        patient_type: str
            Type of patient ("stroke", "tia", "neuro", "other").
        distribution: Distribution
            The inter-arrival time distribution to sample from.
        unit: str
            The unit the patient is arriving at ("asu", "rehab").
        """
        while True:
            # Sample and pass time to arrival
            sampled_iat = distribution.sample()
            yield self.env.timeout(sampled_iat)

            # Create a new patient
            p = Patient(
                patient_id=len(self.patients)+1,
                patient_type=patient_type
            )

            # Record arrival time
            p.arrival_time = self.env.now

            # Print arrival time
            print(f"{patient_type} patient arrive at {unit}: {p.arrival_time}")

            # Add to the patients list
            self.patients.append(p)

    def run(self):
        """
        Run the simulation.
        """
        # Calculate the total run length
        run_length = (self.param.warm_up_period +
                      self.param.data_collection_period)

        # Schedule patient generators to run during the simulation
        for unit, patient_types in self.distributions.items():
            for patient_type, distribution in patient_types.items():
                self.env.process(
                    self.patient_generator(
                        patient_type=patient_type,
                        distribution=distribution,
                        unit=unit
                    )
                )

        # Run the simulation
        self.env.run(until=run_length)
