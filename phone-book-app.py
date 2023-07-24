"""
Problem Statement

Earlier, we use to have a phone book, which consists of contact numbers. Now that we
know the power of python, let's create a digital phonebook.
"""


import psycopg2
from tabulate import tabulate


connection = psycopg2.connect(user='postgres',
                              password='yourpass',
                              host='localhost',
                              database='PhoneBook')

Cursor = connection.cursor()

def create_user_table():
    sql_command='''
                    CREATE TABLE user_info (id int, fname text, lname text, dob date, email varchar, ph_no bigint, password varchar);
    '''
    try:
        Cursor.execute(sql_command)
        connection.commit()
    except Exception:
        print("\nYou are already registerd once.\n")
        Login()

def create_client_table():
    sql_comman='''
                    CREATE TABLE contacts (contact_id int, first_name text, last_name text, ph_no bigint, email varchar);
    '''
    try:
        Cursor.execute(sql_comman)
        connection.commit()
    except Exception as e:
        print(e,'\n')

def store_register_data(id,fname,lname,dob,email,ph_no,pw):
    sql_command='''
                    INSERT INTO user_info(id, fname, lname, dob, email, ph_no, password)
                    VALUES(%s,%s,%s,%s,%s,%s,%s);
    '''
    data=(id,fname,lname,dob,email,ph_no,pw)
    try:
        Cursor.execute(sql_command,data)
        connection.commit()
        print('REGISTRATION SUCESSFUL\n')
        create_client_table()
        Login()
    except Exception as e:
        print(e,'\n')

def Registration():
    fname = input('Enter your first name:\t')
    lname = input('Enter your last name:\t')
    dob = input('Enter your date of birth (yyyy-mm-dd):\t')
    email = input('Enter your email:\t')
    ph_no = int(input('Enter your phone number:\t'))

    n = str(ph_no)
    n = [*n]
    lst = []
    for i in range(-4, 0):  
        lst.append((n[i]))
    id = int(''.join(lst))


    pw = input('Enter your password:\t')
    rpw = input('Re-type your password:\t')
    if pw != rpw:
        print('Password does not match')
        Registration()
    else:
        create_user_table()
        store_register_data(id,fname,lname,dob,email,ph_no,pw)




def Login():
    print('\t\t\tLOGIN')
    ph=int(input('Enter the phone no.\t'))
    pw=input('Enter the password:\t')
    sql_command='''
                    SELECT ph_no, password
                    FROM user_info;
    '''
    Cursor.execute(sql_command)
    result=Cursor.fetchall()
    if ph==result[0][0]:
        if pw==result[0][1]:
            print('\nLogin successful\n')
        else:
            print('\nWrong password\n')
            Login()
    else:
        print('\ninvalid number!\n')
        Login()





def view_a():
    sql_command='''SELECT * FROM contacts;'''
    try:
        Cursor.execute(sql_command)
        result=Cursor.fetchall()

        print('YOUR CONTACTS ARE:')
        header=('Contact Id', 'First Name', 'Last Name', 'Ph NO.', 'Email')
        print(tabulate(result, headers=header, tablefmt='fancy_grid'))
    except Exception as e:
        print(e,'\n')
    functions()




def search_by_id():
    id=(int(input('Enter the id:\t')),)
    sql_command='''
                    SELECT * FROM contacts
                    WHERE contact_id = %s;
    '''
    try:
        Cursor.execute(sql_command, id)
        result=Cursor.fetchall()
        print('Here is your data:')
        header=('Contact Id', 'First Name', 'Last Name', 'Ph NO.', 'Email')
        print(tabulate(result, headers=header, tablefmt='fancy_grid'))
    except Exception as e:
        print(e,'\n')
    

def search_by_PhNumber():
    ph=(int(input('Enter the Phone number:\t')),)
    sql_command='''
                    SELECT * FROM contacts
                    WHERE ph_no = %s;
    '''
    try:
        Cursor.execute(sql_command, ph)
        result=Cursor.fetchall()
        print('Here is your data:')
        header=('Contact Id', 'First Name', 'Last Name', 'Ph NO.', 'Email')
        print(tabulate(result, headers=header, tablefmt='fancy_grid'))
    except Exception as e:
        print(e,'\n')


def search_by_mail():
    mail=(input('Enter the Email:\t'),)
    sql_command='''
                    SELECT * FROM contacts
                    WHERE email = %s;
    '''
    try:
        Cursor.execute(sql_command, mail)
        result=Cursor.fetchall()
        print('Here is your data:')
        header=('Contact Id', 'First Name', 'Last Name', 'Ph NO.', 'Email')
        print(tabulate(result, headers=header, tablefmt='fancy_grid'))
    except Exception as e:
        print(e)

