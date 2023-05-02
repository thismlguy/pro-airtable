from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type


class AirtableField(ABC, object):
    """This is a custom field that can be used to create custom fields for your airtable schema.
    See https://pydantic-docs.helpmanual.io/usage/schema/#custom-data-types for more information"""

    name: str
    required: bool
    default: Optional[Any] = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    @abstractmethod
    def validate(cls, v):
        """This should handle both cases when a field is being read from airtable and when a user might want to set
        it manually."""
        raise NotImplementedError("You must implement this method in your custom field")

    @classmethod
    def format_airtable(cls, v):
        """format value to be exported to airtable"""
        return v


def make_field(cls: Type[AirtableField], name: str, required: bool, default: Any, params: Optional[Dict] = None):
    return type(cls.__name__, (cls,), {"name": name, "required": required, "default": default, **(params or {})})
