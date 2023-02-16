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

    def save_wallet(self, external_descriptor: str, internal_descriptor: str) -> None:
        # Log.i(
        #     TAG,
        #     "Saved wallet:\npath -> $path \ndescriptor -> $descriptor \nchange descriptor -> $changeDescriptor"
        # )
        self.data["wallet_initialized"] = True
        self.data["external_descriptor"] = external_descriptor
        self.data["internal_descriptor"] = internal_descriptor

    def save_mnemonic(self, mnemonic: str) -> None:
        # Log.i(TAG, "The recovery phrase is: $mnemonic")
        self.data["mnemonic"] = mnemonic.as_string()

    def get_mnemonic(self) -> str:
        return self.data["mnemonic"]
