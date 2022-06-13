from scripts.helpful_scripts import get_account, encode_function_data
from brownie import Box, network, ProxyAdmin, TransparentUpgradeableProxy, Contract


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})
    print(box.retrieve())
    # print(box.increment())

    proxy_admin = ProxyAdmin.deploy({"from": account})

    # initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print("Proxy deployed to {proxy}, you can upgrade to v2!")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(proxy_box.retrieve())
    print(proxy_box.store(2, {"from": account}))
    print(proxy_box.retrieve())
