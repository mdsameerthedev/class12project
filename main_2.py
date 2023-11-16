import tkinter as tk
import mysql.connector as sql
import tabulate as tb


'''class Account:
    def __int__(self, no, name, email, address, pin):
        self.no = no
        self.name = name
        self.email = email
        self.address = address
        self.pin = pin

    def print_user(self):
        data  = (self.no, self.name, self.email, self.address, self.pin)
        return data'''


class DataBase:
    def __init__(self, host, usname, psswd):
        self.host = host
        self.usname = usname
        self.psswd = psswd
        self.conn = sql.connect(host=self.host, username=self.usname, password=self.psswd)
        self.cursor = self.conn.cursor()
        self.cursor.execute('use Bank')

    def is_connected(self):
        if self.conn.is_connected():
            print('Connected Successfully!')
        else:
            print('Connection Unsuccessful!')

    def user_register(self, user_data):
        query = "insert into Account_Holders (`Account_Number`,`Holder's Name`,`Holder's Email`,`Holder's Address`,`Account's PIN`) values(%s,%s,%s,%s,%s)"
        check = 'select * from Account_Holders'
        self.cursor.execute(check)
        got = self.cursor.fetchall()
        if user_data not in got:
            self.cursor.execute(query, user_data)
            self.conn.commit()
            print('Registered Successfully!')
            return True
        else:
            raise Exception('Registration failed!')
            return False

    def get_user(self, username):
        query = "select `Account_Number`,`Account's PIN` from Account_Holders where `Account_Number` = %s"
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchall()
        print(user)
        self.conn.commit()
        print('Login SuccessFull!')
        return user[0][0], user[0][1]


db = DataBase(host='localhost', usname='root', psswd='root@123')
db.is_connected()

class UserAlgo:
    @staticmethod
    def open_account():
        print()
        print('Account Openning:')
        account_no = input('Account Number : ')
        holder_name = input('Account Holder Name : ')
        holder_email = input('Account Holder Email : ')
        holder_Address = input('Account Holders Address : ')
        try:
          acc_pin = int(input('PIN Number : '))
        except ValueError:
            print('Invalid PIN, Give it in Integer!')
            acc_pin = int(input('PIN Number : '))

        acc = (account_no, holder_name, holder_email, holder_Address, acc_pin)
        db.user_register(acc)

    @staticmethod
    def login():
        try:
            print()
            print('Login into your account: ')
            acc_no = input('Account Number : ')
            try:
                acc_pin = int(input('PIN Number : '))
            except ValueError:
                print('Invalid PIN, Give it in Integer!')
                acc_pin = int(input('PIN Number : '))

            acc = (acc_no,acc_pin)
            res = acc[0]
            db.get_user(res)
            return True
        except:
            return False






print()
print('Auth:')
print('1.Login')
print('2.Open Account')
print('3.quit')
choice = input('Choose Your Option')
if choice == '1':
    if UserAlgo.login():
if choice == '2':
    UserAlgo.open_account()

