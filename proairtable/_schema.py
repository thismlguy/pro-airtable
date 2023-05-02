from abc import ABC
from typing import Any, Dict, Iterator, Optional, Tuple, TypeVar

from pydantic import BaseModel, PrivateAttr

from proairtable.fields.base import AirtableField
from proairtable.fields.string import RecordID

A = TypeVar("A")


class AirtableSchema(ABC, BaseModel):
    """This base model comes with some functionality which makes it easier to define airtable schemas into python and
    handle data transaction between airtable and python. Some key features are:

    - The column names are automatically inferred from the field names of the schema. This means that you can use

    """

    record_id: RecordID = None

    _error_key = PrivateAttr(default="error")

    @classmethod
    def _check_error_value(cls, value: Optional[A]) -> Optional[A]:
        """run a mapper on an item if it is not None"""
        if value is None:
            return None
        if isinstance(value, dict):
            if cls._error_key in value:
                return None
        return value

    @classmethod
    def _parse_field(cls, airtable_fields: Dict[str, Any]) -> Iterator[Tuple[str, AirtableField]]:
        # iterate through all fields
        for field_name, field in cls.__fields__.items():
            field_type: AirtableField = field.type_
            value = cls._check_error_value(airtable_fields.get(field_type.name))
            if value is not None:
                yield field_name, value
            else:
                # if field is not present in airtable, check if it has a default value
                if field.default is not None:
                    yield field_name, field.default
                else:
                    # if field is not present in airtable and has no default value, check if it is required
                    if field.required:
                        raise ValueError(f"field {field_name} is required but not present in airtable")

    @classmethod
    def parse_record(cls, id: str, airtable_fields: Dict[str, Any]) -> "AirtableSchema":
        fields = dict(cls._parse_field(airtable_fields))
        return cls(record_id=id, **fields)

    def create_export_fields(self):
        # drop keys with None values and record_id key
        field_type_mapping = {name: field.type_ for name, field in self.__fields__.items()}
        return {
            self.__fields__[key].type_.name: self.__fields__[key].type_.format_airtable(value)
            for key, value in self.dict().items()
            if value is not None
        }
