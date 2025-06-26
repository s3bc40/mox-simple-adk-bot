from src import counter
from moccasin.boa_tools import VyperContract


def deploy() -> VyperContract:
    counter_contract: VyperContract = counter.deploy()
    return counter_contract


def moccasin_main() -> VyperContract:
    return deploy()
