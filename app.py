from __future__ import print_function, unicode_literals

import os
import psycopg2
from pathlib import Path

from PyInquirer import style_from_dict, Token, prompt, print_json, Separator
from pprint import pprint
from examples import custom_style_2

authorized = False
isOwner = False

DATABASE_USERNAME = ''
DATABASE_PASS = ''





# connect to database
def connectBase():
    return psycopg2.connect(user = "postgres",
                                  password = "896011pop",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "MyBookStore")

first_time = [
    {
        'type': 'list',
        'name': 'first',
        'message': 'What would you like to do?',
        'choices': [
            'Log in',
            'Sign Up',
            'Exit'
        ]
    },
]
login = [
    {
        'type': 'input',
        'message': 'Enter your username',
        'name': 'username'
    },  
    {
        'type': 'password',
        'message': 'Enter your password',
        'name': 'password'
    }
]











def add_new_customer():
    first = True
    match = False 
    name = None
    email = None
    bank = None
    password = None
    while not match and not all(map(lambda x: x is not None, [name, email, bank, password])):
        if not first:
            print('Your passwords do not match ') 
        sign = [
            {
                'type': 'input',
                'message': 'Enter your username',
                'name': 'username'
            },  
            {
                'type': 'input',
                'message': 'Enter your email',
                'name': 'email'
            },
            {
                'type': 'input',
                'message': 'Enter your bank account number',
                'name': 'bank'
            },    
            {
                'type': 'input',
                'message': 'Enter your password',
                'name': 'password'
            },
            {
                'type': 'input',
                'message': 'Confirm your password',
                'name': 'password-c'
            },
        ]
        a = prompt(sign, style=custom_style_2)
        name = a['username']
        email = a['email']
        bank = a['bank']
        password = a['password']
        password_confirm =  a['password-c']
        match = True  if password == password_confirm  else False
    sql = """INSERT INTO customer(name, email, password, bank_account)
             VALUES(%s, %s, %s, %s);"""
    values = (name, email, password, bank);
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = connectBase()
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, values)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        authorized = True

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close() 


# Insert owner of the store
def insert_owner():
    print('creating owner')
    sql = """INSERT INTO customer(name, email, password, bank_account)
             VALUES(%s, %s, %s, %s);"""
    values = ("owner", "owner@owner.com", "owner1", "12312361236163131");
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = connectBase()
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, values)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close() 



def execute_commands(commands):
    print(""" create tables in the PostgreSQL database""")
    commands = tuple(commands)
    conn = None
    try:
        conn = connectBase()
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            if command:
                cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



# gets commands from the sql file
def getCommands(fileName):
    fd = open('SQL/'+fileName, 'r')
    sqlFile = fd.read()
    fd.close()

    return sqlFile.split(';')

def checkout():
    print('checkout')
def add_to_cart(book):
    select = [
        {
        'type': 'input',
        'name': 'quant',
        'message': 'What\'s the quantity?',
        }
    ]
    a = prompt(select, style=custom_style_2)
    quant = a['quant']
    print()
def select(options):
    next_options = [
        {
        'type': 'list',
        'name': 'book',
        'message': 'What would you like to do?',
        'choices': [
            'Menu',
            'Exit'
        ]
        },
    ]
    select_options = [
    {
        'type': 'list',
        'name': 'book',
        'message': 'Which book would you like to select?',
        'choices': options.keys()
    },
    ]
    a = prompt(select_options, style=custom_style_2)
    book_ID = int(options[a['book']])
    # Print book info
    try:
        conn = connectBase()
        cur = conn.cursor()
        cur.execute("SELECT title, author.name, publisher.name, ISBN, price, genre, page_num, inventory_quantity  FROM book, author, publisher WHERE book.ID = %s and author.ID = book.authorID and book.publisherID = publisher.ID", (book_ID))
        rows = cur.fetchall()
        print("Book information ")
        book = rows[0]
        print('Title: ', book[0])
        print('Author: ', book[1])
        print('Publisher: ', book[2])
        print('ISBN: ', book[3])
        print('Price: ', str(book[4]))
        print('Genre: ', book[5])
        print('Pages: ', str(book[6]))
        print('Quantity: ', str(book[7]))
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        a = prompt(next_options, style=custom_style_2)
        c = a['action']
        if c == 'Menu':
            menu()
        elif c == 'Exit':
            running = False



