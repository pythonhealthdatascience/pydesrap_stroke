<div align="center">

# Stroke capacity planning model: python DES RAP

[![python](https://img.shields.io/badge/-Python_3.13.1-blue?logo=python&logoColor=white)](https://www.python.org/)
![licence](https://img.shields.io/badge/Licence-MIT-green.svg?labelColor=gray)
[![Tests](https://github.com/pythonhealthdatascience/stroke_rap_python/actions/workflows/tests.yaml/badge.svg)](https://github.com/pythonhealthdatascience/stroke_rap_python/actions/workflows/tests.yaml)
[![Linting](https://github.com/pythonhealthdatascience/stroke_rap_python/actions/workflows/lint.yaml/badge.svg)](https://github.com/pythonhealthdatascience/stroke_rap_python/actions/workflows/lint.yaml)
[![ORCID: Heather](https://img.shields.io/badge/ORCID_Amy_Heather-0000--0002--6596--3479-brightgreen)](https://orcid.org/0000-0002-6596-3479)

</div>

This repository applies the [Python DES RAP Template](https://github.com/pythonhealthdatascience/rap_template_python_des) to a real-life example:

> Monks T, Worthington D, Allen M, Pitt M, Stein K, James MA. A modelling tool for capacity planning in acute and community stroke services. BMC Health Serv Res. 2016 Sep 29;16(1):530. doi: [10.1186/s12913-016-1789-4](https://doi.org/10.1186/s12913-016-1789-4). PMID: 27688152; PMCID: PMC5043535.

![](images/stroke_rehab_design.png)

<br>

## Installation

TBC

<!-- TODO: Provide instructions for installing dependencies and setting up the environment. -->

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

# Modified on of the arrival rates, some routing probabilities, and the
# number of replications
param = Param(
    asu_arrivals=ASUArrivals(tia=10),
    rehab_routing=RehabRouting(neuro_esd=0.2, neuro_other=0.8),
    number_of_runs=10
)
runner = Runner(param=param)
rep_results = runner.run_reps()
```

### Generating the figures from the article

The original study used Simul8. Each of the outputs from that article have been reproduced in this repository using Python, with some examples below. To generate these, simply execute `notebooks/analysis.ipynb`.

#### Examples

**Figure 1**

Original:

![](docs/article/fig1.png)

From this repository:

![](outputs/occupancy_freq_asu.png)

**Figure 3**

Original:

![](docs/article/fig3.png)

From this repository:

![](outputs/delay_prob_asu.png)

<br>

## Run time and machine specification

TBC

<!-- State the run time, and give the specification of the machine used (which achieved that run time).

**Example:** Intel Core i7-12700H with 32GB RAM running Ubuntu 24.04.1 Linux. 

To find this information:

* **Linux:** Run `neofetch` on the terminal and record your CPU, memory and operating system.
* **Windows:** Open "Task Manager" (Ctrl + Shift + Esc), go to the "Performance" tab, then select "CPU" and "Memory" for relevant information.
* **Mac:** Click the "Apple Menu", select "About This Mac", then window will display the details.-->

<br>

## Citation

For this applied example, please cite:

> Heather, A. (2025). Stroke capacity planning model: python DES RAP. GitHub. https://github.com/pythonhealthdatascience/stroke_rap_python.

This example is built using the [Python DES RAP Template](https://github.com/pythonhealthdatascience/rap_template_python_des). Please also cite the original template:

> Heather, A. Monks, T. (2025). Python DES RAP Template. Zenodo. https://doi.org/10.5281/zenodo.14622466. GitHub. https://github.com/pythonhealthdatascience/rap_template_python_des.

A `CITATION.cff` file is also provided.
