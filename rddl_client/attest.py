import urllib3
import json
import ast
from .config import HW_03_SERVICE
from .config import TASMOTA_SERVICE


def store(data: dict, encrypt: bool = False):
    http = urllib3.PoolManager()
    dict_string = json.dumps(data)
    cid_resp = http.request(
        "POST",
        HW_03_SERVICE + "/data?encrypt=" + str(encrypt),
        headers={"Content-Type": "application/json"},
        body=dict_string,
    )
    cid_str = cid_resp.data.decode()
    cid_dict = ast.literal_eval(cid_str)
    return cid_dict


def get_energy_data():
    http = urllib3.PoolManager()
    consumption = http.request("GET", TASMOTA_SERVICE + "/cm?cmnd=Status%208")
    data = consumption.data.decode()
    cid_dict = ast.literal_eval(data)
    return cid_dict


def get_fake_energy_data():
    import datetime

    x = str(datetime.datetime.now())
    data_dict = {
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
    return data_dict


def attest_cid(cid: str):
    http = urllib3.PoolManager()
    tx_id = http.request("POST", HW_03_SERVICE + "/assets?cid=" + cid)
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
    data = get_energy_data()
    cid_dict = store(data, False)
    tx_id = attest_cid(cid_dict["cid"])
    print(f"TX ID: {tx_id}")
