import importlib.util
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"
MAIN_FILE = BASE_DIR / "main.py"


def dependencies_installed():
    return importlib.util.find_spec("tinytuya") is not None


def install_requirements():
    if not REQUIREMENTS_FILE.is_file():
        print(f"requirements.txt was not found:\n{REQUIREMENTS_FILE}")
        return False

    print("Installing required dependencies...")
    print()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(REQUIREMENTS_FILE),
        ],
        check=False,
    )

    if result.returncode != 0:
        print()
        print("Dependency installation failed.")
        return False

    print()
    print("Dependencies installed successfully.")
    return True


def run_application():
    result = subprocess.run(
        [sys.executable, str(MAIN_FILE)],
        cwd=BASE_DIR,
        check=False,
    )

    if result.returncode != 0:
        print("The diffuser controller exited with an error.")


def main():
    if not dependencies_installed():
        print("Required dependencies are missing.")
        print()

        if not install_requirements():
            return

    run_application()


if __name__ == "__main__":
    main()