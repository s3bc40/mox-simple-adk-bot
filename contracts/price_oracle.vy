# pragma version 0.4.2
"""
@title Simple Price Oracle Contract
@license MIT
@author s3bc40
@notice A simple price oracle contract that allows an updater to set a price.
"""
################################################################
#                            EVENTS                            #
################################################################
event PriceUpdated:
    updater: indexed(address)  # Address of the updater
    timestamp: uint256  # Timestamp of the update
    new_price: uint256  # New price in WEI


event UpdaterSet:
    new_updater: indexed(address)  # Address of the new updater


################################################################
#                            ERRORS                            #
################################################################
SENDER_ZERO_ADDRESS: public(
    constant(String[51])
) = "price_oracle: sender address cannot be zero address"
ONLY_OWNER: public(
    constant(String[40])
) = "price_oracle: only owner can set updater"
ONLY_UPDATER: public(
    constant(String[60])
) = "price_oracle: only designated updater can call this function"

################################################################
#                    CONSTANTS & IMMUTABLES                    #
################################################################
OWNER: public(immutable(address))

################################################################
#                       STATE VARIABLES                        #
################################################################
price: public(uint256)  # Price in WEI
last_updated_timestamp: public(uint256)
updater_address: public(address)

################################################################
#                         CONSTRUCTOR                          #
################################################################
@deploy
def __init__():
    """
    @notice Initializes the contract with the deployer as the owner and sets initial values.
    """
    self._not_zero_address(msg.sender)
    OWNER = msg.sender
    self.price = 0
    self.last_updated_timestamp = block.timestamp
    self.updater_address = msg.sender


################################################################
#                      EXTERNAL FUNCTIONS                      #
################################################################
@external
def set_updater(_new_updater: address):
    """
    @notice Sets a new updater address for the price oracle.

    Only the owner can call this function.

    @param _new_updater The address of the new updater.
    """
    assert msg.sender == OWNER, ONLY_OWNER
    self._not_zero_address(_new_updater)

    self.updater_address = _new_updater
    log UpdaterSet(new_updater=_new_updater)


@external
def update_price(_new_price: uint256):
    """
    @notice Updates the price in the oracle.
    Only the designated updater can call this function.
    @param _new_price The new price to set in the oracle.
    """
    assert msg.sender == self.updater_address, ONLY_UPDATER
    self.price = _new_price
    self.last_updated_timestamp = block.timestamp
    log PriceUpdated(
        updater=msg.sender, timestamp=block.timestamp, new_price=_new_price
    )


################################################################
#                        VIEW FUNCTIONS                        #
################################################################
@external
@view
def get_price() -> uint256:
    """
    @notice Returns the current price stored in the oracle.
    @return The current price in WEI.
    """
    return self.price


@external
@view
def get_last_updated() -> uint256:
    """
    @notice Returns the timestamp of the last price update.
    @return The timestamp of the last update.
    """
    return self.last_updated_timestamp


################################################################
#                      INTERNAL FUNCTIONS                      #
################################################################
@internal
@pure
def _not_zero_address(_sender: address):
    """
    @notice Internal function to check if the sender address is not zero.
    """
    assert _sender != empty(address), SENDER_ZERO_ADDRESS
