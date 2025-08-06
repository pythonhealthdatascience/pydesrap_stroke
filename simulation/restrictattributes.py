"""
Attribute restriction utilities.

Provides a base class to prevent adding new attributes to objects
after initialisation.
"""

from collections import UserDict


class RestrictAttributesMeta(type):
    """
    Metaclass for attribute restriction.

    A metaclass modifies class construction. It intercepts instance creation
    via __call__, adding the _initialised flag after __init__ completes. This
    is later used by RestrictAttributes to enforce attribute restrictions.
    """
    def __call__(cls, *args, **kwargs):
        # Create instance using the standard method
        instance = super().__call__(*args, **kwargs)
        # Set the "_initialised" flag to True, marking end of initialisation
        instance.__dict__["_initialised"] = True
        return instance


class RestrictAttributes(metaclass=RestrictAttributesMeta):
    """
    Base class that prevents the addition of new attributes after
    initialisation.

    This class uses RestrictAttributesMeta as its metaclass to implement
    attribute restriction. It allows for safe initialisation of attributes
    during the __init__ method, but prevents the addition of new attributes
    afterwards.

    The restriction is enforced through the custom __setattr__ method, which
    checks if the attribute already exists before allowing assignment.
    """
    def __setattr__(self, name, value):
        """
        Prevent addition of new attributes.

        Parameters
        ----------
        name: str
            The name of the attribute to set.
        value: any
            The value to assign to the attribute.

        Raises
        ------
        AttributeError
            If `name` is not an existing attribute and an attempt is made
            to add it to the class instance.
        """
        # Check if the instance is initialised and the attribute doesn"t exist
        if hasattr(self, "_initialised") and not hasattr(self, name):
            # Get a list of existing attributes for the error message
            existing = ", ".join(self.__dict__.keys())
            raise AttributeError(
                f"Cannot add new attribute '{name}' - only possible to " +
                f"modify existing attributes: {existing}."
            )
        # If checks pass, set the attribute using the standard method
        object.__setattr__(self, name, value)


class LockedDict(UserDict):
    """
    Wrapper that prevents adding or deleting top-level keys in a dictionary
    after creation.

    This prevents accidental addition or deletion of keys after construction,
    helping to avoid subtle bugs (e.g., typos introducing new keys).

    Attributes
    ----------
    _locked_keys : set
        The set of top-level keys locked after initialisation.
    _locked_keys_initialised : bool
        Indicates whether locked key enforcement is active (True after
        __init__ completes). This flag is crucial for compatibility with
        joblib and multiprocessing, as object reconstruction during
        deserialisation may call __setitem__ before additional attributes are
        restored.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialise the LockedDict.

        Parameters
        ----------
        *args, **kwargs : any
            Arguments passed to dict for initialisation. Top-level keys will
            be locked.

        Notes
        -----
        """
        self._locked_keys_initialised = False
        super().__init__(*args, **kwargs)
        self._locked_keys = set(self.data)
        self._locked_keys_initialised = True

    def __setitem__(self, key, value):
        """
        Restrict assignment to existing top-level keys.

        Parameters
        ----------
        key : str
            Top-level dictionary key.
        value : any
            Value to assign.

        Raises
        ------
        KeyError
            If key is not an original top-level key.

        Notes
        -----
        Key restriction is enforced only after initialisation to prevent errors
        when used with joblib or multiprocessing, which may call __setitem__
        before all attributes are available.
        """
        if getattr(self, '_locked_keys_initialised', False):
            if key not in self._locked_keys:
                raise KeyError(
                    f"Attempted to add or update key '{key}', which is not "
                    f"one of the original locked keys. This is likely due to "
                    f"a typo or unintended new parameter. Allowed top-level "
                    f"keys are: [{self._locked_keys}]"
                )
        super().__setitem__(key, value)

    def __delitem__(self, key):
        """
        Prevent deletion of top-level keys.

        Parameters
        ----------
        key : str
            Top-level dictionary key.

        Raises
        ------
        KeyError
            Always, to disallow top-level key deletion.
        """
        raise KeyError(
            f"Deletion of key '{key}' is not allowed. The set of top-level "
            f"keys is locked to prevent accidental removal of expected "
            f"parameters. Allowed top-level keys are: [{self._locked_keys}]"
        )
