# Log

## Set-up

Created repository from Python DES RAP Template v1.2.0

Created `docs/log.md` to keep a record of all changes necessary to adapt the template.

Used the template at the end of a README to make a first draft README.

Emptied `docs/heather_2025.md`, `docs/nhs_rap.md` and `CHANGELOG.md`.

Deleted `docs/hsma_changes.md` and `inputs/`.

Redid `CITATION.cff`.

Left `LICENSE` as is (but others would need to change).

Used [llm_simpy/notebooks/03_stroke/00_stress/](https://github.com/pythonhealthdatascience/llm_simpy/tree/main/notebooks/03_stroke/00_stress) to fill out `docs/stress_des.md`.

Renamed and created environment.

> 💡 **Reflections...**
>
> * Could encourage / suggestion Allyon 2021 [Keeping modelling notebooks with TRACE: Good for you and good for environmental research and management support](https://www.sciencedirect.com/science/article/pii/S1364815220309890).
> * Template README could have space for orcid.
> * Would have been handy for template README to give an example of giving credit to template.
> * Should template README just be a seperate file? But then would have to rename, so maybe, fine as is.
> * Empty versions of docs/ and changelog would have been handy.

## Parameters

### Structuring the parameter class

Focused just on `model.py`. I made an empty .py file, then looked at them side-by-side.

I started with my model parameters, and filling a class with all the base parameters.

But this seemed very clunky, with lots of parameters, and figured I ought to find a better way of doing it...

```
class Param:
    """
    Default parameters for simulation.
    """
    def __init__(
        self,
        # Acute stroke unit arrivals
        asu_arrive_stroke=1.2,
        asu_arrive_tia=9.3,
        asu_arrive_neuro=3.6,
        asu_arrive_other=3.2,
        # Rehab arrivals
        rehab_arrive_stroke=21.8,
        rehab_arrive_neuro=31.7,
        rehab_arrive_other=28.6,
        # Acute stroke unit length of stay
        asu_los_stroke_no_esd_mean=7.4,
        asu_los_stroke_no_esd_sd=8.61,
        asu_los_stroke_esd_mean=4.6,
        asu_los_stroke_esd_sd=4.8,
        asu_los_tia_mean=1.8,
        asu_los_tia_sd=2.3,
        asu_los_neuro_mean=4.0,
        asu_los_neuro_sd=5.0,
        asu_los_other_mean=3.8,
        asu_los_other_sd=5.2,
        # Rehab length of stay
        rehab_los_stroke_no_esd_mean=28.4,
        rehab_los_stroke_no_esd_sd=27.2,
        rehab_los_stroke_esd_mean=30.3,
        rehab_los_stroke_esd_sd=23.1,
        rehab_los_tia_mean=18.7,
        rehab_los_tia_sd=23.5,
        rehab_los_neuro_mean=27.6,
        rehab_los_neuro_sd=28.4,
        rehab_los_other_mean=16.1,
        rehab_los_other_sd=14.1,
        # Routing out of the acute stroke unit
        asu_to_rehab_stroke=0.24,
        asu_to_rehab_tia=0.01,
        asu_to_rehab_neuro=0.11,
        asu_to_rehab_other=0.05,
        asu_to_esd_stroke=0.13,
        asu_to_esd_tia=0.01,
        asu_to_esd_neuro=0.05,
        asu_to_esd_other=0.10,
        asu_to_other_stroke=0.63,
        asu_to_other_tia=0.98,
        asu_to_other_neuro=0.84,
        asu_to_other_other=0.85,
        # Routing out of rehab
        rehab_to_esd_stroke=0.40,
        rehab_to_esd_tia=0,
        rehab_to_esd_neuro=0.09,
        rehab_to_esd_other=0.13,
        rehab_to_other_stroke=0.60,
        rehab_to_other_tia=1,
        rehab_to_neuro=0.91,
        rehab_to_other=0.88
    ):
        """
        Initialise instance of the parameter class.
        """
        self.asu_arrive_stroke = asu_arrive_stroke
        self.asu_arrive_tia = asu_arrive_tia
        self.asu_arrive_neuro = asu_arrive_neuro
        self.asu_arrive_other = asu_arrive_other
        self.rehab_arrive_stroke = rehab_arrive_stroke
        self.rehab_arrive_neuro = rehab_arrive_neuro
        self.rehab_arrive_other = rehab_arrive_other
        self.asu_los_stroke_no_esd_mean = asu_los_stroke_no_esd_mean
        self.asu_los_stroke_no_esd_sd = asu_los_stroke_no_esd_sd
        self.asu_los_stroke_esd_mean = asu_los_stroke_esd_mean
        self.asu_los_stroke_esd_sd = asu_los_stroke_esd_sd
        self.asu_los_tia_mean = asu_los_tia_mean
        self.asu_los_tia_sd = asu_los_tia_sd
        self.asu_los_neuro_mean = asu_los_neuro_mean
        self.asu_los_neuro_sd = asu_los_neuro_sd
        self.asu_los_other_mean = asu_los_other_mean
        self.asu_los_other_sd = asu_los_other_sd
        self.rehab_los_stroke_no_esd_mean = rehab_los_stroke_no_esd_mean
        self.rehab_los_stroke_no_esd_sd = rehab_los_stroke_no_esd_sd
        self.rehab_los_stroke_esd_mean = rehab_los_stroke_esd_mean
        self.rehab_los_stroke_esd_sd = rehab_los_stroke_esd_sd
        self.rehab_los_tia_mean = rehab_los_tia_mean
        self.rehab_los_tia_sd = rehab_los_tia_sd
        self.rehab_los_neuro_mean = rehab_los_neuro_mean
        self.rehab_los_neuro_sd = rehab_los_neuro_sd
        self.rehab_los_other_mean = rehab_los_other_mean
        self.rehab_los_other_sd = rehab_los_other_sd
        # etc...
```

Using a single line instead of assigning each parameter individually...

```
vars(self).update(locals())
```

Using classes when populating the classes, and storing groups of parameters in dictionaries, i.e.:

```
@dataclass
class ASUArrivalRates:
    stroke=1.2
    tia=9.3
    neuro=3.6
    other=3.2

@dataclass
class RehabArrivalRates:
    stroke=21.8
    neuro=31.7
    other=28.6

class Param:
    def __init__(
        asu_arrivals=ASUArrivalRates(),
        rehab_arrivals=RehabArrivalRates(),
        ...
    )
```

Importance of ArrivalRates() class is that it aids people in altering the default parameters - for example, to just change the stroke arrival rate,...

```
Param(asu_arrivals = ASUArrivalRates(stroke=3))
```

Also, we could import these values from a file as well? For now though, will stick with defining in the code.

Then I ran pylint, and add pylint disablers for too many arguments.

> 💡Handy to consider this way of structuring, for models with lots of parameters (which can be fairly common).

## Clearing out

I removed most files... it was overwhelming and tricky to work with, if I am changing and breaking things, and that breaks all my tests, and so on.

> 💡 I realise the templates are a little daunting - and I wrote them! Getting started with this, I did the strategy of essentially "clearing things away" - and then referring back to them as I got set up again. Perhaps a more useable / accessible version of these templates would be structuring them as step-by-step quarto books. Because that"s essentially how am I treating them - AND that is how I learnt best, when I was learning DES, is working through step-by-step with the HSMA book, building it up. So these templates are me having worked out how to implement everything we want - and then the applied examples is stress testing / real life testing, figuring out how we work through, where we make changes - and using all that then to write step-by-step tutorial books. One for Python, one for R. Step-by-step walkthough of RAP DES in XYZ.

## Back to parameters

### Refactoring

With so many parameters, I feel like it maybe makes sense to seperate out the code more than I did in the template, so have changed from `model.py` to `parameters.py`

> 💡 Could the location of functions in the template do with reorganising? What is clearest?

### Playing with them

I wanted to try out using the classes to make sure they work. I created a disposable notebook to play around with them in.

> 💡 Should be clear how we do this early on, so can play about with it.

I realised dataclasses don"t allow you to call ASUArrivals(stroke=4), as they are recognised as attributes, but only recognised as parameters when you type hint ie.

```
@dataclass
class ASUArrivals:
    stroke: float = 1.2
    tia: float = 9.3
    neuro: float = 3.6
    other: float = 3.2

ASUArrivals(stroke=4)
```

I don"t want this weird/hidden-feeling behaviour, especially as people say type hints shouldn"t functionally affect your code in Python, and so will stick with normal classes.

### Preventing addition of new attributes

From writing the templates, I know how important it is that we prevent the addition of new attributes.

In python, I do this using a method in the parameter class. This is also possible in R if set up as a R6Class, but I chose to use a function for simplicity, so that instead checks the parameters when they are input to model. The downside of that approach as it will check every time the model is called (i.e. with each replication).

However, an alternative would be for my parameter classes to **inherit** from a main class with that functionality.

> 💡 Emphasise the importance of this, that it"s not just something to drop.

> 💡 When using the dataclasses, our provided method for preventing the addition of new attributes no longer works.

I set up the **parent class**, and then add **tests** which check this is functioning properly.

## Distributions

The next logical step seemed to be to make **classes for each of the distributions** we planned to use, and then, to add **tests** for each of these.

Decided to switch to simpler method of just importing `sim-tools`, and I add some extra tests for them to Tom"s sim-tools repository, removing those tests from this repository.

> 💡 Mention that you can import sim-tools or copy over functions as it"s MIT licensed, just need to give appropriate credit. Mention that can add own tests.

Relatedly, will switch to use **NumPy style docstrings** and **double quotes** to be consistent with the rest of Tom"s prior code-base (also HSMA use double quotes - though not any docstrings). Had chosen google before as prefer the appearance but, on reflection, it would be better to be consistent.

## Patient generators

The next step figures to be just setting up the basic model logic, starting with patient generators.

We have patients arriving from four different sources, each with their own different inter-arrival time, so we need generator functions for each patient type.

I add a basic warm up and data collection period to parameters:

```
class Param(RestrictAttributes):
    """
    Default parameters for simulation.
    """
    def __init__(
        self,
        asu_arrivals=ASUArrivals(),
        rehab_arrivals=RehabArrivals(),
        asu_los=ASULOS(),
        rehab_los=RehabLOS(),
        asu_routing=ASURouting(),
        rehab_routing=RehabRouting(),
        warm_up_period=0,
        data_collection_period=100
    ):
    ...
    self.warm_up_period = warm_up_period
    self.data_collection_period = data_collection_period
```

A basic patient class and a basic model class which generates patients and saves them to a list.

```
%load_ext autoreload
%autoreload 1
%aimport simulation

import numpy as np
import simpy

from sim_tools.distributions import Exponential
from simulation.parameters import Param


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
    def __init__(self, param, run_number):
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
        seeds = ss.spawn(4)

        # Create distributions
        self.asu_arrivals_stroke_dist = Exponential(
            mean=self.param.asu_arrivals.stroke, random_seed=seeds[0])
        self.asu_arrivals_tia_dist = Exponential(
            mean=self.param.asu_arrivals.tia, random_seed=seeds[1])
        self.asu_arrivals_neuro_dist = Exponential(
            mean=self.param.asu_arrivals.neuro, random_seed=seeds[2])
        self.asu_arrivals_other_dist = Exponential(
            mean=self.param.asu_arrivals.other, random_seed=seeds[3])

    def stroke_patient_generator(self):
        """Generate stroke patient arrivals."""
        while True:
            # Sample and pass time to arrival
            sampled_iat = self.asu_arrivals_stroke_dist.sample()
            yield self.env.timeout(sampled_iat)

            # Create a new patient, with ID based on length of patient list + 1
            p = Patient(patient_id=len(self.patients) + 1,
                        patient_type="stroke")

            # Record their arrival time
            p.arrival_time = self.env.now

            # Print arrival time
            print(f"Stroke patient arrival: {p.arrival_time}")

            # Add to the patients list
            self.patients.append(p)

    def tia_patient_generator(self):
        """Generate transient ischaemic attack (TIA) patient arrivals."""
        while True:
            # Sample and pass time to arrival
            sampled_iat = self.asu_arrivals_tia_dist.sample()
            yield self.env.timeout(sampled_iat)

            # Create a new patient, with ID based on length of patient list + 1
            p = Patient(patient_id=len(self.patients) + 1,
                        patient_type="tia")

            # Record their arrival time
            p.arrival_time = self.env.now

            # Print arrival time
            print(f"TIA patient arrival: {p.arrival_time}")

            # Add to the patients list
            self.patients.append(p)

    def neuro_patient_generator(self):
        """Generate complex neurological patient arrivals."""
        while True:
            # Sample and pass time to arrival
            sampled_iat = self.asu_arrivals_neuro_dist.sample()
            yield self.env.timeout(sampled_iat)

            # Create a new patient, with ID based on length of patient list + 1
            p = Patient(patient_id=len(self.patients) + 1,
                        patient_type="neuro")

            # Record their arrival time
            p.arrival_time = self.env.now

            # Print arrival time
            print(f"Neuro patient arrival: {p.arrival_time}")

            # Add to the patients list
            self.patients.append(p)

    def other_patient_generator(self):
        """Generate other patient arrivals."""
        while True:
            # Sample and pass time to arrival
            sampled_iat = self.asu_arrivals_other_dist.sample()
            yield self.env.timeout(sampled_iat)

            # Create a new patient, with ID based on length of patient list + 1
            p = Patient(patient_id=len(self.patients) + 1,
                        patient_type="other")

            # Record their arrival time
            p.arrival_time = self.env.now

            # Print arrival time
            print(f"Other patient arrival: {p.arrival_time}")

            # Add to the patients list
            self.patients.append(p)

    def run(self):
        """Run the simulation."""
        # Calculate the total run length
        run_length = (self.param.warm_up_period +
                      self.param.data_collection_period)

        # Schedule patient generators to run during the simulation
        self.env.process(self.stroke_patient_generator())
        self.env.process(self.tia_patient_generator())
        self.env.process(self.neuro_patient_generator())
        self.env.process(self.other_patient_generator())

        # Run the simulation
        self.env.run(until=run_length)

model = Model(param=Param(), run_number=0)
model.run()
```

> 💡 This is alot in one go. Need to break down into steps, e.g.
>
> 1. Add warm-up and data collection parameters
> 2. Create the patient class - can make it and then test it like:

```
# Test the Patient class
test_patient = Patient(patient_id=1, patient_type="stroke")
print(f"Patient ID: {test_patient.patient_id}")
print(f"Patient Type: {test_patient.patient_type}")
print(f"Initial arrival time: {test_patient.arrival_time}")
```

> 3. Create basic model structure (just param, run number, simpy environment, patients) - can make and run like:

```
# Test the basic model structure
model = Model(param=Param(), run_number=0)
print(f"Run number: {model.run_number}")
print(f"Initial patient list: {model.patients}")
```

> 4. Add random number generation (create seeds, create distributions).

```
# Test the model with random number generation
model = Model(param=Param(), run_number=42)
print(f"Sample from stroke arrival distribution: {model.asu_arrivals_stroke_dist.sample()}")
print(f"Sample from TIA arrival distribution: {model.asu_arrivals_tia_dist.sample()}")
```

> 5. Add single patient generator + run

```
# Test the model with stroke patient generator
model = Model(param=Param(), run_number=42)
model.run()
```

> 6. Add the other patient generators

```
# Test the model with all patient generators
model = Model(param=Param(), run_number=42)
model.run()
```

### Simplifying the patient generators

However, having seperate generators for each patient type is *very* repetitive - particularly when we factor in the rehab ones - and the simpler thing would be to make one method for all arrivals.

I did that, and made it a seperate method for better maintainability / clarity:

```
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
            print(f"{patient_type} patient arrival at {unit}: {p.arrival_time}")

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
```

## Tests and run time

We could add some basic tests now, e.g.

* Check that distributions are created for all patients (eg. "stroke" in distributions asu, "tia" in ...)
* Run with no warm-up and check env.now == param.data_collection_period
* Run with no data collection and check env.now == param.warm_up 

Although as not actually doing warm-up logic yet, going down that path a bit premature.

> 💡 Start with basic run time, then change to warm up + data collection

> 💡 Maybe don't need to be mentioning tests at this stage yet.

Hence, removed some of the tests and switched to just run time.

```
class MockParam:
    """
    Mock parameter class.
    """
    def __init__(self):
        """
        Initialise with specific run periods and arrival parameters.
        """
        self.warm_up_period = 10
        self.data_collection_period = 20

        self.asu_arrivals = namedtuple(
            "ASUArrivals", ["stroke", "tia", "neuro", "other"])(
            stroke=5, tia=7, neuro=10, other=15
        )
        self.rehab_arrivals = namedtuple(
            "RehabArrivals", ["stroke", "tia", "other"])(
            stroke=8, tia=12, other=20
        )


def test_create_distributions():
    """
    Test that distributions are created correctly for all units and patient
    types specified in MockParam.
    """
    param = MockParam()
    model = Model(param, run_number=42)

    # Check ASU distributions
    assert len(model.distributions["asu"]) == 4
    assert "stroke" in model.distributions["asu"]
    assert "tia" in model.distributions["asu"]
    assert "neuro" in model.distributions["asu"]
    assert "other" in model.distributions["asu"]

    # Check Rehab distributions
    assert len(model.distributions["rehab"]) == 3
    assert "stroke" in model.distributions["rehab"]
    assert "tia" in model.distributions["rehab"]
    assert "other" in model.distributions["rehab"]
    assert "neuro" not in model.distributions["rehab"]

    # Check that all distributions are Exponential
    for _, unit_dict in model.distributions.items():
        for patient_type in unit_dict:
            assert isinstance(unit_dict[patient_type], Exponential)


def test_sampling_seed_reproducibility():
    """
    Test that using the same seed produces the same results when sampling
    from one of the arrival distributions.
    """
    param = MockParam()

    # Create two models with the same seed
    model1 = Model(param, run_number=123)
    model2 = Model(param, run_number=123)

    # Sample from a distribution in both models
    samples1 = [model1.distributions["asu"]["stroke"].sample()
                for _ in range(10)]
    samples2 = [model2.distributions["asu"]["stroke"].sample()
                for _ in range(10)]

    # Check that the samples are the same
    np.testing.assert_array_almost_equal(samples1, samples2)


def test_run_time():
    """
    Check that the run length is correct with varying warm-up and data
    collection periods.
    """
    param = MockParam()

    # Test with zero warm-up period
    param.warm_up_period = 0
    model = Model(param, run_number=42)
    model.run()
    assert model.env.now == param.data_collection_period

    # Test with zero data collection period
    param.warm_up_period = 10
    param.data_collection_period = 0
    model = Model(param, run_number=42)
    model.run()
    assert model.env.now == 10
    # assert len(model.patients) == 0

    # Test with warm-up and data collection period
    param.warm_up_period = 12
    param.data_collection_period = 9
    model = Model(param, run_number=42)
    model.run()
    assert model.env.now == 21
    assert len(model.patients) > 0
```

## Patient destination & model logic

In the model length of stay is determined not just by patient type, but also patient destination post ASU. For example Early Supported Discharge greatly reduces length of stay. As such the model is designed to sample destination as the patient arrives.

Restructured `ASURouting` and `RehabRouting` (and also the LOS classes) to be dictionaries for each patient, a more useable format, as we'll be searching for parameters by patient type.

Created sampling distributions for routing and length of stay, and sampled the post-ASU destination.

At this point, built rest of model logic basically.

* Removed the redundant distribution from Model.patient_generator() and add the patient routing type (dependent on post-ASU destination for stroke - stroke_esd or stroke_noesd).
* Set up the ASU and rehab processes.

## Daily audit of occupancy

Figure 1 is the results from a daily audit of occupancy of the ASU (i.e. number of patients on the unit).

I add a variable recording occupancy, which is increased and decreased as patients come and go.

I then set up an auditor which checks and records the value of occupancy once per day.

## Logging

Soon, will want to run the model for longer time periods, and so want to be able to disable the printed messages if desired.

Hence, at this stage, I switched to using the logging module rather than simple print statements.

> 💡 Remember trace as simpler alternative if full logs are not desired.

I copied over the code from `rap_template_python_des` `logging.py`.

I then imported this class to `Param`, with `logger` now a parameter, tweaking it so you're just setting `log_to_console` and `log_to_file` rather than needing to provide the `SimLogger` class.

Within `Model`, I add information about model information to the log within `__init__`, and then replaced the `print()` statements elsewhere with `log()`.

## Occupancy plot

Now able to disable logging, I increased the run length and add code to generate the occupancy plot in `analysis.ipynb`.

This is similar but won't be quite right as have not yet add the warm-up period...

## Warm-up

Followed the template to add the warm-up period. Didn't include anything on choosing warm-up as that is already chosen in the paper. Steps to add warm-up were:

* Changing default warm-up parameter in `Param`.
* Run time is warm-up + data collection (already done).
* Add a warm-up method to `Model` which resets the results variables.
* Schedule this method in `run()`.

The template has lots going on in this regard, with fixing for utilisation and so on. Just went simple, with it all done in `warm_up()` method, and just setting `patients` and `audit_list` to [].

## Probability of delay plot

Add code to generate Figure 3, and included explanation of how we can determine probability of delay based on the frequencies and cumulative frequencies.

## Multiple replications & results output by the model

When running scenarios in the paper, the model was run with 150 replications. Used the python template to add a `Runner` class to execute this.

This took 26 seconds, so implemented with option for parallel execution.

I need to output the occupancy frequencies / probability of delay for each replication, so moved this code into the package.

## Linting, testing and parameter validation

Had been a while since linted, so did that.

This raised some errors in tests, which I hadn't run in ages, and these were no longer working properly.

I then add new tests based on the python template and on the tests ran in https://github.com/pythonhealthdatascience/llm_simpy/. This included unit tests, functional tests and back tests.

I add methods to check parameter validity in `Param`. This flagged that rehab other routing probability don't sum to 100% (88% and 13%) - but this is as described in the paper, and presumed to be due to rounding, so altered the validation test to allow.

> 💡 When explain tests, could do all in one section, like Tests > Back tests, Tests > Functional tests, Tests > Unit tests - and then on each of those pages, it's like, if you have parameter validation... if you have warm-up... etc. etc. suggesting tests could include.

## Scenario logic

Having successfully implemented the base model generating Figure 1 and 3 (as in https://github.com/pythonhealthdatascience/llm_simpy/), I then moved on to the scenarios from Monks et al. 2016. These were:

0. **Current admissions** Current admission levels; beds are reserved for either acute or rehab patients
1. **5% more admissions** A 5% increase in admissions across all patient subgroups.
2. **Pooling of acute and rehab beds** The acute and rehab wards are co-located at same site. Beds are pooled and can be used by either acute or rehabilitation patients. Pooling of the total bed stock of 22 is compared to the pooling of an increased bed stock of 26.
3. **Partial pooling of acute and rehab beds** The acute and rehab wards are co-located at same site. A subset of the 26 beds are pooled and can be used by either acute or rehab patients.
4. **No complex-neurological cases** Complex neurological patients are excluded from the pathway in order to assess their impact on bed requirements

### Scenario 1 and 4

As from the supplementary:

> "Scenarios investigating increased demand multiply the mean arrival rates (supplied in main text) by the appropriate factor. To exclude a particular patient group, the mean inter-arrival time for that group is multiplied by a large number such that no arrivals will occur in the modelled time horizon."

Hence, it is understood that:

* **Scenario 1** can be achieved by multiplying all patient IAT by 1.05 (see below: 0.95).
* **Scenario 4** can be achieved by multiplying IAT for complex neurological patients by a very high number (e.g. 10,000,000) - and can add a test which checks no patients are complex neurological.

## Using multiple replications

Altered `Runner` to output summary tables from across replications, and switched to using these for Figures 1 and 3.

## Scenario 1 + Table 2

Ran scenario 1 in `analysis.ipynb` and created Table 2. Noticed some differences. 

I find scenario with same bed number, probability of delay drops. They find that it goes up.

Thinking through the logic, scenario has more arrivals -> wards more full -> expect delays for lower max bed numbers earlier -> expect higher probability of delay for lower bed numbers.

I then realised my mistake! I had actually lower admissions, as I'd multiplied IAT by 1.05, when I should've multiplied by 0.95.

## Scenario 4 + supplementary table 1

Ran scenario, adjusted function from table 2 so it could be used to make this table too.

## Scenario logic

We now have two remaining scenarios:

* Scenario 2: **Pooling of acute and rehab beds** The acute and rehab wards are co-located at same site. Beds are pooled and can be used by either acute or rehabilitation patients. Pooling of the total bed stock of 22 is compared to the pooling of an increased bed stock of 26.
* Scenario 3: **Partial pooling of acute and rehab beds** The acute and rehab wards are co-located at same site. A subset of the 26 beds are pooled and can be used by either acute or rehab patients.

It took quite a while to understand the formula and how to implement them.