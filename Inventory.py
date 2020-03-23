import mysql.connector
import configparser

cfg = configparser.ConfigParser()
cfg.read('inventoryconfig.cfg')
host = cfg['MySQL server connection properties']['host']
user = cfg['MySQL server connection properties']['user']
passwd = cfg['MySQL server connection properties']['password']

mydb = mysql.connector.connect(
    host = host,
    user = user,
    password = passwd,
    auth_plugin = 'mysql_native_password'
)

addItem = ("INSERT INTO items (itemName,price,quantity)"
            "VALUES (%s, %s, %s)")

cursor = mydb.cursor(buffered=True)

cursor.execute('create database inventory')
cursor.execute('USE inventory')
cursor.execute('create table items( id int auto_increment primary key, itemName varchar(50), price float, quantity int)')

def parser():
    cmd = input('Enter a command: ')
    validCmd = ['ls','help','input','sql','quit','init']
    if cmd not in validCmd:
        print('Enter a valid command (use "help" for a list of commands")')
        return parser()
    elif cmd == "help":
        print('Avalible commands are:')
        print('help: get help')
        print('ls: returns a list of items currently in the database')
        print('input: add an item to the database')
        print('sql: execute a MySql query against the database')
        print('quit: exit the program')
        return parser()
    elif cmd == 'quit':
        return
    elif cmd == 'ls':
        cursor.execute("SELECT * FROM items")
        result = cursor.fetchall()
        print(result) 
        return parser()
    elif cmd == 'input':
        nameInput = input("Input an item name: ")
        priceInput = input("Input a price (without $): ")
        quantityInput = input("Input a quantity: ")
        p = float(priceInput)
        q = int(quantityInput)
        n = nameInput
        cursor.execute(addItem,(n,p,q))
        return parser()
    elif cmd == 'sql':
        query = input('Enter a query: ')
        try:
            cursor.execute(query)
        except:
            print('SQL error')
            return parser()

print('Inventory Manager by: W. Conner Camp')
print('This program allows you to manage an inventory using MySQL as a database')
input("Press 'Enter' to Continue ")

parser()

