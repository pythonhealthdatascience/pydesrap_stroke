"""
Back Testing

Back tests check that the model code produces results consistent with those
generated historically/from prior code.
"""

from pathlib import Path
import pandas as pd
import pytest

from simulation import Model, Param, Runner


def test_model():
    """
    Compare audit_list from Model to one generated previously.

    Notes
    -----
    This is adapted from `test_reproduction` in
    github.com/pythonhealthdatascience/pydesrap_mms.
    """
    # Run model and get audit list as a dataframe
    model = Model(param=Param(), run_number=0)
    model.run()
    audit_list = pd.DataFrame(model.audit_list)

    # Import expected result
    exp_audit_list = pd.read_csv(
        Path(__file__).parent.joinpath("exp_results/audit_list.csv"))

    # Compare the generated and expected results
    pd.testing.assert_frame_equal(audit_list, exp_audit_list)


@pytest.mark.parametrize("unit", [("asu"), ("rehab")])
def test_runner(unit):
    """
    Compare the occupancy dataframes from Runner to those generated before.

    Parameters
    ----------
    unit: str
        Unit to assess results from ("asu", "rehab")

    Notes
    -----
    This is adapted from `test_reproduction` in
    github.com/pythonhealthdatascience/pydesrap_mms.
    """
    # Run model and get occupancy dataframe
    runner = Runner(param=Param())
    occupancy = runner.run_single(run=0)[unit]

    # Import expected result
    exp_occupancy = pd.read_csv(
        Path(__file__).parent.joinpath(f"exp_results/{unit}_occupancy.csv"))

    # Compare the generated and expected results
    pd.testing.assert_frame_equal(occupancy, exp_occupancy)
