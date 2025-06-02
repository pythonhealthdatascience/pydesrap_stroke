<div align="center">

# Stroke capacity planning model: python DES RAP

[![python](https://img.shields.io/badge/-Python_3.13.1-blue?logo=python&logoColor=white)](https://www.python.org/)
![licence](https://img.shields.io/badge/🛡️_Licence-MIT-green.svg?labelColor=gray)
[![Tests](https://github.com/pythonhealthdatascience/stroke_rap_python/actions/workflows/tests.yaml/badge.svg)](https://github.com/pythonhealthdatascience/stroke_rap_python/actions/workflows/tests.yaml)
[![Linting](https://github.com/pythonhealthdatascience/stroke_rap_python/actions/workflows/lint.yaml/badge.svg)](https://github.com/pythonhealthdatascience/stroke_rap_python/actions/workflows/lint.yaml)
[![ORCID](https://img.shields.io/badge/ORCID_Amy_Heather-0000--0002--6596--3479-A6CE39?&logo=orcid&logoColor=white)](https://orcid.org/0000-0002-6596-3479)

</div>

This repository applies the [Python DES RAP Template](https://github.com/pythonhealthdatascience/rap_template_python_des) to a real-life example:

> Monks T, Worthington D, Allen M, Pitt M, Stein K, James MA. A modelling tool for capacity planning in acute and community stroke services. BMC Health Serv Res. 2016 Sep 29;16(1):530. doi: [10.1186/s12913-016-1789-4](https://doi.org/10.1186/s12913-016-1789-4). PMID: 27688152; PMCID: PMC5043535.

Model diagram:

![](images/stroke_rehab_design.png)

<br>

## Installation

Clone the repository locally:

```
git clone https://github.com/pythonhealthdatascience/stroke_rap_python.git
cd stroke_rap_python
```

Use the provided `environment.yaml` file to set up a Python environment with `conda`:

```
conda env create --file environment.yaml
conda activate
```

The provided `environment.yaml` file is a snapshot of the environment used when creating the repository, including specific package versions. You can update this file if necessary, but be sure to test that everything continues to work as expected after any updates. Also note that some dependencies are not required for modelling, but instead served other purposes, like running `.ipynb` files and linting.

As an alternative, a `requirements.txt` file is provided which can be used to set up the environment with `virtualenv`. This is used by GitHub actions, which run much faster with a virtual environment than a conda environment. However, we recommend locally installing the environment using conda, as it will also manage the Python version for you. If using `virtualenv`, it won't fetch a specific version of Python - so please note the version listed in `environment.yaml`.

<br>

## How to run

The simulation code is provided as a **package** within `simulation/`. There are notebooks executing the model and analysing the results in `notebooks/`.

To run the model with base parameters once or with replications:

```
from simulation.parameters import Param
from simulation.runner import Runner

param = Param()
runner = Runner(param=param)

single_result = runner.run_single(run=0)
rep_results = runner.run_reps()
```

Example altering the model parameters:

```
from simulation.parameters import Param, ASUArrivals, RehabRouting
from simulation.runner import Runner

# Modified one of the arrival rates, some routing probabilities, and the
# number of replications
param = Param(
    asu_arrivals=ASUArrivals(tia=10),
    rehab_routing=RehabRouting(neuro_esd=0.2, neuro_other=0.8),
    number_of_runs=10
)
runner = Runner(param=param)
rep_results = runner.run_reps()
```

### Generating the results from the article

The original study used Simul8. Each of the outputs from that article have been replicated in this repository using Python:

* Figure 1. Simulation probability density function for occupancy of an acute stroke unit.
* Figure 3. Simulated trade-off between the probability that a patient is delayed and the no. of acute beds available.
* Table 2. Likelihood of delay. Current admissions versus 5% more admissions.
* Table 3. Results of pooling of acute and rehab beds.
* Supplementary Table 1. Likelihood of delay. Current admissions versus No Complex neurological patients.
* Supplementary Table 3. Likelihood of delay. Current admissions versus ring fenced acute stroke beds.

To generate these, simply execute `notebooks/analysis.ipynb`.

#### Examples

**Figure 1**

Original:

![](docs/article/fig1.png)

From this repository:

![](outputs/figure1_asu.png)

**Figure 3**

Original:

![](docs/article/fig3.png)

From this repository:

![](outputs/figure3_asu.png)

<br>

## Run time and machine specification

The run time for this analysis (`notebooks/analysis.ipynb`) is 10 seconds. This was on an Intel Core i7-12700H, 32GB RAM, Ubuntu 24.04.1.

The other notebooks generate results for tests and illustrate other functionality (e.g. importing parameters from csv, running with logs), and these just take a second or two.

<br>

## Citation

For this applied example, please cite:

> Heather, A. (2025). Stroke capacity planning model: python DES RAP. GitHub. https://github.com/pythonhealthdatascience/stroke_rap_python.

This example is built using the [Python DES RAP Template](https://github.com/pythonhealthdatascience/rap_template_python_des). Please also cite the original template:

> Heather, A. Monks, T. (2025). Python DES RAP Template. Zenodo. https://doi.org/10.5281/zenodo.14622466. GitHub. https://github.com/pythonhealthdatascience/rap_template_python_des.

A `CITATION.cff` file is also provided.
