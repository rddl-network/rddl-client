import urllib3
import json
from enum import Enum
from .config import HW3C_SERVICE


def store(data: dict):
    http = urllib3.PoolManager()
    cid_resp = http.request("POST", HW3C_SERVICE + "/data", headers={"Content-Type": "application/json"}, body=data)
    return cid_resp.data.decode()


def get_energy_data():
    # http = urllib3.PoolManager()
    # consumption = http.request("GET", "http://sonoff/cm?cmnd=Status%208")
    # return consumption.data.decode()
    import datetime

    x = str(datetime.datetime.now())
    dd = {
        "StatusSNS": {
            "Time": x,
            "ENERGY": {
                "TotalStartTime": x,
                "Total": 0.782,
                "Yesterday": 0.421,
                "Today": 0.182,
                "Power": 17,
                "ApparentPower": 41,
                "ReactivePower": 37,
                "Factor": 0.43,
                "Voltage": 230,
                "Current": 0.177,
            },
            "ESP32": {"Temperature": 26.7},
            "TempUnit": "C",
        }
    }
    return json.dumps(dd)


def attest_cid(cid: str):
    http = urllib3.PoolManager()
    tx_id = http.request("POST", HW3C_SERVICE + "/cid?cid=" + cid)
    return tx_id.data.decode()


def attest_machine(machine_descripion: dict):
    data = json.dumps(machine_descripion)
    http = urllib3.PoolManager()
    tx_id = http.request("POST", HW3C_SERVICE + "/machine", headers={"Content-Type": "application/json"}, body=data)
    return tx_id.data.decode()


def get_and_attest_energy():
    data = get_energy_data()
    cid = store(data)
    print(f"CID: {cid}")
    tx_id = attest_cid(cid)
    print(f"TX ID: {tx_id}")
    print(f"https://test.ipdb.io/api/v1/transactions/{json.loads(tx_id)['NFT token']}")


# get_and_attest_energy()
