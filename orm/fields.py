import abc
import datetime


class FieldMeta(abc.ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        if '__field_type__' not in namespace:
            raise AttributeError("Field must have __field_type__ attribute!")

        return super().__new__(mcs, name, bases, namespace)


class BaseField(metaclass=FieldMeta):
    __field_type__ = None

    def __init__(self, id=False, default=None, presentation=False, required=False):
        # TODO: add immutable option, make ids immutable by default
        # TODO: add `name` option
        self._id = id
        self._presentation = presentation
        self._required = required

        if default is None or isinstance(default, self.__field_type__):
            self._value = default
        else:
            raise TypeError("Default value should be None of of the same type as field!")

    @property
    def is_id(self):
        return self._id

    @property
    def required(self):
        return self._required

    @property
    def presentation(self):
        return self._presentation

    @presentation.setter
    def presentation(self, value):
        self._presentation = bool(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value and not isinstance(value, self.__field_type__):
            try:
                self._value = self.__field_type__(value)
                return
            except Exception as exception:
                raise TypeError("{}: Wrong field type <{}>. Should be <{}>.".format(
                    self.__class__.__name__,
                    value.__class__.__name__,
                    self.__field_type__.__name__
                )) from exception

        self._value = value

    @value.deleter
    def value(self):
        self._value = None


class AnyField(BaseField):
    __field_type__ = object


class StringField(BaseField):
    __field_type__ = str


class IntField(BaseField):
    __field_type__ = int


class FloatField(BaseField):
    __field_type__ = float


class DictField(BaseField):
    __field_type__ = dict


class BooleanField(BaseField):
    __field_type__ = bool


class DateField(BaseField):
    __field_type__ = datetime.datetime

