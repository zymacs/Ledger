import json
import uuid
from datetime import datetime
from interactive import record_transaction

from utils import custom_input, is_numeric, get_date, clear

default_currency = 'TL'

def fx(source, dest, amt):
    pass


def load_accounts():
    with open('accounts.json','r') as f:
        accounts = json.load(f)
    if 'accounts' not in accounts:
        accounts['accounts'] = {}
    return accounts

def update_accounts(accounts):
    with open("accounts.json","w") as f:
        json.dump(accounts,f, indent=4)


accounts = load_accounts()

def create_account(ac_name, ac_code, ac_currency, ac_type, init_bal):
    new_account = {
        'ac_name': ac_name,
        'ac_bal': float(init_bal),
        'date_created': get_date(),
        'ac_type': ac_type,
        'ac_code': ac_code,
        'currency': currency
    }
    ac_id = str(uuid.uuid4())
    new_account['id'] = ac_id
    accounts['accounts'][ac_id] = new_account
    update_accounts(accounts)
    return ac_id




def load_records():
    with open("records.json", "r") as f:
        data = json.load(f)
    if 'records' not in data:
        data['records'] = {}
    return data

old_records = load_records() 

def update_records(records):
    print("Updating records")
    with open("records.json", "w") as f:
        json.dump(records, f, indent=4)

    
def create_transaction(args):
    t_id = str(uuid.uuid4())
    t_date = get_date()
    da_id = args[0]
    sa_id = args[1]
    t_amt = args[2]
    t_notes = args[3]
    t_units = args[4] 
    t_qty =  args[5] 
    t_meta = args[6] 

    new_record = {
            'id': t_id,
            'date': t_date,
            'amt': float(t_amt),
            'sa_id': sa_id,
            'da_id': da_id,
            'notes': t_notes
            }
    if t_units:
        new_record['units'] = t_units
    if t_qty:
        new_record['qty'] = float(t_qty)
    if t_meta:
        new_record['meta'] = t_meta

    old_records['records'][new_record['id']] = new_record
    update_records(old_records)
    return new_record

def ac_handler(cmd):
    '''
    ac related actions handler
    '''
    print("handling account")
    print(cmd)


def show_handler(cmd):
    '''
    show:
    - accounts
    - transactions
    - filtering supported
    '''
    print(f"Showing  {cmd}")


def get_account_by_code(account_code, accounts):
    print(f"Getting account for : {account_code}")
    account_ids = list(accounts.keys())
    for account in accounts:
        if accounts[account]['ac_code'] == account_code:
            return (accounts[account], account)
    return None
    
def transfer_funds(args):
    if len(args) < 3:
        print("Insufficient args")
        return

    records = load_records()
    accounts = load_accounts()
    
    ac1, ac1_id = get_account_by_code(args[0], accounts['accounts'])
    if ac1 is None:
        print(f"No such code: {args[0]}")
        return
    ac2, ac2_id = get_account_by_code(args[1], accounts['accounts'])
    if ac2 is None:
        print(f"No such code: {args[1]}")
        return
    print(f"Moving {args[2]}Munits from {ac1['ac_name']} to {ac2['ac_name']}")
    if ac1['ac_type'] != 'Equity':
        ac1['ac_bal'] -= float(args[2])
    else:
        ac1['ac_bal'] += float(args[2])
    ac2['ac_bal'] += float(args[2])
    print("Updating accounts")
    update_accounts(accounts)
    amt = args[2]
    tr_reason = "Moving money" if len(args) < 4 else args[3]
    tr_date  = get_date()
    sa_id = ac1_id
    da_id = ac2_id
    tr_units = None if len(args) < 5 else args[4]
    tr_qty = None if len(args) < 6 else args[5]
    tr_meta = None if len(args) < 7 else args[6]
    create_transaction([da_id, sa_id, amt, tr_reason, tr_units, tr_qty, tr_meta]) 
    print("Transaction complete")
    
    
    
def transfer_handler(cmd):
    '''
    transfer handler
    - tr from to
    - parse args
    - validate args
    - execute command
    - return 
    '''
    
    tokens = cmd.split()
    print(f"Tokens: {tokens}")
    transfer_funds(tokens)
    
def get_accounts():
    accounts = load_accounts()
    return accounts['accounts']

def history(ac_code):
    pass

def get_total_bal():
    pass

def ls_handler(cmd):
    '''
    ls account_codes # show account codes
    ls transactions # show past transactions
    ls vendors # show expense accounts
    
    '''
    supported_args = 'account_codes vendors transactions ac_codes accounts'.split()
    tokens = cmd.split()
    if len(tokens) == 0:
        return
    for token in tokens:
        if token == 'accounts':
            accounts = get_accounts()
            for i,account in enumerate(accounts):
                print(f"{i:4}  {accounts[account]['ac_code']:6} {accounts[account]['ac_name']:20} {accounts[account]['ac_type']:15}"\
                         f" {accounts[account]['ac_bal']:<10} {accounts[account]['currency']}")
        elif token == 'transactions':
            pass
        elif token == 'vendors':
            pass
        elif token == 'assets':
            accounts = get_accounts()
            for i,account in enumerate(accounts):
                if accounts[account].get('ac_type') == 'Asset':
                    print(f"{i:4}  {accounts[account]['ac_code']:6} {accounts[account]['ac_name']:20}"\
                              f"{accounts[account]['ac_bal']:<10} {accounts[account]['currency']}")

        else:
            print(f"No handler defined for {token}")


def touch_handler(cmd):
    tokens = cmd.split()
    if len(tokens) < 6:
        print("Insufficient args")
        return
    ac_name = tokens[0]
    ac_code = tokens[1]
    ac_currency = tokens[2]
    ac_type = tokens[3]
    initial_bal = tokens[4]
    currency = tokens[5]
    ac_id = create_account(ac_name, ac_code, ac_currency, ac_type, initial_bal, currency)
    print(f"New account created with id: {ac_id}")


def mod_handler():
    pass

def help_handler(cmd):
    tokens = cmd.split()
    if len(tokens) > 1:
        print("Too many supplied args")
        return
    if tokens[0] == "touch":
        print("touch ac_name ac_code ac_currency ac_type init_bal currency")
    elif tokens[0] == "mv" or tokens[0] == "tr":
        print("mv source destination amt reason [units, qty, meta]")

def cmd_parser(cmd):
    if cmd == 'exit':
        exit()
    elif cmd.startswith('tr '):
        transfer_handler(cmd.lstrip('tr'))
    elif cmd.startswith('mv '):
        transfer_handler(cmd.lstrip('mv'))
    elif cmd.startswith('ac '):
        ac_handler(cmd.lstrip('ac').strip())
    elif cmd.startswith('ls '):
        ls_handler(cmd.lstrip('ls').strip())
    elif cmd.startswith('touch'):
        touch_handler(cmd.lstrip('touch ').strip())
    elif cmd.startswith('help '):
        help_handler(cmd.lstrip('help').strip())
    elif cmd == 'clear':
        clear()
    else:
        print(cmd)
    

def get_cmd():
    next_cmd = custom_input("$ ")
    return next_cmd
    
def prompt_cli():
    clear()
    print(".....LEDGER-CLI.....")
    while True:
        next_cmd = get_cmd()
        cmd_parser(next_cmd)

   
if __name__ == '__main__':
    try:
        prompt_cli()
    except KeyboardInterrupt:
        print("Exiting")
        os.system('clear')
        exit()
    except Exception as e:
        print(f'Error: {e}')