def view():
    print('\n\n[id]         Search by Contact Id')
    print('[ph]         Search by Phone number')
    print('[mail]       Search by Email')

    choose=input('Enter your choose:\t').lower()

    match choose:
        case 'id':
            search_by_id()
        case 'ph':
            search_by_PhNumber()
        case 'mail':
            search_by_mail()
        case _:
            print('\nEnter valid choice:\n')
            view()

    functions()






def add():
    fname=input('Enter the first name:\t')
    lname=input('Enter the last name:\t')
    ph=int(input('Enter the phone numbe:\t'))
    mail=input('Enter the email:\t')

    n = str(ph)
    n = [*n]
    lst = []
    for i in range(-4, 0):  
        lst.append((n[i]))

    id = int(''.join(lst))

    sql_command='''
                    INSERT INTO contacts (contact_id, first_name, last_name, ph_no, email)
                    VALUES (%s,%s,%s,%s,%s);
    '''
    data=(id,fname,lname,ph,mail)
    try:
        Cursor.execute(sql_command,data)
        connection.commit()

        print('\nRecord inserted successfully\n')
    except Exception as e:
        print(e,'\n')

    functions()






def update():
    print('UPDATE RECORD:')
    print('\n[id]       Update id')
    print('[fname]      Update First name')
    print('[lname]      Update Last name')
    print('[ph]         Update Phone Number')
    print('[mail]       Update Email')
    choose2=input('\nEnter your choice\t').lower()


    match choose2:
        case 'id':
            choose2='contact_id'
        case 'fname':
            choose2='first_name'
        case 'lname':
            choose2='last_name'
        case 'ph':
            choose2='ph_no'
        case 'mail':
            choose2 ='email'
        case _:
            print('\nEnter valid choice\t')
            update()
    
    data=input('Enter the new data:\t')


    print('SELECT RECORD:')
    print('\n[id]       Select data using id')
    print('[fname]      Select data using First name')
    print('[lname]      Select data using Last name')
    print('[ph]         Select data using Phone Number')
    print('[mail]       Select data using Email')
    choose=input('\nEnter your choice\t').lower()
    match choose:
        case 'id':
            choose='contact_id'
        case 'fname':
            choose='first_name'
        case 'lname':
            choose='last_name'
        case 'ph':
            choose='ph_no'
        case 'mail':
            choose ='email'
        case _:
            print('\nEnter valid choice\t')
            update()
    record_data=input(f'\nEnter the {choose}\t')


    sql_command='''
                    UPDATE contacts
                    SET {} = '{}'
                    wHERE {} = {}
    '''.format(choose2, data, choose, record_data )

    try:
        Cursor.execute(sql_command)
        connection.commit()
        print('\nRecord updated\n')
    except Exception as e:
        print(e,'\n')

    functions()




def dele():
    print('SELECT RECORD:')
    print('\n[id]       Select data using id')
    print('[fname]      Select data using First name')
    print('[lname]      Select data using Last name')
    print('[ph]         Select data using Phone Number')
    print('[mail]       Select data using Email')
    choose=input('\nEnter your choice\t').lower()
    match choose:
        case 'id':
            choose='contact_id'
        case 'fname':
            choose='first_name'
        case 'lname':
            choose='last_name'
        case 'ph':
            choose='ph_no'
        case 'mail':
            choose ='email'
        case _:
            print('\nEnter valid choice\t')
            dele()
        
    data=input(f'\nEnter the {choose}\t')

    try:
        sql_command='''
                        SELECT * FROM contacts
                        WHERE {} = {};
        '''.format(choose, data)

        Cursor.execute(sql_command)
        result=Cursor.fetchall()
        header=('Contact Id', 'First Name', 'Last Name', 'Ph NO.', 'Email')
        print(tabulate(result, headers=header, tablefmt='fancy_grid'))


        sql_command='''
                        DELETE FROM contacts
                        WHERE {} = {};
        '''.format(choose,data)

        Cursor.execute(sql_command)
        connection.commit()

        print('\nRecord deleted\n')
    except Exception as e:
        print(e,'\n')

    functions()






def functions():
    print('[view-a]     to view all save contacts')
    print('[view]       to view a specific contact')
    print('[add]        to a new contact')
    print('[del]        to delete a contact')
    print('[update]     to update an existing contact')
    print('[exit]       to exit the program\n')

    choose=input('Enter your choose:\t').lower()
    match choose:
        case 'view-a':
            view_a()
        case 'view':
            view()
        case 'add':
            add()
        case 'del':
            dele()
        case 'update':
            update()
        case 'exit':
            print('\nProgram exit\n')
            quit()
        case _:
            print('\nEnter a valid choice:\n')
            functions()

def main():
    print("Choose an option.")
    print('1. Enter R for registration.')
    print('2. Enter L for login.')
    welcome = input().upper()

    if welcome == 'R':
        Registration()
    elif welcome == 'L':
        Login()
    else:
        print('Enter a valid choice')
        main()
    functions()


main()

Cursor.close()