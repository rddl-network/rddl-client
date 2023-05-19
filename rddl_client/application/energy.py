import ast
import urllib3
from rddl_client.config import TASMOTA_SERVICE


def get_energy_data():
    http = urllib3.PoolManager()
    consumption = http.request("GET", TASMOTA_SERVICE + "/cm?cmnd=Status%208")
    data_str = consumption.data.decode()
    return data_str


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
