import customtkinter as ctk
import customtkinter
import mysql.connector as mysql
import socket
import threading
import os
from PIL import Image
import twilio


# ---------- GET IP ------#
class IP:
    def __init__(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.connect(('8.8.8.8', 80))
        self.ipAddress = soc.getsockname()[0]
        soc.close()

    def __repr__(self):
        return self.ipAddress


# ------------------------------------------#

# ------- USER MANAGEMENT -------#

# LOGIN USER FORMAT
class LoginUser:
    def __init__(self, username, passwrd):
        self.username = username
        self.password = passwrd

    def print_user(self):
        user = [self.username, self.password]
        return user


# REGISTER USER FORMAT
class RegisterUser:
    def __init__(self, name, email, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.email = email

    def print_user(self):
        user = (self.name, self.username, self.email, self.password)
        return user


# ---DATABASE CONNECTION---#
class DataBase:
    def __init__(self, host, usname, psswd):
        self.host = host
        self.usname = usname
        self.psswd = psswd
        self.conn = mysql.connect(host=self.host, username=self.usname, password=self.psswd)
        self.cursor = self.conn.cursor()
        self.cursor.execute('use chat')

    def is_connected(self):
        if self.conn.is_connected():
            print('Connected Successfully!')
        else:
            print('Connection Unsuccessful!')

    def user_register(self, us1):
        query = 'insert into users (name,username,email,password) values(%s,%s,%s,%s)'
        check = 'select * from users'
        res = self.cursor.execute(check)
        print(res)
        got = self.cursor.fetchall()
        print(got)
        if us1 not in got:
            self.cursor.execute(query, us1)
            self.conn.commit()
            print('Registered Successfully!')
            return True
        else:
            raise 'Registration failed!'
            return False

    def get_user(self, username):
        query = 'select * from users where username = %s'
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchall()
        print(user)
        self.conn.commit()
        return user[0][2], user[0][4]


db = DataBase(host='localhost', usname='root', psswd='root@123')
db.is_connected()

# --------GRAPHICAL USER INTERFACE-------#
ctk.set_appearance_mode('dark')


# ACCOUNT DISPLAY FRAME
class AccountDisplay:
    def __init__(self, master, us):
        self._accountFrame = ctk.CTkFrame(master=master, corner_radius=10)
        self._accountFrame.pack(pady=10, padx=10, fill='both', expand=True)
        self._label = ctk.CTkLabel(master=self._accountFrame, text='Account', font=('Roboto', 30), height=30, width=500,
                                   anchor='w')
        self._label.pack(padx=20, pady=20)
        self.Name = ctk.CTkLabel(master=self._accountFrame, text=f'Name: {us.print_user()[0]}', anchor='w', height=30,
                                 width=400)
        self.Name1 = ctk.CTkLabel(master=self._accountFrame, text=f'UserName: {us.print_user()[1]}', anchor='w',
                                  height=30, width=400)
        self.Name2 = ctk.CTkLabel(master=self._accountFrame, text=f'E-Mail: {us.print_user()[2]}', anchor='w',
                                  height=30, width=400)
        self.Name2.pack()


class choose:
    def __init__(self):
        self._chooseWindow = ctk.CTk()
        self._chooseWindow.title('Login OR Register')
        self._chooseWindow.geometry('400x200')
        self._frame = ctk.CTkFrame(master=self._chooseWindow)
        self._frame.pack(pady=20, padx=20, fill='both', expand=True)
        self._login = ctk.CTkButton(master=self._frame, text='Login', height=40, width=200, command=self.login)
        self._login.pack(pady=20, padx=20)
        self._register = ctk.CTkButton(master=self._frame, text='Register', height=40, width=200,
                                       command=self.register)
        self._register.pack(pady=10, padx=20)

    def login(self):
        self._chooseWindow.destroy()
        LoginPage().run()

    def register(self):
        self._chooseWindow.destroy()
        RegisterPage().run()

    def run(self):
        self._chooseWindow.mainloop()


# LOGIN WINDOW
class LoginPage:
    def __init__(self):
        self.user = None
        self._loginWindow = ctk.CTk()
        self._loginWindow.geometry('500x400')
        self._loginWindow.title('Login')
        self._loginFrame = ctk.CTkFrame(master=self._loginWindow)
        self._loginFrame.pack(pady=20, padx=20, fill='both', expand=True)

        self._loginLabel = ctk.CTkLabel(master=self._loginFrame, text='Login', font=('Roboto', 40))
        self._loginLabel.pack(pady=20, padx=20)

        self._loginUsernameEntry = ctk.CTkEntry(master=self._loginFrame, placeholder_text='Username / Email ID',
                                                height=40, width=200)
        self._loginUsernameEntry.pack(pady=20, padx=20)

        self._loginPasswordEntry = ctk.CTkEntry(master=self._loginFrame, placeholder_text='Password', show='*',
                                                height=40, width=200)
        self._loginPasswordEntry.pack(pady=8, padx=20)

        self._loginButton = ctk.CTkButton(master=self._loginFrame, text='Login', height=50, width=110,
                                          command=self.get_values)
        self._loginButton.pack(pady=20, padx=20)

        self._back = ctk.CTkButton(master=self._loginFrame, text='Return to Previous Window!',
                                   command=self.back)
        self._back.pack()

        self.user_list = []

    def get_values(self):
        username = self._loginUsernameEntry.get()
        password = self._loginPasswordEntry.get()
        data = [username, password]
        self.user_list.append(data)
        print(self.user_list)
        print(data)
        self.user = LoginUser(username=username, passwrd=password).print_user()
        return self.user

    def back(self):
        self._loginWindow.destroy()
        choose().run()

    def run(self):
        self._loginWindow.mainloop()
        choose().run()


# REGISTER WINDOW
class RegisterPage:
    def __init__(self):

        self.messagebox = None
        self.user = None
        self.db = db
        self._registerWindow = ctk.CTk()
        self._registerWindow.title('Register')
        self._registerWindow.geometry('600x750')
        self._registerFrame = ctk.CTkFrame(master=self._registerWindow)
        self._registerFrame.pack(pady=20, padx=20, fill='both', expand=True)

        self._registerLabel = ctk.CTkLabel(master=self._registerFrame, text='Register', font=('Roboto', 40))
        self._registerLabel.pack(pady=20, padx=20)

        self.nameEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Name', height=45, width=400,
                                      font=('Helvetica', 20))
        self.nameEntry.pack(pady=20, padx=20)

        self._usernameEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Username', height=45,
                                           width=400, font=('Helvetica', 20))
        self._usernameEntry.pack(pady=20, padx=20)

        self._emailEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Email ID', height=45,
                                        width=400, font=('Helvetica', 20))
        self._emailEntry.pack(pady=20, padx=20)

        self._passEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Password', show='*',
                                       height=45, width=400, font=('Helvetica', 20))
        self._passEntry.pack(pady=20, padx=20)

        self._RegisterButton = ctk.CTkButton(master=self._registerFrame, text='Register', height=50, width=200,
                                             command=self.check_login, font=('Helvetica', 20))
        self._RegisterButton.pack(pady=20, padx=20)

        self.user_list = []

        self._back = ctk.CTkButton(master=self._registerFrame, text='Return to Previous Window!',
                                   command=self.back)
        self._back.pack()

        

    def get_values(self, db):
        name = self.nameEntry.get()
        username = self._usernameEntry.get()
        email = self._emailEntry.get()
        password = self._passEntry.get()
        data = [name, username, email, password]
        self.user = RegisterUser(name=data[0], username=data[1], email=data[2],
                                 password=data[3])
        try:
            print(self.user.print_user())

            data2 = self.user.print_user()
            # INSERT INTO table_name (column1, column2) VALUES (%s, %s, %s, %s)
            db.user_register(data2)
            db.conn.commit()
            return True, 'Register Success!'
        except:
            return False, 'Register Failed!'

    def check_login(self):
        self.messagebox = ctk.CTk()
        self.messagebox.geometry('400x120')

        if self.get_values(db)[0]:
            message = self.get_values(db)[1]

            label = ctk.CTkLabel(master=self.messagebox, text=message, height=80, width=400, anchor='center',
                                 font=('Roboto', 20))
            label.pack()
            button = ctk.CTkButton(master=self.messagebox, text='Ok',command=self.close_mess)
            button.pack()
            self.messagebox.mainloop()
        else:
            message = self.get_values(db)[1]
            label = ctk.CTkLabel(master=self.messagebox, text=message, height=80, width=400, anchor='center',
                                 font=('Roboto', 20))
            label.pack()
            button = ctk.CTkButton(master=self.messagebox, text='Ok',command=self.close_mess)
            button.pack()
            self.messagebox.mainloop()





    def back(self):
        self._registerWindow.destroy()
        choose().run()

    def run(self):
        self._registerWindow.mainloop()

    def close_mess(self):
        self.messagebox.destroy()



choose().run()
