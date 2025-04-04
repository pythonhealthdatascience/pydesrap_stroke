"""
Code for the simulation.
"""

import numpy as np
import simpy
from sim_tools.distributions import Exponential, Discrete, Lognormal


class Patient:
    """
    Represents a patient.

    Attributes
    ----------
    patient_id: int, float or str
        Unique patient identifier.
    patient_type: str
        Patient type ("stroke", "tia", "neuro" or "other").
    asu_arrival_time: float
        Arrival time at the acute stroke unit (ASU) for the patient (in days).
    post_asu_destination: str
        Destination after the ASU ("rehab", "esd", "other").
    routing_patient_type: str
        Routing patient type ("stroke_esd", "stroke_noesd", "tia", "neuro" or
        "other").
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
        self.asu_arrival_time = np.nan
        self.post_asu_destination = np.nan
        self.routing_patient_type = np.nan


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
        self.seed_generator = iter(ss.spawn(30))

        # Create arrival distributions
        self.arrival_dist = self.create_distributions(
            asu_param=self.param.asu_arrivals,
            rehab_param=self.param.rehab_arrivals,
            distribution_type="exponential")

        # Create routing sampling distributions
        self.routing_dist = self.create_distributions(
            asu_param=self.param.asu_routing,
            rehab_param=self.param.rehab_routing,
            distribution_type="discrete")

        # Create length of stay (LOS) sampling distributions
        self.los_dist = self.create_distributions(
            asu_param=self.param.asu_los,
            rehab_param=self.param.rehab_los,
            distribution_type="lognormal")

    def create_distributions(self, asu_param, rehab_param, distribution_type):
        """
        Create a nested dictionary with two items: "asu" and "rehab". Each
        then contains a set of distributions by patient type.

        Parameters
        ----------
        asu_param: Class
            Acute stroke unit (ASU) parameters.
        rehab_param: Class
            Rehabilitation unit parameters.
        distribution_type: str
            Name of the distribution to use ("exponential", "discrete",
            "lognormal").
        """
        # Create dictionary to store distributions
        distributions = {}

        # Loop through each unit
        for unit, unit_param in [("asu", asu_param), ("rehab", rehab_param)]:

            # Make sub-dictionary to store that unit's distributions
            distributions[unit] = {}

            # Get a list of the patients in that unit (ignore other attributes)
            patient_types = [attr for attr in dir(unit_param) if attr in
                             ["stroke", "stroke_esd", "stroke_noesd",
                              "tia", "neuro", "other"]]

            # For each patient type...
            for patient_type in patient_types:

                # Get the entry for that patient
                patient_param = getattr(unit_param, patient_type)

                # Create distributions of specified type
                if distribution_type == "exponential":
                    distributions[unit][patient_type] = Exponential(
                        mean=patient_param,
                        random_seed=next(self.seed_generator)
                    )
                elif distribution_type == "discrete":
                    distributions[unit][patient_type] = Discrete(
                        values=list(patient_param.keys()),
                        freq=list(patient_param.values()),
                        random_seed=next(self.seed_generator)
                    )
                elif distribution_type == "lognormal":
                    distributions[unit][patient_type] = Lognormal(
                        mean=patient_param["mean"],
                        stdev=patient_param["sd"],
                        random_seed=next(self.seed_generator)
                    )
        return distributions

    def patient_generator(self, patient_type, unit):
        """
        Generic patient generator for any patient type and unit.

        Parameters
        ----------
        patient_type: str
            Type of patient ("stroke", "tia", "neuro", "other").
        unit: str
            The unit the patient is arriving at ("asu", "rehab").
        """
        while True:
            # Sample and pass time to arrival
            sampled_iat = self.arrival_dist[unit][patient_type].sample()
            yield self.env.timeout(sampled_iat)

            # Create a new patient and add to the patients list
            p = Patient(patient_id=len(self.patients)+1,
                        patient_type=patient_type)
            self.patients.append(p)

            # Record and print arrival time
            p.asu_arrival_time = self.env.now
            print(f"{patient_type} patient arrive at {unit}: " +
                  f"{p.asu_arrival_time}.")

            # Sample destination after ASU (we do this immediately on arrival
            # in the ASU, as the destination influences the length of stay)
            if unit == "asu":
                p.post_asu_destination = (
                    self.routing_dist["asu"][p.patient_type].sample())

                # If it is a stroke patient on the ASU, find out if they are
                # going to the ESD (stroke_esd) or not (stroke_noesd)
                if p.patient_type == "stroke":
                    if p.post_asu_destination == "esd":
                        p.routing_patient_type = "stroke_esd"
                    else:
                        p.routing_patient_type = "stroke_noesd"
                else:
                    p.routing_patient_type = p.patient_type

    def run(self):
        """
        Run the simulation.
        """
        # Calculate the total run length
        run_length = (self.param.warm_up_period +
                      self.param.data_collection_period)

        # Schedule patient generators to run during the simulation
        # For each unit...
        for unit, patient_types in self.arrival_dist.items():
            # For each patient...
            for patient_type, _ in patient_types.items():
                self.env.process(
                    self.patient_generator(
                        patient_type=patient_type,
                        unit=unit
                    )
                )

        # Run the simulation
        self.env.run(until=run_length)
