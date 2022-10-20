from decouple import config

HW3_SERVICE = config("HW3_SERVICE", default="http://localhost:8000")
