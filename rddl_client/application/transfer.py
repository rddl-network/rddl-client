import urllib3
import json
import ast

from rddl_client.config import HW_03_SERVICE


def transfer_tokens(transfer_description: dict):
    transfer_description["amount"] = str(transfer_description["amount"])
    transfer_description["is_confidential"] = transfer_description["confidential"]
    transfer_description["network_slip_id"] = transfer_description["nw_id"]
    transfer_description["network_slip_symbol"] = transfer_description["nw_symbol"]

    del transfer_description["confidential"]
    del transfer_description["nw_id"]
    del transfer_description["nw_symbol"]

    ast_data = ast.literal_eval(str(transfer_description))
    data = json.dumps(ast_data)

    http = urllib3.PoolManager()
    tx_id = http.request("POST", HW_03_SERVICE + "/wallet", headers={"Content-Type": "application/json"}, body=data)

    return tx_id.status, json.loads(tx_id.data.decode())
