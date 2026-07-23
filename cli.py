def cli_selection():
    print("""
Available selections:

on    - Turn the diffuser on
off   - Turn the diffuser off
exit  - Quit the application
clear - clear the cached credentials
    """)

def cli_invalid_input():
        print("""
Invalid input please select from the following :

on    - Turn the diffuser on
off   - Turn the diffuser off
exit  - Quit the application
clear - clear the cached credentials
    """)

def cli_clear_credentials():
    print("""
Cached credentials cleared.

""")

def cli_using_cached_credentials(file_path):
    print("""
Using cached credentials from:  
""" + str(file_path))

def cli_create_credentials_choice():
    return input("""
Do you want to create new credentials? 
Enter 'y' or any other input to exit: 
    """).strip().lower()