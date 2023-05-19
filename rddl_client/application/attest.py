import urllib3
import json
import ast

from rddl_client.application.energy import get_energy_data
from rddl_client.config import HW_03_SERVICE
from rddl_client.config import TASMOTA_SERVICE

APPLICATION_JSON = "application/json"


def store(data: str, encrypt: bool = False):
    http = urllib3.PoolManager()
    cid_resp = http.request(
        "POST",
        HW_03_SERVICE + f"/data?data={data}&encrypt=" + str(encrypt),
        headers={"Content-Type": APPLICATION_JSON},
    )
    cid_str = cid_resp.data.decode()
    cid_dict = ast.literal_eval(cid_str)
    return cid_dict


def attest_cid(cid: str):
    http = urllib3.PoolManager()
    tx_id = http.request("POST", HW_03_SERVICE + "/assets?cid=" + cid)
    return tx_id.data.decode()


def attest_machine(machine_descripion: dict):
    data = json.dumps(machine_descripion)
    http = urllib3.PoolManager()
    tx_id = http.request("POST", HW_03_SERVICE + "/machine", headers={"Content-Type": APPLICATION_JSON}, body=data)
    return tx_id.data.decode()


def get_0x21e8_config():
    http = urllib3.PoolManager()
    cfg = http.request("GET", HW_03_SERVICE + "/config", headers={"Content-Type": APPLICATION_JSON})
    return cfg.data.decode()


def get_and_attest_energy():
    data = get_energy_data()
    print(f"data : {data}")
    cid_dict = store(data, False)
    print(f"cid : {cid_dict}")
    tx_id = attest_cid(cid_dict["cid"])
    print(f"TX ID: {tx_id}")
