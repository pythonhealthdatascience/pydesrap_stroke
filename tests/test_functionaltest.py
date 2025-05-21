"""
Functional testing

Functional tests verify that the system or components perform their intended
functionality.
"""

from joblib import cpu_count
import numpy as np
import pandas as pd
import pytest

from simulation.parameters import (ASUArrivals, RehabArrivals, ASULOS,
                                   RehabLOS, Param)
from simulation.model import Model
from simulation.runner import Runner


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
                       stroke_mortality_mean=los,
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


def test_warmup_only():
    """
    Check that results are as expected if model is run with no data collection
    period, and only a warm-up period.

    Notes
    -----
    Inspired by `test_warmup_only` in
    github.com/pythonhealthdatascience/rap_template_python_des/.
    """
    # Run with warm-up period only
    param = Param(warm_up_period=500, data_collection_period=0)
    model = Model(param=param, run_number=0)
    model.run()

    # Check that there are no entries for patients or audit list
    assert len(model.patients) == 0
    assert len(model.audit_list) == 0

    # But that current occupancy is positive, as it reflects patients who
    # arrived during warm-up still occupying space
    assert model.asu_occupancy > 0
    assert model.rehab_occupancy > 0


def test_warmup_impact():
    """
    Check that running with warm-up leads to different results than without.

    Notes
    -----
    Adapted from `test_warmup_impact` in
    github.com/pythonhealthdatascience/rap_template_python_des/.
    """
    def helper_warmup(warm_up_period):
        """
        Helper function to run model with high arrivals and specified warm-up.

        Arguments:
            warm_up_period (float):
                Duration of the warm-up period - running simulation but not yet
                collecting results.
        """
        param = Param(warm_up_period=warm_up_period,
                      data_collection_period=1500)
        model = Model(param=param, run_number=0)
        model.run()
        return model

    # Run model with and without warm-up period
    model_warmup = helper_warmup(warm_up_period=500)
    model_none = helper_warmup(warm_up_period=0)

    # Extract result of first patient
    first_warmup = model_warmup.patients[0]
    first_none = model_none.patients[0]

    # Check that model with warm-up has arrival time later than warm-up length
    assert first_warmup.asu_arrival_time > 500, (
        "Expect first patient to arrive after time 500 when model is run " +
        f"with warm-up (length 500), but got {first_warmup.asu_arrival_time}."
    )

    # Check that model without warm-up has arrival first arrival after time 0
    assert first_none.asu_arrival_time > 0, (
        "Expect first patient to arrive after time 0 when model is run " +
        f"without warm-up, but got {first_none.asu_arrival_time}."
    )

    # Check that the first interval audit entry with no warm-up has occupancy
    # 0, but first entry with warm-up has occupancy > 0
    assert model_warmup.audit_list[0]["asu_occupancy"] > 0
    assert model_warmup.audit_list[0]["rehab_occupancy"] > 0
    assert model_none.audit_list[0]["asu_occupancy"] == 0
    assert model_none.audit_list[0]["rehab_occupancy"] == 0

    # Check time of first entry in the audit lists
    assert model_warmup.audit_list[0]["time"] == 500
    assert model_none.audit_list[0]["time"] == 0


def test_changing_occupancy():
    """
    Test that adjusting parameters alters the observed occupancy.

    Notes
    -----
    Inspired by `test_arrivals_decrease` in
    github.com/pythonhealthdatascience/rap_template_python_des/.
    """
    # Run model with lots of stroke arrivals (IAT 1) and fewer (IAT 100)
    initial_model = Model(Param(ASUArrivals(stroke=1)), run_number=0)
    initial_model.run()
    adj_model = Model(Param(ASUArrivals(stroke=100)), run_number=0)
    adj_model.run()

    # Check that patient list is longer with more arrivals
    i_n = len(initial_model.patients)
    a_n = len(adj_model.patients)
    assert i_n > a_n, (
        "Expect high IAT to have more patients than low IAT, but " +
        f"saw {i_n} for high and {a_n} for low"
    )

    # Check that sum of the audit occupancies is higher with more arrivals
    initial_audit = pd.DataFrame(initial_model.audit_list)
    adj_audit = pd.DataFrame(adj_model.audit_list)

    i_asu = initial_audit["asu_occupancy"].sum()
    a_asu = adj_audit["asu_occupancy"].sum()
    assert i_asu > a_asu, (
        "Expect high IAT to have higher ASU occupancy than low IAT, but " +
        f"saw {i_asu} for high and {a_asu} for low")

    i_reh = initial_audit["rehab_occupancy"].sum()
    a_reh = adj_audit["rehab_occupancy"].sum()
    assert i_reh > a_reh, (
        "Expect high IAT to have higher rehab occupancy than low IAT, but " +
        f"saw {i_reh} for high and {a_reh} for low")


