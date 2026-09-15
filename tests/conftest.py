import pytest
from utils.api_client import APIClient
from utils.db_client import DBClient

@pytest.fixture
def api(): return APIClient()

@pytest.fixture
def authenticated_api(api):
    api.login(); return api

@pytest.fixture
def db(): return DBClient()

@pytest.fixture
def meter_serial(): return "MTR-61594"
