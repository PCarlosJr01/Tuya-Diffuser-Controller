import json

import tinytuya


ON_SETTINGS = {
    1: True,
    11: True,
    12: 0,
    13: "0",
    14: 0,
    103: "small",
    108: "00aaff00c86464",
    109: "white",
    110: "2",
    111: 255,
}

OFF_SETTINGS = {
    1: False,
    11: False,
    12: 0,
    13: "0",
    14: 0,
    103: "off",
    108: "00aaff00c86464",
    109: "white",
    110: "2",
    111: 255,
}




def load_device():
    with open("devices.json", "r", encoding="utf-8") as file:
        devices = json.load(file)

    device_info = devices[0]

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
        print(f"DP {dp_id}: {response}")


def main():
    device = load_device()
    apply_settings(device, ON_SETTINGS)


if __name__ == "__main__":
    main()