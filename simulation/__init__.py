"""
SimPy Discrete-Event Simulation (DES) Model.
"""

__version__ = "1.0.0"


# This section allows us to import using e.g. `from simulation import Model`,
# rather than `from simulation.model import Model`.

from .lockeddict import LockedDict
from .logging import SimLogger
from .model import Model
from .parameters import Param
from .patient import Patient
from .restrictattributes import RestrictAttributes, RestrictAttributesMeta
from .runner import Runner

__all__ = [
    "LockedDict",
    "SimLogger",
    "Model",
    "Param",
    "Patient",
    "RestrictAttributes",
    "RestrictAttributesMeta",
    "Runner"
]
