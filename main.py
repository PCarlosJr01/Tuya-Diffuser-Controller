import json
from pathlib import Path

import tinytuya

from cli import cli_clear_credentials,   cli_create_credentials_choice,  cli_invalid_input,  cli_selection,  cli_using_cached_credentials
from config import OFF_SETTINGS, ON_SETTINGS
from credentials import create_credentials, delete_credentials


BASE_DIR = Path(__file__).resolve().parent
DEVICE_FILE = BASE_DIR / "device_data" / "devices.json"


def load_device():
    if not DEVICE_FILE.is_file():
        raise FileNotFoundError(
            f"Device configuration file not found:\n{DEVICE_FILE}"
        )

    with DEVICE_FILE.open("r", encoding="utf-8") as file:
        devices = json.load(file)

    if not devices:
        raise ValueError("No devices were found in devices.json.")

    device_info = devices[0]

    required_fields = ("id", "ip", "key", "version")

    for field in required_fields:
        if field not in device_info:
            raise KeyError(f"Missing '{field}' in devices.json.")

    device = tinytuya.Device(
        device_info["id"],
        device_info["ip"],
        device_info["key"],
    )

    device.set_version(float(device_info["version"]))

    return device


def apply_settings(device, settings):
    for dp_id, value in settings.items():
        response = device.set_value(dp_id, value)

        if response is None:
            continue

        if isinstance(response, dict) and response.get("Error"):
            print(f"Failed to set DP {dp_id}: {response}")
            return False

    return True


def run_controller():
    cli_using_cached_credentials(DEVICE_FILE)
    cli_selection()

    device = load_device()

    while True:
        user_setting = input("Enter a selection: ").strip().lower()

        if user_setting == "on":
            if apply_settings(device, ON_SETTINGS):
                print("Diffuser settings applied successfully.")

        elif user_setting == "off":
            if apply_settings(device, OFF_SETTINGS):
                print("Diffuser settings applied successfully.")

        elif user_setting == "clear":
            if delete_credentials(DEVICE_FILE):
                cli_clear_credentials()
                return

        elif user_setting == "exit":
            raise SystemExit

        else:
            cli_invalid_input()


def main():
    while True:
        try:
            if DEVICE_FILE.is_file():
                run_controller()
                continue

            print("No cached credentials found.")

            create_credentials_choice = cli_create_credentials_choice()

            if create_credentials_choice != "y":
                return

            if not create_credentials(DEVICE_FILE):
                return

        except FileNotFoundError as error:
            print(error)

        except json.JSONDecodeError as error:
            print(f"devices.json contains invalid JSON: {error}")

        except (KeyError, ValueError, TypeError) as error:
            print(f"Invalid device configuration: {error}")

        except SystemExit:
            return

        except KeyboardInterrupt:
            print()
            print("Exiting diffuser controller.")
            return

        except Exception as error:
            print(f"Unable to control diffuser: {error}")


if __name__ == "__main__":
    main()