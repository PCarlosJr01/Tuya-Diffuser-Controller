MENU = """
==================================================
              Tuya Device Controller
==================================================

Available selections:

  on     Turn the device on
  off    Turn the device off
  clear  Clear cached credentials
  exit   Quit the application

==================================================
"""


def cli_selection():
    print(MENU)


def cli_invalid_input():
    print()
    print("Invalid selection. Please choose one of the options below.")
    print(MENU)


def cli_clear_credentials():
    print()
    print("Cached credentials cleared successfully.")
    print()


def cli_using_cached_credentials(file_path):
    print()
    print("Using cached credentials:")
    print(f"  {file_path}")
    print()


def cli_create_credentials_choice():
    print()
    print("No cached credentials were found.")
    print()

    return input(
        "Create new credentials? Enter 'y' to continue "
        "or any other input to exit: "
    ).strip().lower()