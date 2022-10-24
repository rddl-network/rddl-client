import urllib3
import json
from .config import HW_03_SERVICE
from .config import TASMOTA_SERVICE


def store(data: dict):
    http = urllib3.PoolManager()
    cid_resp = http.request("POST", HW_03_SERVICE + "/data", headers={"Content-Type": "application/json"}, body=data)
    return cid_resp.data.decode()


def get_energy_data():
    http = urllib3.PoolManager()
    consumption = http.request("GET", TASMOTA_SERVICE + "/cm?cmnd=Status%208")
    return consumption.data.decode()


def get_fake_energy_data():
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
    tx_id = http.request("POST", HW_03_SERVICE + "/cid?cid=" + cid)
    return tx_id.data.decode()


def attest_machine(machine_descripion: dict):
    data = json.dumps(machine_descripion)
    http = urllib3.PoolManager()
    tx_id = http.request("POST", HW_03_SERVICE + "/machine", headers={"Content-Type": "application/json"}, body=data)
    return tx_id.data.decode()


def get_0x21e8_config():
    http = urllib3.PoolManager()
    cfg = http.request("GET", HW_03_SERVICE + "/config", headers={"Content-Type": "application/json"})
    return cfg.data.decode()


def get_and_attest_energy():
    data = get_fake_energy_data()
    cid = store(data)
    print(f"CID: {cid}")
    tx_id = attest_cid(cid)
    print(f"TX ID: {tx_id}")
    cfg = get_0x21e8_config()
    # print( cfg)
    # print(f"{ cfg['planetmint'] }/api/v1/transactions/{json.loads(tx_id)['NFT token']}")