def test_seed_stability():
    """
    Check that two runs using the same random seed return the same results.

    Notes
    -----
    Adapted from `seed_seed_stability` in
    github.com/pythonhealthdatascience/rap_template_python_des/.
    """
    # Run model twice, with same run number (and therefore same seed) each time
    runner1 = Runner(param=Param())
    result1 = runner1.run_single(run=33)
    runner2 = Runner(param=Param())
    result2 = runner2.run_single(run=33)

    # Check that the dataframes are equal
    pd.testing.assert_frame_equal(result1["asu"], result2["asu"])
    pd.testing.assert_frame_equal(result1["rehab"], result2["rehab"])


def test_parallel():
    """
    Check that sequential and parallel execution produce consistent results.

    Notes
    -----
    Adapted from `test_parallel` in
    github.com/pythonhealthdatascience/rap_template_python_des/.
    """
    # Sequential (1 core) and parallel (-1 cores) execution
    results = {}
    for mode, cores in [("seq", 1), ("par", -1)]:
        param = Param(cores=cores)
        runner = Runner(param)
        results[mode] = runner.run_single(run=0)

    # Verify results are identical
    pd.testing.assert_frame_equal(results["seq"]["asu"],
                                  results["par"]["asu"])
    pd.testing.assert_frame_equal(results["seq"]["rehab"],
                                  results["par"]["rehab"])


@pytest.mark.parametrize("cores", [
    (-2), (0), (cpu_count()), (cpu_count()+1)
])
def test_valid_cores(cores):
    """
    Check there is error handling for input of invalid number of cores.

    Notes
    -----
    Copied from github.com/pythonhealthdatascience/rap_template_python_des/.
    """
    param = Param(cores=cores)
    runner = Runner(param)
    with pytest.raises(ValueError):
        runner.run_reps()


def test_sampled_distributions():
    """
    Ensure that the mean of sampled values from arrival_dist, los_dist, and
    routing_dist are close to their expected values.

    Notes
    -----
    Adapted from `test_sampled_times` in
    github.com/pythonhealthdatascience/rap_template_python_des/.
    """
    param = Param()
    model = Model(param, run_number=0)

    # Test arrival_dist
    for unit in ['asu', 'rehab']:
        for patient_type, dist in model.arrival_dist[unit].items():
            samples = [dist.sample() for _ in range(10000)]
            observed_mean = np.mean(samples)
            expected_mean = getattr(
                getattr(param, f"{unit}_arrivals"), patient_type)
            assert np.isclose(observed_mean, expected_mean, rtol=0.05), (
                f"Expected mean arrival time for {unit} {patient_type} ≈ "
                f"{expected_mean}, but got {observed_mean}.")

    # Test los_dist
    for unit in ['asu', 'rehab']:
        for patient_type, dist in model.los_dist[unit].items():
            samples = [dist.sample() for _ in range(10000)]
            observed_mean = np.mean(samples)
            expected_mean = getattr(
                getattr(param, f"{unit}_los"), patient_type)["mean"]
            assert np.isclose(observed_mean, expected_mean, rtol=0.05), (
                f"Expected mean LOS for {unit} {patient_type} ≈ "
                f"{expected_mean}, but got {observed_mean}.")

    # Test routing_dist
    for unit in ['asu', 'rehab']:
        for patient_type, dist in model.routing_dist[unit].items():
            samples = [dist.sample() for _ in range(10000)]
            observed_probs = {dest: samples.count(dest) / len(samples)
                              for dest in set(samples)}
            expected_probs = getattr(
                getattr(param, f"{unit}_routing"), patient_type)
            for dest in expected_probs:
                # If a destination has a very low probability, it might not
                # appear in samples. In that case, set the observed probability
                # to 0
                observed_prob = observed_probs.get(dest, 0)
                assert np.isclose(observed_prob,
                                  expected_probs[dest], atol=0.05), (
                    f"Expected routing probability for {unit} {patient_type} "
                    f"to {dest} ≈ {expected_probs[dest]}, but got "
                    f"{observed_prob}.")
