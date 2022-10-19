import urllib3
import json
from enum import Enum
from .config import HW3C_SERVICE


def create_seed(words: int):
    http = urllib3.PoolManager()
    mnemonic = http.request("GET", HW3C_SERVICE + "/seed?number_of_words=" + str(words))
    return mnemonic.data.decode()


def recover_seed(mnemonic_phrase: str):
    http = urllib3.PoolManager()
    resp = http.request("POST", HW3C_SERVICE + "/seed?mnemonic=" + mnemonic_phrase)
    return resp.data.decode()
