from contracts import price_oracle
from moccasin.boa_tools import VyperContract


def deploy() -> VyperContract:
    contract: VyperContract = price_oracle.deploy()
    return contract


def moccasin_main() -> VyperContract:
    return deploy()
