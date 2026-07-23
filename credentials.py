import subprocess
import sys
from pathlib import Path


def create_credentials(file_path: Path):
    print("Starting TinyTuya credential setup.")
    print()

    file_path.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tinytuya",
            "wizard",
        ],
        cwd=file_path.parent,
        check=False,
    )

    if result.returncode != 0:
        print("TinyTuya setup was canceled or failed.")
        return False

    if not file_path.is_file():
        print("TinyTuya completed, but devices.json was not created.")
        return False

    print()
    print("Device credentials created successfully.")
    return True


def delete_credentials(file_path: Path):
    if not file_path.is_file():
        print("No cached credentials were found.")
        return False

    file_path.unlink()

    print("Cached credentials deleted successfully.")
    return True