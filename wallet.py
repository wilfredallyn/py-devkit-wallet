import bdkpython as bdk
from datetime import datetime


class Wallet(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Wallet, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.network = bdk.Network.TESTNET
        self.database = bdk.DatabaseConfig.MEMORY()
        # self.database = bdk.DatabaseConfig.SQLITE(
        #     bdk.SqliteDbConfiguration(os.path.join(os.getcwd(), "bdk-sqlite"))
        # )
        self._create_blockchain()
        self.create_wallet()

    def _create_blockchain(self) -> None:
        blockchain_config = bdk.BlockchainConfig.ELECTRUM(
            bdk.ElectrumConfig(
                url="ssl://electrum.blockstream.info:60002",
                socks5=None,
                retry=5,
                timeout=None,
                stop_gap=100,
                validate_domain=True,
            )
        )
        self.blockchain = bdk.Blockchain(blockchain_config)

    def create_wallet(self) -> None:
        mnemonic = bdk.Mnemonic(bdk.WordCount.WORDS12)
        bip32_root_key = bdk.DescriptorSecretKey(
            network=self.network,
            mnemonic=mnemonic,
            password="",
        )
        external_descriptor = self._create_external_descriptor(bip32_root_key)
        internal_descriptor = self._create_internal_descriptor(bip32_root_key)

        self.bdk_wallet = bdk.Wallet(
            descriptor=external_descriptor,
            change_descriptor=internal_descriptor,
            network=self.network,
            database_config=self.database,
        )

    def _create_external_descriptor(
        self, root_key: bdk.DescriptorSecretKey
    ) -> bdk.Descriptor:
        external_path = bdk.DerivationPath("m/84h/1h/0h/0")
        return bdk.Descriptor(
            f"wpkh({root_key.extend(external_path).as_string()})",
            self.network,
        )
        # Log.i(TAG, "Descriptor for receive addresses is $externalDescriptor")

    def _create_internal_descriptor(
        self, root_key: bdk.DescriptorSecretKey
    ) -> bdk.Descriptor:
        internal_path = bdk.DerivationPath("m/84h/1h/0h/1")
        return bdk.Descriptor(
            f"wpkh({root_key.extend(internal_path).as_string()})",
            self.network,
        )
        # Log.i(TAG, "Descriptor for change addresses is $internalDescriptor")

    def get_last_unused_address(self) -> bdk.AddressInfo:
        return self.bdk_wallet.get_address(bdk.AddressIndex.LAST_UNUSED)

    def get_new_address(self) -> bdk.AddressInfo:
        return self.bdk_wallet.get_address(bdk.AddressIndex.NEW)

    def sync(self, log_progress=None) -> None:
        self.bdk_wallet.sync(self.blockchain, log_progress)

    def get_balance(self) -> bdk.Balance:
        return self.bdk_wallet.get_balance()

    def create_transaction(
        self, recipient: str, amount: int, fee_rate: float
    ) -> bdk.TxBuilderResult:
        script_pubkey = bdk.Address(recipient).script_pubkey()
        return (
            bdk.TxBuilder()
            .add_recipient(script_pubkey, amount)
            .fee_rate(sat_per_vbyte=fee_rate)
            .finish(self.bdk_wallet)
        )

    def sign(self, psbt: bdk.PartiallySignedTransaction) -> None:
        self.bdk_wallet.sign(psbt)

    def broadcast(self, signed_psbt: bdk.PartiallySignedTransaction) -> str:
        self.blockchain.broadcast(signed_psbt)
        return signed_psbt.txid()

    def get_transaction_history(self):  # -> List<TransactionDetails>
        # convert transactions to dict
        tx_list = map(vars, self.bdk_wallet.list_transactions())

        # get timestamp from confirmation_time, set to -1 if unconfirmed
        tx_list = list(map(Wallet.parse_timestamp, tx_list))

        # sort by ascending timestamp, convert details to string output
        sorted_list = sorted(tx_list, key=lambda x: x["confirmation_time"])
        tx_details = list(map(Wallet.parse_transaction_details, sorted_list))
        return tx_details

    @staticmethod
    def parse_timestamp(tx: dict) -> dict:
        if tx["confirmation_time"] is None:
            tx["confirmation_time"] = -1
        else:
            tx["confirmation_time"] = tx["confirmation_time"].timestamp
        return tx

    @staticmethod
    def parse_transaction_details(tx: dict) -> str:
        lines = []
        for k, v in tx.items():
            if k == "confirmation_time":
                if v == -1:
                    lines.append(f"Confirmation Time: unconfirmed")
                else:
                    dt = datetime.fromtimestamp(v).strftime("%Y-%m-%d %H:%M:%S")
                    lines.append(f"Confirmation Time: {dt}")
            else:
                lines.append(f"{k.capitalize().replace('_', ' ')}: {v}")
        return "\n".join(lines)
