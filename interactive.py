
def get_input(prompt, dtype='string', nullable=False, rm=None): # rm: return mappings
    user_input =  input(prompt)
    while not user_input and not nullable:
        print("Field does not accept null input ")
        user_input = input(prompt)
    print('User input is: ', user_input)
    if user_input == '':
        return None
    if dtype != "string":
        while not is_numeric(user_input):
            print("Please enter numeric input only")
            user_input = input(prompt)
        return float(user_input)
    else:
        while is_numeric(user_input):
            print("String input please")
            user_input = input(prompt)
        if rm is not None:
            return rm[user_input.lower()]
        return user_input

 

def get_choice(choices):
    for i, c in enumerate(choices):
        print(i+1, ' ' , c)
    print(f"Choose one of {choices}")
    choice = int(get_input("Enter choice: ", dtype='int'))
    while not choice >= 1 and not choice <= i+1:
        print(f"Choice must be within the range: 1 to {i+1}")
        
        choice = int(get_input("Enter choice: ", dtype='int'))
    return choices[choice-1]
    



def get_account(prompt):
    create_new = get_input("Create new account? [y/n] ", rm={'y':True, 'n':False})
    if create_new:
        return create_new_account()
    print("Choosing: ", prompt)
    account_ids = [g for g in [f for f in accounts.values()][0].keys()]
    account_names = [(aid, accounts['accounts'][aid]['ac_name']) for aid in account_ids]
    user_choice = get_choice(account_names)
    return user_choice[0]




def create_new_account(initial_bal=0):
    ac_name = get_input("Enter account name: ")
    ac_code = get_input("Enter account nickname or code: ")
    init_bal  = get_input("Enter account initial bal: ", dtype="float", nullable=True) or 0
    ac_type = get_choice("Asset Equity Liability Expense".split())
    ac_currency = get_input("Enter account currency: ")
    creation_date = get_date()
    new_account_id = create_account(ac_name, ac_code, ac_currency, ac_type, init_bal)
    return new_account_id




def interactive_cli(old_records, accounts):
    x = True
    new_records = []
    while (x):
       r = record_transaction(old_records, accounts)
       new_records.append(r)
       x = input("Enter new transaction ? ")
       if x not in ['no', 'naye', 'n']:
           continue
       else:
           break
    os.system('clear')
    print(f"Previous balance: {accounts_bkup}")
    total_expense = 0
    for record in new_records:
        total_expense += record['total_price']

    
    for r in new_records:
        print(f"Item: {r['notes']} qty bought: {r['qty']}{r['units']}  price: {r['total_price']}")
    print(f"Total expense: {total_expense}")
    print(f"Account balance: {accounts}")
 


def record_transaction(old_records, accounts):
    record = {}
    record['id'] = str(uuid.uuid4())
    record['date'] = get_date()
    print("Destination Account")
    record['da_id'] = get_account("Destination Account") # cannot be equal to source
    print("Source Account")
    record['sa_id'] = get_account("Source Account")
    while record['da_id'] == record['sa_id']:
        print("Source and destination accounts cannot be the same")
        record['sa_id'] = get_account("Source Account")
        record['da_id'] = get_account("Destination Account") # cannot be equal to source
    # determine transaction type from here
    # record['transaction_type'] = '' transfer, expense, income
    record['notes'] = get_input("Enter name of item: ") # prompt depends on transaction type
    # record['meta_data'] = get_metadata() 
    record['units'] = get_input("Enter item units: ")
    record['qty'] = get_input("quantity: ", "float")
    u_or_t = get_input("Unit price or total price? U for unit, T for total: ").lower()
    record['item_price'] = get_input("Unit Price: " if u_or_t.lower() == 'u' else 'Total Price :', "float" )
    if u_or_t == 'u':
        record['total_price'] = float(record['item_price']) * float(record['qty'])
    else:
        record['total_price'] = float(record['item_price'])
    record['unit_price'] = record['total_price']/record['qty']

    # update records list and accounts
    accounts['accounts'][record['sa_id']]['ac_bal'] -= record['total_price']
    accounts['accounts'][record['da_id']]['ac_bal'] += record['total_price']

    old_records['records'][record['id']] = record
    update_records(old_records)
    update_accounts(accounts)
    return record
 
