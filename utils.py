import os
import readline


def custom_input(prompt):
    readline.set_startup_hook(lambda: readline.insert_text(''))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

def is_numeric(n):
    try:
        x = float(n)
        return True
    except ValueError:
        try:
            x = int(n)
            return True
        except ValueError:
            return False
    
def clear():
    os.system('clear')

def get_date():
    a = datetime.now()
    return a.strftime('%m.%d.%y') + '-' + str(a.timestamp())


