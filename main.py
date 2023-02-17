import bdkpython as bdk
from logger import setup_logger
import pprint
from repository import Repository
from wallet import Wallet


if __name__ == "__main__":
    logger = setup_logger()

    # create wallet
    pkl_file = "repository.pkl"
    wallet = Wallet(pkl_file)

    # check balance
    wallet.sync()
    balance = wallet.get_balance()
    logger.info(f"Balance\n{pprint.pformat(balance.__dict__)}\n")

    # receive and sync
    receive_address = wallet.get_new_address()
    logger.info(f"New P2PKH testnet address is {receive_address.address}\n")

    send_amount = 800
    if balance.spendable < send_amount:
        logger.info(
            f"You need to deposit funds to demonstrate wallet send functionality\n"
        )
    else:
        # send: create tx, sign, broadcast
        send_address = "tb1qtnjgg0qnvjw7rk4pa8459ew0n6j3sgjksjysc7"
        tx_result = wallet.create_transaction(
            recipient=send_address,
            amount=send_amount,
            fee_rate=1.0,
        )
        psbt, tx_details = tx_result.psbt, tx_result.transaction_details
        wallet.sign(psbt)
        txid = wallet.broadcast(psbt)
        logger.info(f"Transaction Details\n{pprint.pformat(tx_details.__dict__)}\n")

        # should reflect new balance after send
        wallet.sync()
        logger.info(
            f"After sending {send_amount}, balance is\n{pprint.pformat(balance.__dict__)}\n"
        )

    # get transaction history
    tx_history = wallet.get_transaction_history()
    logger.info("Wallet transaction history")
    for tx in tx_history:
        logger.info(tx + "\n")

    # display recovery phrase
    logger.info(f"Mnemonic is '{wallet.get_mnemonic()}'")

    # enable wallet recovery
    wallet.persist()
    wallet_2 = Wallet(pkl_file)
    logger.info(f"Mnemonic for recovered wallet is '{wallet_2.get_mnemonic()}'\n")
