import os
import bdkpython as bdk


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
        self.create_wallet()

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
