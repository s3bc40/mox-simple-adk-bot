import pytest
from script.deploy import deploy


@pytest.fixture(scope="session")
def counter_contract():
    return deploy()
