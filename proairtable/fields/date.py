from abc import ABC
from datetime import datetime
from typing import Any, Optional

from proairtable.fields.base import AirtableField, make_field


class _DateField(str, AirtableField, ABC):
    _airtable_format: str = "%Y-%m-%d"
    _user_format: str = _airtable_format

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError(f"DateField requires a string input, found {type(v)}")
        # check it is
        return v

    @classmethod
    def format_airtable(cls, v: str) -> str:
        if cls._user_format == cls._airtable_format:
            return v
        return datetime.strptime(v, cls._user_format).strftime(cls._airtable_format)


def Date(name: str, required: bool, default: Optional[Any] = None, date_format: Optional[str] = None):
    """Type for date fields.
    Args:
        name: name of the field to read from airtable
        required: if True, an error will be raised if the field is not present in airtable; default is False
        default: default value for the field
        date_format: date format in which you want to store date values. Note that this will change the format in
            which dates should be parsed when reading data from airtable. By default, airtable uses ISO format
            `YYYY-MM-DD` for dates. Even If you set this attribute, this will only change how the dates are stored
            into the given schema when reading data from airtable. The date will be converted
            back to airtable's accepted format when you export data to airtable.

    Returns:
        New Type for the particular date field
    """
    return make_field(
        _DateField,
        name=name,
        required=required,
        default=default,
        params={"_user_format": date_format} if date_format else None,
    )
