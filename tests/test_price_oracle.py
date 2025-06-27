import boa

from eth.constants import ZERO_ADDRESS
from boa.test.strategies import given, strategy as st_boa


MAX_PRICE = 3000 * 10**18  # Example maximum price in WEI


def test_initial_price_oracle_state(price_oracle_contract):
    """Test that the initial state of the Price Oracle contract is correct."""
    assert price_oracle_contract.price() == 0
    assert price_oracle_contract.last_updated_timestamp() > 0
    assert price_oracle_contract.updater_address() == price_oracle_contract.OWNER()


def test_set_updater_zero_address(price_oracle_contract):
    """Test that setting the updater to a zero address by the owner raises an error."""
    with boa.env.prank(price_oracle_contract.OWNER()):
        with boa.reverts(price_oracle_contract.SENDER_ZERO_ADDRESS()):
            price_oracle_contract.set_updater(ZERO_ADDRESS.hex())


def test_set_updater_not_owner(price_oracle_contract):
    """Test that a non-owner cannot set the updater address."""
    non_owner = boa.env.generate_address("non_owner")

    with boa.env.prank(non_owner):
        with boa.reverts(price_oracle_contract.ONLY_OWNER()):
            price_oracle_contract.set_updater(non_owner)


def test_set_updater(price_oracle_contract):
    """Test setting a new updater address by the owner."""
    new_updater = boa.env.generate_address("new_updater")

    with boa.env.prank(price_oracle_contract.OWNER()):
        price_oracle_contract.set_updater(new_updater)
    logs = price_oracle_contract.get_logs()
    log_update_set = logs[0]

    assert price_oracle_contract.updater_address() == new_updater
    assert log_update_set.new_updater == new_updater


def test_update_price_not_updater(price_oracle_contract):
    """Test that a non-updater cannot update the price."""
    non_updater = boa.env.generate_address("non_updater")

    with boa.env.prank(non_updater):
        with boa.reverts(price_oracle_contract.ONLY_UPDATER()):
            price_oracle_contract.update_price(MAX_PRICE)


@given(_new_price=st_boa("uint256", min_value=1, max_value=MAX_PRICE))
def test_update_price(price_oracle_contract, _new_price):
    """Test updating the price by the designated updater."""
    # The initial updater is the contract owner
    updater = price_oracle_contract.OWNER()

    with boa.env.prank(updater):
        price_oracle_contract.update_price(_new_price)
    logs = price_oracle_contract.get_logs()
    log_price_updated = logs[0]

    assert price_oracle_contract.price() == _new_price
    assert price_oracle_contract.last_updated_timestamp() > 0
    assert log_price_updated.updater == updater
    assert log_price_updated.new_price == _new_price
    assert log_price_updated.timestamp == price_oracle_contract.last_updated_timestamp()
