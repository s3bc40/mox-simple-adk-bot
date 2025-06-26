from boa.test.strategies import given, strategy as st_boa


MAX_UINT256 = (
    115792089237316195423570985008687907853269984665640564039457584007913129639935
)


def test_initial_counter(counter_contract):
    """Test that the initial counter value is 0."""
    assert counter_contract.counter() == 0


@given(_value=st_boa("uint256", min_value=1, max_value=1000))
def test_set_counter(counter_contract, _value):
    """Test setting the counter to a specific value."""
    counter_contract.set_counter(_value)
    logs = counter_contract.get_logs()
    log_counter = logs[0].new_counter

    assert counter_contract.counter() == _value
    assert log_counter == _value


def test_increment(counter_contract):
    """Test incrementing the counter by 1."""
    counter_contract.increment_or_reset()
    logs = counter_contract.get_logs()
    log_counter = logs[0].new_counter

    assert counter_contract.counter() == 1
    assert log_counter == 1


def test_increment_reset_overflow(counter_contract):
    """Test that incrementing the counter at max value resets it to 0."""
    # Set the counter to the maximum value
    max_value = MAX_UINT256
    counter_contract.set_counter(max_value)
    log_set_counter = counter_contract.get_logs()[0].new_counter

    # Attempt to increment the counter, which should raise an assertion error
    counter_contract.increment_or_reset()
    log_reset = counter_contract.get_logs()[0]

    assert counter_contract.counter() == 0
    assert log_set_counter == max_value
    assert log_reset is not None
