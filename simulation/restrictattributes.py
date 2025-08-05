"""
Attribute restriction utilities.

Provides a base class to prevent adding new attributes to objects
after initialisation.
"""


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
