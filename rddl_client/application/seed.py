import urllib3
from rddl_client.config import HW_03_SERVICE


def create_seed(words: int):
    http = urllib3.PoolManager()
    mnemonic = http.request("GET", HW_03_SERVICE + "/seed?number_of_words=" + str(words))
    return mnemonic.data.decode()


def recover_seed(mnemonic_phrase: str):
    http = urllib3.PoolManager()
    resp = http.request("POST", HW_03_SERVICE + "/seed?mnemonic_phrase=" + mnemonic_phrase)
    return resp.data.decode()
