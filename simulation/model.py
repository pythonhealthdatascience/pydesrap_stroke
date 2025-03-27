"""
Discrete Event Simulation Model.
"""

from dataclasses import dataclass


@dataclass
class ASUArrivals:
    """Acute stroke unit arrivals."""
    stroke = 1.2
    tia = 9.3
    neuro = 3.6
    other = 3.2


@dataclass
class RehabArrivals:
    """Rehab arrivals."""
    stroke = 21.8
    neuro = 31.7
    other = 28.6


@dataclass
class ASULOS:
    """Acute stroke unit length of stay."""
    stroke_no_esd_mean = 7.4
    stroke_no_esd_sd = 8.61
    stroke_esd_mean = 4.6
    stroke_esd_sd = 4.8
    tia_mean = 1.8
    tia_sd = 2.3
    neuro_mean = 4.0
    neuro_sd = 5.0
    other_mean = 3.8
    other_sd = 5.2


@dataclass
class RehabLOS:
    """Rehab length of stay."""
    rehab_los_stroke_no_esd_mean = 28.4
    rehab_los_stroke_no_esd_sd = 27.2
    rehab_los_stroke_esd_mean = 30.3
    rehab_los_stroke_esd_sd = 23.1
    rehab_los_tia_mean = 18.7
    rehab_los_tia_sd = 23.5
    rehab_los_neuro_mean = 27.6
    rehab_los_neuro_sd = 28.4
    rehab_los_other_mean = 16.1
    rehab_los_other_sd = 14.1


@dataclass
class ASURouting:
    """Routing out of the acute stroke unit."""
    rehab_stroke = 0.24
    rehab_tia = 0.01
    rehab_neuro = 0.11
    rehab_other = 0.05
    esd_stroke = 0.13
    esd_tia = 0.01
    esd_neuro = 0.05
    esd_other = 0.10
    other_stroke = 0.63
    other_tia = 0.98
    other_neuro = 0.84
    other_other = 0.85


@dataclass
class RehabRouting:
    """Routing out of rehab."""
    rehab_to_esd_stroke = 0.40
    rehab_to_esd_tia = 0
    rehab_to_esd_neuro = 0.09
    rehab_to_esd_other = 0.13
    rehab_to_other_stroke = 0.60
    rehab_to_other_tia = 1
    rehab_to_neuro = 0.91
    rehab_to_other = 0.88


@dataclass
class Param:
    """Default parameters for simulation."""
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        asu_arrivals=ASUArrivals(),
        rehab_arrivals=RehabArrivals(),
        asu_los=ASULOS(),
        rehab_los=RehabLOS(),
        asu_routing=ASURouting(),
        rehab_routing=RehabRouting()
    ):
        """Initialise instance of the parameter class."""
        self.asu_arrivals = asu_arrivals
        self.rehab_arrivals = rehab_arrivals
        self.asu_los = asu_los
        self.rehab_los = rehab_los
        self.asu_routing = asu_routing
        self.rehab_routing = rehab_routing
