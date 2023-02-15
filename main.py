import bdkpython as bdk
from wallet import Wallet


if __name__ == "__main__":
    # https://github.com/thunderbiscuit/bitcoindevkit-scripts/tree/master/python
    # https://thunderbiscuit.github.io/devkit-wallet/simple-wallet/

    # create wallet
    wallet = Wallet()

    # receive and sync
    receive_address = wallet.get_last_unused_address()
    print(f"Last unused P2PKH testnet address: {receive_address}")
    # print(f"New P2PKH testnet address: {wallet.get_new_address()}")

    # fund wallet with 1000 sats to receive_address
    # check balance
    wallet.sync()
    print(wallet.get_balance())

    # send: create tx, sign, broadcast
    send_address = "tb1qtnjgg0qnvjw7rk4pa8459ew0n6j3sgjksjysc7"
    tx_result = wallet.create_transaction(
        recipient=send_address,
        amount=800,
        fee_rate=1.0,
    )
    psbt, tx_details = tx_result.psbt, tx_result.transaction_details
    wallet.sign(psbt)
    txid = wallet.broadcast(psbt)
    # print(tx_details.__dict__)

    # should reflect new balance after send
    wallet.sync()
    print(wallet.get_balance())

    # get transaction history
    tx_history = wallet.get_transaction_history()
    for tx in tx_history:
        print(tx, "\n")

    # display recovery phrase

    # enable wallet recovery
