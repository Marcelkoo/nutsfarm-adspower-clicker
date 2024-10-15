from prettytable import PrettyTable

balances = []

def read_accounts_from_file():
    with open('accounts.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

def write_accounts_to_file(accounts):
    with open('accounts.txt', 'w') as file:
        for account in accounts:
            file.write(f"{account}\n")

def reset_balances():
    global balances
    balances = []

def update_balance_table(serial_number, balance):
    global balances
    for i, (serial, bal) in enumerate(balances):
        if serial == serial_number:
            balances[i] = (serial_number, balance)
            return
    balances.append((serial_number, balance))

def print_balance_table():
    table = PrettyTable()
    table.field_names = ["Serial Number", "Balance"]
    for serial, bal in balances:
        table.add_row([serial, bal])
    print(table)
