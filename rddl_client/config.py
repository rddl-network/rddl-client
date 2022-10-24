from decouple import config

HW_03_SERVICE = config("HW_03_SERVICE", default="http://localhost:8000")
TASMOTA_SERVICE = config("TASMOTA_SERVICE", default="http://sonoff")
