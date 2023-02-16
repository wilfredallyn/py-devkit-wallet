import bdkpython as bdk
import pickle
from typing import Type


class Repository(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Repository, cls).__new__(cls)
        return cls._instance

    def __init__(self, pkl_file, data=None) -> None:
        # log pkl_file path
        if data:
            self.data = data
        else:
            self.data = {}
        self.pkl_file = pkl_file

    def persist(self) -> None:
        with open(self.pkl_file, "wb") as f:
            pickle.dump(self.data, f)

    @staticmethod
    def load(pkl_file) -> Type["Repository"]:
        with open(pkl_file, "rb") as f:
            data = pickle.load(f)
        return Repository(pkl_file=pkl_file, data=data)

    def save_wallet(
        self, external_descriptor: bdk.Descriptor, internal_descriptor: bdk.Descriptor
    ) -> None:
        # Log.i(
        #     TAG,
        #     "Saved wallet:\npath -> $path \ndescriptor -> $descriptor \nchange descriptor -> $changeDescriptor"
        # )
        self.data["wallet_initialized"] = True
        self.data["external_descriptor"] = external_descriptor.as_string()
        self.data["internal_descriptor"] = internal_descriptor.as_string()

    def save_mnemonic(self, mnemonic: str) -> None:
        # Log.i(TAG, "The recovery phrase is: $mnemonic")
        self.data["mnemonic"] = mnemonic.as_string()

    def get_mnemonic(self) -> str:
        return self.data["mnemonic"]
