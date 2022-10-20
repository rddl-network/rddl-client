import urllib3
from .config import HW3_SERVICE


def create_seed(words: int):
    http = urllib3.PoolManager()
    mnemonic = http.request("GET", HW3_SERVICE + "/seed?number_of_words=" + str(words))
    return mnemonic.data.decode()


def recover_seed(mnemonic_phrase: str):
    http = urllib3.PoolManager()
    resp = http.request("POST", HW3_SERVICE + "/seed?mnemonic=" + mnemonic_phrase)
    return resp.data.decode()
