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

> 💡 I realise the templates are a little daunting - and I wrote them! Getting started with this, I did the strategy of essentially "clearing things away" - and then referring back to them as I got set up again. Perhaps a more useable / accessible version of these templates would be structuring them as step-by-step quarto books. Because that's essentially how am I treating them - AND that is how I learnt best, when I was learning DES, is working through step-by-step with the HSMA book, building it up. So these templates are me having worked out how to implement everything we want - and then the applied examples is stress testing / real life testing, figuring out how we work through, where we make changes - and using all that then to write step-by-step tutorial books. One for Python, one for R. Step-by-step walkthough of RAP DES in XYZ.

## Back to parameters

### Refactoring

With so many parameters, I feel like it maybe makes sense to seperate out the code more than I did in the template, so have changed from `model.py` to `parameters.py`

> 💡 Could the location of functions in the template do with reorganising? What is clearest?

### Playing with them

I wanted to try out using the classes to make sure they work. I created a disposable notebook to play around with them in.

> 💡 Should be clear how we do this early on, so can play about with it.

I realised dataclasses don't allow you to call ASUArrivals(stroke=4), as they are recognised as attributes, but only recognised as parameters when you type hint ie.

```
@dataclass
class ASUArrivals:
    stroke: float = 1.2
    tia: float = 9.3
    neuro: float = 3.6
    other: float = 3.2

ASUArrivals(stroke=4)
```

I don't want this weird/hidden-feeling behaviour, especially as people say type hints shouldn't functionally affect your code in Python, and so will stick with normal classes.

### Preventing addition of new attributes

From writing the templates, I know how important it is that we prevent the addition of new attributes.

In python, I do this using a method in the parameter class. This is also possible in R if set up as a R6Class, but I chose to use a function for simplicity, so that instead checks the parameters when they are input to model. The downside of that approach as it will check every time the model is called (i.e. with each replication).

However, an alternative would be for my parameter classes to **inherit** from a main class with that functionality.

> 💡 Emphasise the importance of this, that it's not just something to drop.

> 💡 When using the dataclasses, our provided method for preventing the addition of new attributes no longer works.

I set up the **parent class**, and then add **tests** which check this is functioning properly.