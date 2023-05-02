from proairtable import AirtableSchema, fields

TEST_TABLE = "Test"


class TestSchema(AirtableSchema):
    name: fields.Text("Name", required=True)
    joining_date: fields.Date("Joining Date", required=False)


def test(test_client):
    # read above schema
    data = test_client.load_data(table=TEST_TABLE, schema=TestSchema)
    if len(data) > 0:
        # delete all records
        test_client.delete_records(table=TEST_TABLE, record_ids=[d.record_id for d in data])
        data = test_client.load_data(table=TEST_TABLE, schema=TestSchema)
    assert len(data) == 0

    # create new records
    new_records = [
        TestSchema(name="test1", joining_date="2020-01-01"),
        TestSchema(name="test2", joining_date="2020-01-02"),
    ]
    test_client.create_records(table=TEST_TABLE, data=new_records)
    data = test_client.load_data(table=TEST_TABLE, schema=TestSchema)
    assert len(data) == 2

    # delete records
    test_client.delete_records(table=TEST_TABLE, record_ids=[d.record_id for d in data])
    data = test_client.load_data(table=TEST_TABLE, schema=TestSchema)
    assert len(data) == 0
