"""
Defines the Patient class for representing individuals in the simulation.
"""

import numpy as np


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
        Arrival time at the acute stroke unit (ASU) in days.
    post_asu_destination: str
        Destination after the ASU ("rehab", "esd", "other").
    asu_los: float
        Length of stay on the ASU in days.
    rehab_arrival_time: float
        Arrival time at the rehabilitation unit in days.
    post_rehab_destination: str
        Destination after rehab ("esd", "other").
    rehab_los: float
        Length of stay on the rehabilitation unit in days.
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
        self.asu_los = np.nan
        self.rehab_arrival_time = np.nan
        self.post_rehab_destination = np.nan
        self.rehab_los = np.nan
