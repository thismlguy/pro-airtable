from typing import Any, Optional

from proairtable.fields.base import AirtableField, make_field


class _StringBase(str, AirtableField):
    """Base class for string fields."""

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError(f"object of type {cls.__name__} requires a string input, found {type(v)}")
        return v


RecordID = make_field(_StringBase, name="record_id", required=False, default=None)


def Text(name: str, required: bool, default: Optional[Any] = None):
    """
    Type for string fields.
    Args:
        name: name of the field to read from airtable
        required: if True, an error will be raised if the field is not present in airtable; default is False
        default: default value for the field
    Returns:
        New Type for the particular string field
    """
    return make_field(_StringBase, name=name, default=default, required=required)
