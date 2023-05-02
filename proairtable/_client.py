import os
from typing import List, Optional, Type, TypeVar

from pyairtable import Table

from proairtable._schema import AirtableSchema

A = TypeVar("A", bound=AirtableSchema)


class AirtableClient:
    """Client that manages data transaction from airtable. It can read, write, update and delete records from
    airtable."""

    _KEY_ENV_VAR = "AIRTABLE_API_KEY"

    def __init__(self, base_id: str, api_key: Optional[str] = None):
        """Initialize airtable client
        Args:
            base_id: ID of the base which needs to be handled, different bases need their own clients.
            api_key: API key for airtable base. if not provided, it will be read from the environment variable
                AIRTABLE_API_KEY
        """
        self.base_id = base_id
        self.api_key = api_key or os.environ[self._KEY_ENV_VAR]
        self._tables = {}

    def _get_table(self, table: str) -> Table:
        if table not in self._tables:
            self._tables[table] = Table(api_key=self.api_key, base_id=self.base_id, table_name=table)
        return self._tables[table]

    def load_data(self, table: str, schema: Type[A], raise_exception: bool = False, verbose: bool = False) -> List[A]:
        """Load data from airtable and parse it using the provided schema.

        Args:
            table: name of the table to read
            schema: the schema of type `AirtableSchema` into which the data needs to be parsed
            raise_exception: if True, an exception will be raised when error is found in parsing. If False,
                the error rows will be skipped
            verbose: if True, the error rows will be printed to stdout

        Returns:
            List of data read from the table in the provided schema
        """
        _table = self._get_table(table)
        all_data = []
        for row in _table.all():
            try:
                row_data = schema.parse_record(id=row["id"], airtable_fields=row["fields"])
                all_data.append(row_data)
            except Exception as e:
                if raise_exception:
                    raise e
                if verbose:
                    print(f"error found in row {row['fields']}")
        return all_data

    def update_records(self, table: str, data: List[AirtableSchema]):
        """Update airtable records. The records will be updated based on the record_id of the data.

        Args:
            table: name of the table to update records in
            data: data to be updated, each record should have `record_id` attribute set which will be used to update
                the records.
        """
        _table = self._get_table(table)
        data_updates = [{"id": d.record_id, "fields": d.create_export_fields()} for d in data]
        _table.batch_update(data_updates, typecast=True)

    def create_records(self, table: str, data: List[AirtableSchema]):
        """Create new records in airtable.

        Args:
            table: name of the table to read
            data: data to be added, `record_id` attribute should NOT be set in this case. If it is set, it will be
                ignored
        """
        _table = self._get_table(table)
        data_records = [d.create_export_fields() for d in data]
        return _table.batch_create(data_records, typecast=True)

    def delete_records(self, table: str, record_ids: List[str]):
        """Delete the given records ids from table.

        Args:
            table: name of the table to read
            record_ids: List of record ids to delete
        """
        _table = self._get_table(table)
        _table.batch_delete(record_ids)