def browse():
    browse_options = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'What would you like to do?',
        'choices': [
            'Select Book(s)',
            'Menu',
            'Exit'
        ]
    },
    ]
    print('Here are all the books in the store')
    # print all books
    conn = None
    options = {}
    try:
        conn = connectBase()
        cur = conn.cursor()
        cur.execute("SELECT book.ID, title, name FROM book, author where book.authorID = author.ID")
        rows = cur.fetchall()
        print("The number of books in the store: ", cur.rowcount)
        print()
        print()
        for i, row in enumerate(rows):
            print('{}. {} by {} '.format(i, row[1], row[2]))
            # set options hash table
            options[row[1]] = str(row[0])
        print()
        print()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        a = prompt(browse_options, style=custom_style_2)
        c = a['action']
        if c == 'Select Book(s)':
            select(options)
        elif c == 'Menu':
            menu()
        elif c == 'Exit':
            running = False


def menu(isOwner):
    store = [
{
        'type': 'list',
        'name': 'action',
        'message': 'What would you like to do?',
        'choices': [
            'Browse Books',
            'Search Books',
            'Checkout',
            'Track Order',
            'Exit'
        ]
    },
]

    admin = [
    {
            'type': 'list',
            'name': 'action',
            'message': 'What would you like to do?',
            'choices': [
                'Display Reports',
                'Add Book',
                'Remove Book',
                'Exit'
            ]
        },
    ]
    if isOwner:
        print('Welcome to the Adming page')
        a = prompt(admin, style=custom_style_2)
        c = a['action']
        running = False
    else:
        print('Welcome to the Store')
        a = prompt(store, style=custom_style_2)
        c = a['action']
        if c == 'Browse Books':
            browse()
        elif c == 'Search Books':
            search()
        elif c == 'Exit':
            running = False
        


# check if user is authorized and proceed to main app
# function for authenticating the user
def authenticate(username, password, isOwner):
    conn = None
    try:
        conn = connectBase()
        cur = conn.cursor()
        cur.execute("SELECT name FROM customer WHERE name = %s and password=%s", (username, password))
        print("The number of customers: ", cur.rowcount)
        n = cur.rowcount
        if n > 0:
            rows = cur.fetchall()
            if rows[0][0] == 'owner':
                isOwner = True
            else:
                isOwner = False
            authorized = True
        else:
            authorized = False
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if authorized:
            menu(isOwner)

try:
    connection = connectBase()

    cur = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(),"\n")

    # check if schemas were created if not use the DDL
    table_str = 'book'
    query = "select to_regclass(%s)"
    cur.execute(query, ['{}.{}'.format('schema', 'table')])
    exists = bool(cur.fetchone()[0])
    if not exists:
    # if True:
        print('table does not exist')
        commands = getCommands('DDL.sql')
        execute_commands(commands)
        insert_owner()
        
    else:
        print('Table exists')
    commands = getCommands('populate_books.sql')
    execute_commands(commands)
# check if user is authorized
    running = True
    while running:
        if not authorized:
            print('Welcome to LookInnaBook!')
            answers = prompt(first_time, style=custom_style_2)
            if answers['first'] == 'Log in':
                a = prompt(login, style=custom_style_2)
                username = a['username']
                passwd = a['password']
                authenticate(username, passwd, isOwner)
            elif answers['first'] == 'Sign Up':
                print('Create new account for LookInnaBook')
                add_new_customer()
            else:
                break
        else:
            if not running:
                break
            menu(isOwner)



    

except (Exception, psycopg2.Error) as error :
    print("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cur.close()
            connection.close()
            print("PostgreSQL connection is closed")