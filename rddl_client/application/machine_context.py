import urllib3
import json
import ast


def get_geolocation_data(dns_name: str):
    http = urllib3.PoolManager()
    geolocation_data = http.request(
        "GET",
        "https://tools.keycdn.com/geo.json?host=" + dns_name,
        headers={"User-Agent": "keycdn-tools:https://" + dns_name},
    )
    decoded_geo_data = geolocation_data.data.decode()
    return json.loads(decoded_geo_data)


def metadata_object(id: int) -> dict:
    dns_name = "node" + str(id) + "-rddl-testnet.twilightparadox.com"
    device_dict = None
    with open("device_info.json", "r") as file:
        data = file.read().rstrip()
        device_dict = ast.literal_eval(data)
    metadata_obj = {
        "GPS": get_geolocation_data(dns_name),
        "Device": device_dict,
        "Asset Definition": {
            "VersionControl": {"PASStandardVersionNumber": "PAS19668:2020", "SecurityTokenFileVersionNumber": "1.0.0"},
            "SecurityTokenDataStore": "https://linktoyoursecuritytokenwebsite.com/pasdata/current_version.json",
            "SecurityTokenLocation": {
                "STBlockchain": [
                    {
                        "STBlockchainName": "Liquid",
                        "STBlockchainInformation": "https://blockstream.com/liquid/",
                        "STTokenizationSolution": ["RDDL Asset Registry"],
                        "STBlockchainUniqueAssetIdentifier": "a28d04f3e243a9a187f4a8b797be2f19a9c01b6ef4e1d65bfb6abbd6a2042097",
                        "ProgrammationOfSecurityToken": "ProgramCryptoConditions",
                        "SecurityTokenTransferVerificationLogic": "VerificationPreTransfer",
                        "SecurityProcedures": ["CapableFreezeAccount", "CapableFreezeST"],
                    }
                ],
                "STIdentificationNumber": "Asset identification according to BS ISO 6166",
            },
            "SecurityTokenClassification": {"IdentificationOfST": {"CFICodeVersion": "1.0", "CFICodeValue": "CFI001"}},
            "InformationDisclosures": {
                "IssuerDisclosures": {
                    "IssuerName": "RDDL Foundation",
                    "IssuerIndustryClassification": "604885180106232618",
                    "IssuerJurisdiction": "LI",
                    "IssuerContactDetails": "c/o at4you AG, Rhigass 1, 9487 Gamprin-Bendern, Liechtenstein",
                    "IssuerNewsFeed": ["https://twitter.com/RDDLNetwork"],
                    "IssuerIncorporationDocuments": "https://rddl.io/incorporation.doc",
                    "IssuerOfferingDocuments": "https://rddl.io/offering.doc",
                    "IssuerAccountInformation": "https://rddl.io/accounting.doc",
                },
                "IssuerAssetDisclosures": {
                    "STTotalSupply": 1,
                    "STFractionalization": True,
                    "STAssetInvestmentProfile": "https://rddl.io/InvestmentProfile",
                    "STMarkets": ["https://rddl.io"],
                    "STPriceDetermination": "STMarketPrice",
                    "AssetBacking": "AssetBacked",
                    "AssetCustodianship": "AssetCustodied",
                    "AssetCustodian": "RDDL Foundation",
                },
            },
            "EligibleInvestorClassification": {"EligibleInvestorCountriesList": [], "RestrictedCountries": ["LI"]},
            "SecurityTokenTechnicalProperties": {
                "IncomeProperties": "IncomeDifferentAddress",
                "VotingProperties": "NoVoting",
                "DelegateRegister": "DelegateTA",
            },
            "KYCAMLRequirements": {"IdentityDocuments": "Passport", "ComplianceRequirements": ""},
        },
    }
    return metadata_obj


def machine_description(id: int, metadata_cid: str) -> dict:
    machine_obj = {
        "name": "RDDL Validator " + str(id),
        "ticker": "RDDLV" + str(id),
        "amount": 1,
        "precision": 8,
        "public_url": "https://rddl.io",
        "reissue": True,
        "cid": metadata_cid,
        ## the following entries are added by the 0x21e8 service
        # "machine id": "machine identity of the secure element",  # skipped right now
        # "issuer_liquid": "m/44/LBTC/0/0/0",  # to be defined (programatically)
        # "issuer_planetmint": "m/44/PLMNT/0/0/0",  # to be defined (programatically)
    }
    return machine_obj
