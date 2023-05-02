import os

import pytest
from dotenv import load_dotenv

from proairtable import AirtableClient

# link to base - https://airtable.com/appKT43W60OTngQkq/tblrV4mZh51UPCFUe/viwN1nh7SnRDSUZyy?blocks=hide
TEST_BASE_ID = "appKT43W60OTngQkq"


@pytest.fixture(scope="module")
def test_client():
    # path to 2 directories above current file
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(path)
    return AirtableClient(TEST_BASE_ID)
