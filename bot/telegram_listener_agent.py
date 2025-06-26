import boa
import logging

from dotenv import load_dotenv
from src import counter

################################################################
#                            SETUP                             #
################################################################
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="telegram_listener_agent.log", encoding="utf-8", level=logging.DEBUG
)

################################################################
#                          CONSTANTS                           #
################################################################
# More supported models can be referenced here: https://ai.google.dev/gemini-api/docs/models#model-variations
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
COUNTER_CONTRACT_ADDRESS = "0xYourCounterContractAddressHere"


################################################################
#                            TOOLS                             #
################################################################
def get_counter() -> dict:
    """Retrieves the current counter value from the contract.

    Returns:
        dict: A dictionary containing the current counter value.
    """
    logger.info("--- Tool: Retrieving current counter value. ---")


# WIP: still not convinced by using web3.py
# if __name__ == "__main__":
#     counter_contract = counter.deploy()
#     logger.info(f"Counter contract deployed at: {counter_contract.address}")
