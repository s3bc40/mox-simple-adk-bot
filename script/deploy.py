import json


from contracts import price_oracle
from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network
from pathlib import Path


def deploy() -> VyperContract:
    """Deploy the price oracle contract to the active network.

    Stores the contract address, ABI, and RPC URL in a JSON file.
    Returns:
        VyperContract: The deployed contract instance.

    Raises:
        ValueError: If the contract deployment fails and returns None.
    """
    active_network = get_active_network()
    contract: VyperContract = price_oracle.deploy()

    # If contract is not None, store the address, abi and RPC URL
    # in a JSON file
    if contract is not None:
        # Create the secrets directory if it doesn't exist
        # and save the contract details in a JSON file
        secrets_dir = Path(__file__).resolve().parent.parent / "secrets"
        secrets_dir.mkdir(parents=True, exist_ok=True)
        output_path = secrets_dir / "price_oracle_deploy.json"
        with open(output_path, "w") as f:
            json.dump(
                {
                    "address": contract.address,
                    "abi": contract.abi,
                    "rpc_url": active_network.url,
                },
                f,
            )
    else:
        raise ValueError("Contract deployment failed. Contract is None.")
    print(f"Price Oracle deployed at {contract.address} on {active_network.name}")
    return contract


def moccasin_main() -> VyperContract:
    return deploy()
