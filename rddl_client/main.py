import typer
import json

from .attest import store, get_and_attest_energy, attest_cid, attest_machine
from .seed import create_seed, recover_seed


app = typer.Typer()


@app.command("attest-machine")
def cmd_attest_machine(name: str, ticker: str, amount: int, precision: int, public_url: str, reissue: bool, cid: str):
    machine_description = {
        "name": name,
        "ticker": ticker,
        "amount": amount,
        "precision": precision,
        "public_url": public_url,
        "reissue": reissue,
        "cid": cid,
    }
    resp = attest_machine(machine_description)
    print(resp)


@app.command("attest-data")
def cmd_attest_data(data: str):
    json_data = json.dumps(data)
    cid = store(json_data)
    print(f"cid: {cid}")
    tx_id = attest_cid(cid)
    print(f"tx_id: {tx_id}")


@app.command("attest-energy-consumption")
def cmd_attest_energy_consumption():
    get_and_attest_energy()


@app.command("create-seed")
def cmd_create_seed(words: int = 24):
    if words not in [12, 24]:
        print("Pleaes provide a recovery list with 12 or 24 words.")

    mnemonic = create_seed(words)
    print(f"MNEMONIC PHRASE: {mnemonic}")


@app.command("recover-seed")
def cmd_recover_seed(mnemonic_phrase: str):
    word_array = mnemonic_phrase.split()
    size = len(word_array)
    if size not in [12, 24]:
        print("Pleaes provide a recovery list with 12 or 24 words.")

    for word in word_array:
        if not isinstance(word, str):
            print("The recovery word list is invalid it must contain strings.")

    resp = recover_seed(mnemonic_phrase)
    print(resp)


if __name__ == "__main__":
    app()
