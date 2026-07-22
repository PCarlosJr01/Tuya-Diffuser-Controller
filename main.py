import json
from pathlib import Path

import tinytuya

from settings import OFF_SETTINGS, ON_SETTINGS


BASE_DIR = Path(__file__).resolve().parent
DEVICE_FILE = BASE_DIR / "device_data" / "devices.json"


def load_device():
    if not DEVICE_FILE.exists():
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

def print_selection():
    print("Available selections:")
    print("  on - Turn the diffuser on")
    print("  off - Turn the diffuser off")
    print("  exit - Quit the application")

def create_credentials(file_path):
    print("Creating new credentials.")
    print("")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.touch()



def main():
    file_path = Path("credentials") / "credentials.txt"

    while True:
        if file_path.is_file():
            print("Using cached credentials from file.")
            print_selection()

            try:
                device = load_device()

                while True:
                    user_setting = input("Enter a selection: ")

                    if user_setting == "on":
                        if apply_settings(device, ON_SETTINGS):
                            print("Diffuser settings applied successfully.")

                    elif user_setting == "off":
                        if apply_settings(device, OFF_SETTINGS):
                            print("Diffuser settings applied successfully.")

                    elif user_setting == "exit":
                        return

                    else:
                        print("Invalid input. Please enter 'on', 'off', or 'exit'.")

            except FileNotFoundError as error:
                print(error)

            except json.JSONDecodeError as error:
                print(f"devices.json contains invalid JSON: {error}")

            except (KeyError, ValueError, TypeError) as error:
                print(f"Invalid device configuration: {error}")

            except Exception as error:
                print(f"Unable to control diffuser: {error}")

        else:
            print("No cached credentials found.")

            create_credentials(file_path)




if __name__ == "__main__":
    main()