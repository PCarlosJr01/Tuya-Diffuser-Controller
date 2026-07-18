import os

from dotenv import load_dotenv
from tuya_connector import TuyaOpenAPI


def main():
    load_dotenv()

    endpoint = os.getenv("TUYA_ENDPOINT")
    access_id = os.getenv("TUYA_ACCESS_ID")
    access_secret = os.getenv("TUYA_ACCESS_SECRET")

    if not endpoint or not access_id or not access_secret:
        print("Missing Tuya credentials in .env")
        return

    openapi = TuyaOpenAPI(
        endpoint,
        access_id,
        access_secret,
    )

    response = openapi.connect()

    if response.get("success"):
        print("Connected to Tuya Cloud successfully.")
    else:
        print("Failed to connect to Tuya Cloud.")
        print(response)


if __name__ == "__main__":
    main()