import requests
import uuid


def register_device(license_key, name):
    form_url = 0
    hwid = str(uuid.getnode())
    print(hwid)


if __name__ == "__main__":
    register_device(license_key="udvash", name="Mahbub")
