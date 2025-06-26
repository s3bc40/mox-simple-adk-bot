# pragma version 0.4.2
"""
@title Counter Contract
@license MIT
@author s3bc40
@notice A simple counter contract that allows setting and incrementing a counter.
"""

################################################################
#                            ERRORS                            #
################################################################
COUNTER_RISK_OVERFLOW: public(constant(String[64])) = "Counter: counter risk overflow"

################################################################
#                            EVENTS                            #
################################################################
event CounterIncremented:
    new_counter: indexed(uint256)


event CounterSet:
    new_counter: indexed(uint256)

event CounterReset:
    pass


################################################################
#                       STATE VARIABLES                        #
################################################################
counter: public(uint256)


################################################################
#                      EXTERNAL FUNCTIONS                      #
################################################################
@external
def set_counter(_new_counter: uint256):
    """Set the counter to a new value.

    Args:
        _new_counter (uint256): The new value for the counter.
    """
    self.counter = _new_counter
    log CounterSet(new_counter=_new_counter)


@external
def increment_or_reset():
    """Increment the counter by 1 or reset it if it overflows."""
    if self.counter == max_value(uint256):
        self.counter = 0
        log CounterReset()
    else:
        self.counter += 1
        log CounterIncremented(new_counter=self.counter)
