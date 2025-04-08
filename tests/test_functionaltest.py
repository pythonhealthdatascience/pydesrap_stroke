"""
Functional testing

Functional tests verify that the system or components perform their intended
functionality.
"""

import pytest

from simulation.parameters import (ASUArrivals, RehabArrivals, ASULOS,
                                   RehabLOS, Param)
from simulation.model import Model


@pytest.mark.parametrize("warm_up_period", [(0), (1)])
def test_audit_length(warm_up_period):
    """
    Given that we set an audit interval of 1, and that first audit is performed
    at time 0, check that the length of the audit list matches the simulation
    time (with no warm-up). Also, check that this is suitably reduced when a
    warm-up period is implemented.

    Parameters
    ----------
    warm_up_period: float
        Length of the warm-up period in days.

    Notes
    -----
    Inspired by `results_collection_test1`, `results_collection_test2` and
    `test_warm_up` in github.com/pythonhealthdatascience/llm_simpy/.
    """
    # Run the model
    param = Param(warm_up_period=warm_up_period,
                  data_collection_period=10)
    model = Model(param=param, run_number=0)
    model.run()

    # Check the length of the audit list
    if warm_up_period == 0:
        # Should have audits for timepoints 0 to 9 (so length of 10)
        assert len(model.audit_list) == model.env.now == 10
    elif warm_up_period == 1:
        # With warm-up = 1, should have audits for timepoints 2 to 10 (so
        # length of 9), as it is wiped at timepoint 1, so drop 0 and 1, but ran
        # for one longer, so goes up to 10
        assert len(model.audit_list) == model.env.now - warm_up_period - 1 == 9


def test_high_iat():
    """
    Extreme value test, setting a very high inter-arrival time for all
    patients, and so we expect no arrivals.

    Notes
    -----
    Inspired by `ev_test_2` from github.com/pythonhealthdatascience/llm_simpy/.
    """
    # Set high inter-arrival time for all patient types
    iat = 10_000_000
    param = Param(
        asu_arrivals=ASUArrivals(stroke=iat, tia=iat, neuro=iat, other=iat),
        rehab_arrivals=RehabArrivals(stroke=iat, neuro=iat, other=iat))

    # Run the model
    model = Model(param=param, run_number=0)
    model.run()

    # Check that there are no arrivals
    assert len(model.patients) == 0

    # Check that the units are empty
    assert model.asu_occupancy == 0
    assert model.rehab_occupancy == 0


@pytest.mark.parametrize("stroke_no_esd_mean", [(10_000_000), (5)])
def test_long_los(stroke_no_esd_mean):
    """
    Extreme value test, setting a very long length of stay for:
    1. All patients -> expect no patients to depart the model.
    2. All except one type -> expect only those to depart the model (crudely
    checked by seeing if occupancy is less than total arrivals).

    Notes
    -----
    Inspired by `ev_test_3` and `test_ev_4` from
    github.com/pythonhealthdatascience/llm_simpy/.
    """
    # Set high length of stay for all patient types except stroke_no_esd_mean.
    # Also, no warm-up period, otherwise arrivals != occupancy (as arrivals
    # excludes warm-up, but occupancy does not, if they are still present).
    los = 10_000_000
    param = Param(
        asu_los=ASULOS(stroke_no_esd_mean=stroke_no_esd_mean,
                       stroke_esd_mean=los,
                       tia_mean=los,
                       neuro_mean=los,
                       other_mean=los),
        rehab_los=RehabLOS(stroke_no_esd_mean=stroke_no_esd_mean,
                           stroke_esd_mean=los,
                           tia_mean=los,
                           neuro_mean=los,
                           other_mean=los),
        warm_up_period=0)

    # Run the model
    model = Model(param=param, run_number=0)
    model.run()

    # Check that the total arrivals is equal to or less than total occupancy
    total_occupancy = model.asu_occupancy + model.rehab_occupancy
    if stroke_no_esd_mean == 10_000_000:
        assert len(model.patients) == total_occupancy
    elif stroke_no_esd_mean == 5:
        assert len(model.patients) > total_occupancy


# TODO: test_ev_5/6/7/8 - requires patient counts by unit and patient type
