import typer
import ast

from rddl_client.attest import store, get_and_attest_energy
from rddl_client.attest import attest_cid, attest_machine, get_0x21e8_config
from rddl_client.seed import create_seed, recover_seed
from rddl_client.machine_context import metadata_object, machine_description

app = typer.Typer()


@app.command("attest-validator")
def cmd_attest_machine_with_cid(
    id: int = typer.Argument(
        ...,
        min=0,
        max=10000,
        help="The validator id. The IP geolocation and machine data as well as the default asset definition are created.",
    ),
):
    metadata_obj = metadata_object(id)
    metadata_cid = store(metadata_obj, False)
    print(f"Metadata CID: {metadata_cid['cid']}")

    """
    This method issues the requested machine tokens for the machine on RDDL and notarizes the machine and the issued tokens.
    """
    machine_desc_obj = machine_description(id, metadata_cid["cid"])
    print(f"Machine description: {machine_desc_obj}")
    resp = attest_machine(machine_desc_obj)
    print(resp)


@app.command("attest-machine")
def cmd_attest_machine_with_cid(
    name: str = typer.Argument(..., help="The name of the machine token that will be issued."),
    ticker: str = typer.Argument(..., help="The ticker of the machine token that will be issued."),
    amount: int = typer.Argument(..., help="The number of tokens that are to be issued."),
    precision: int = typer.Argument(..., help="The precision of the token."),
    public_url: str = typer.Argument(..., help="The legal entity that this machine and token are associated with."),
    reissue: bool = typer.Option(True, "--reissue/--no-reissue"),
    cid: str = typer.Argument(
        None,
        help="The CID of the token details. This needs to created and handled before calling this method. In case this is not defined, the IP geolocation and machine data as well as the default asset definition are created.",
    ),
):
    """
    This method issues the requested machine tokens for the machine on RDDL and notarizes the machine and the issued tokens.
    """
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
def cmd_attest_data(
    data: str = typer.Argument(
        ..., help="A dcit object in string representation that is to be stored on IPFS and attested on RDDL."
    ),
    encrypt: bool = typer.Option(False, "--encrypt"),
):
    """
    This method stores the given JSON data on the configured storage solution and notarizes the resulting CID on RDDL, thereafter.
    """
    data_dict = ast.literal_eval(data)
    cid_dict = store(data_dict, encrypt)
    print(f"{cid_dict}")
    raw_cid = cid_dict["cid"]
    tx_id = attest_cid(raw_cid)
    print(f"tx_id: {tx_id}")


@app.command("attest-energy-consumption")
def cmd_attest_energy_consumption():
    """
    Reads out the energy meter and notarizes the data on-chain.
    """
    get_and_attest_energy()


@app.command("service-config")
def cmd_get_config():
    """
    Shows the configuration of the 0x21e8 Keymanagement Service.
    """
    cfg = get_0x21e8_config()
    print(f"CONFIG : {cfg}")


@app.command("create-seed")
def cmd_create_seed(
    words: int = typer.Argument(
        24, help="The number of words (12 or 24) that the mnemonic phrase to be derived should contain."
    )
):
    """
    Creates a seed based on true randomness and provices a mnemonic phrase (12 or 24 words) as a backup of the generated seed.
    The lenght of the resulting mnemonic phrase implicitly defines the lenght of the seed.
    """
    if words not in [12, 24]:
        print("Pleaes provide a recovery list with 12 or 24 words.")

    mnemonic = create_seed(words)
    print(f"MNEMONIC PHRASE: {mnemonic}")


@app.command("recover-seed")
def cmd_recover_seed(
    mnemonic_phrase: str = typer.Argument(..., help="The mnemonic phrase, a space seperated list of 12 or 24 words")
):
    """
    Recovers a seed from the menmonic phrase passed to the method (12 or 24 words).
    The lenght of the resulting mnemonic phrase implicitly defines the lenght of the seed.
    """
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
