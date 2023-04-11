from dmidecode import DMIDecode

dmi = DMIDecode()
print(dmi.data["0x0001"])
