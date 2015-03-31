# BEGIN MODEL_V5
import abc


class AutoStorage:  # <1>
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)  # <2>


class Validated(abc.ABC, AutoStorage):  # <3>

    def __set__(self, instance, value):
        value = self.validate(instance, value)  # <4>
        super().__set__(instance, value)  # <5>

    @abc.abstractmethod
    def validate(self, instance, value):  # <6>
        """return validated value or raise ValueError"""


class Quantity(Validated):  # <7>
    """a number greater than zero"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value  # <8>

# END MODEL_V5
