import pytest
from script.deploy import deploy


@pytest.fixture(scope="session")
def price_oracle_contract():
    return deploy()
