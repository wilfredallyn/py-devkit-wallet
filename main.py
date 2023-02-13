import bdkpython as bdk
from wallet import Wallet


if __name__ == "__main__":
    # create wallet
    wallet = Wallet()

    # receive and sync
    print(f"Last unused P2PKH testnet address: {wallet.get_last_unused_address()}")
    print(f"New P2PKH testnet address: {wallet.get_new_address()}")

    wallet.sync()
    print(wallet.get_balance())

    # send

    # get transaction history

    # display recovery phrase

    # enable wallet recovery
