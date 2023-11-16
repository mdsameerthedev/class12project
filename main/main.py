import customtkinter as ctk
import mysql.connector as sql
from screeninfo import get_monitors


class DataBase:
    def __init__(self, host, usname, psswd):
        self.holdername = None
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
        query = "select `Account_Number`,`Account's PIN`,`Holder's Name` from Account_Holders where `Account_Number` = %s"
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchall()
        self.holdername = user[0][2]
        print(user)
        self.conn.commit()
        print('Login SuccessFull!')
        return user[0][0], user[0][1]

    def win_name(self):
        return self.holdername


db = DataBase(host='localhost', usname='root', psswd='root@123')
db.is_connected()


class RegisterPage:
    def __init__(self):
        self.user = None
        self.db = db
        self._registerWindow = ctk.CTk()
        self._registerWindow.title('Register')
        self._registerWindow.geometry('600x750')
        self._registerFrame = ctk.CTkFrame(master=self._registerWindow)
        self._registerFrame.pack(pady=20, padx=20, fill='both', expand=True)

        self._registerLabel = ctk.CTkLabel(master=self._registerFrame, text='Register', font=('Roboto', 40))
        self._registerLabel.pack(pady=20, padx=20)

        self.nameEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Account Number ', height=45, width=400,
                                      font=('Helvetica', 20))
        self.nameEntry.pack(pady=20, padx=20)

        self._usernameEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Full Name ', height=45,
                                           width=400, font=('Helvetica', 20))
        self._usernameEntry.pack(pady=20, padx=20)

        self._emailEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Email ID', height=45,
                                        width=400, font=('Helvetica', 20))
        self._emailEntry.pack(pady=20, padx=20)

        self._passEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='PIN', show='*',
                                       height=45, width=400, font=('Helvetica', 20))
        self._passEntry.pack(pady=20, padx=20)
        self._type = ctk.CTkComboBox(master=self._registerFrame,values=('Savings Account','Current Account'))
        self._type.pack()

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
        print(self.user.print_user())

        data2 = self.user.print_user()
        # INSERT INTO table_name (column1, column2) VALUES (%s, %s, %s, %s)
        db.user_register(data2)
        db.conn.commit()
        return True

    def check_login(self):
        if self.get_values(db):
            print('Success!')
        else:
            print('Register Failed!')

    def back(self):
        self._registerWindow.destroy()
        choose().run()

    def run(self):
        self._registerWindow.mainloop()


class display:
    def __init__(self):
        global res
        for m in get_monitors():
            res = str(m)
            print(res)

        width = res[24:28]
        height = res[37:41]
        self.val = width + 'x' + height

    def get_info(self):
        return self.val


info = display().get_info()
ctk.set_appearance_mode('system')


class message:
    def __init__(self, title, warning):
        self.message = ctk.CTkToplevel()
        self.message.title = title
        self.message.geometry('500x200')
        self.lable = ctk.CTkLabel(master=self.message, text=warning, font=('roboto', 20), height=150, width=500,
                                  anchor='center')
        self.lable.pack()
        self.button = ctk.CTkButton(master=self.message, text='Ok', height=80, width=50, command=self.close)
        self.button.pack()

    def run(self):
        self.message.mainloop()

    def close(self):
        self.message.destroy()


class mainwindow:
    def __init__(self, win_name):
        self.main = ctk.CTk()
        self.main.geometry(info)
        self.main.title(f"{win_name}'s Account Dashboard")
        self._mainFrame = ctk.CTkFrame(master=self.main)
        self._mainFrame.pack(pady=20, padx=20, fill='both', expand=True)

        self.main_lab = ctk.CTkLabel(master=self._mainFrame, text='Home', font=('Roboto', 50), height=10, width=2000,
                                     anchor='w')
        self.main_lab.pack(padx=20, pady=20)

        self.frame1 = ctk.CTkFrame(master=self._mainFrame)
        self.frame1.pack(pady=20, padx=20, fill='both', expand=True)

        self._accountFrame = ctk.CTkFrame(master=self.frame1,height=745,width=500)
        self._accountFrame.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')

        self.deposit2 = ctk.CTkFrame(master=self.frame1,height=745,width=1082)
        self.deposit2.grid(row=1,column=1,pady=5)

        self._label = ctk.CTkLabel(master=self._accountFrame, text='Account', font=('Roboto', 30), height=30, width=500,
                                   anchor='w')
        self._label.pack(padx=20, pady=20)
        self.Name = ctk.CTkLabel(master=self._accountFrame, text=f'Name: ', anchor='w', height=30,
                                 width=400)
        self.Name.pack()
        self.Name1 = ctk.CTkLabel(master=self._accountFrame, text=f'Account Number :  ', anchor='w',
                                  height=30, width=400)
        self.Name1.pack()
        self.Name2 = ctk.CTkLabel(master=self._accountFrame, text=f'E-Mail: ', anchor='w',
                                  height=30, width=400)
        self.Name2.pack()

    def run(self):
        self.main.mainloop()


class UserAlgo:
    @staticmethod
    def open_account():
        print()
        print('Account Opening:')
        account_no = input('Account Number : ')
        holder_name = input('Account Holder Name : ')
        holder_email = input('Account Holder Email : ')
        holder_address = input('Account Holders Address : ')
        try:
            acc_pin = int(input('PIN Number : '))
        except ValueError:
            print('Invalid PIN, Give it in Integer!')
            acc_pin = int(input('PIN Number : '))

        acc = (account_no, holder_name, holder_email, holder_address, acc_pin)
        db.user_register(acc)

    @staticmethod
    def login(acc_no, acc_pin):
        try:
            acc = (acc_no, acc_pin)
            result = acc[0]
            bin = db.get_user(result)
            if bin[0] == acc_no and bin[1] == acc_pin:
                print('Success!')
                return True
        except:
            return False


class LoginUser:
    def __init__(self, username, passwrd):
        self.username = username
        self.password = passwrd

    def print_user(self):
        user = [self.username, self.password]
        return user


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

        self._loginUsernameEntry = ctk.CTkEntry(master=self._loginFrame, placeholder_text='Account Number',
                                                height=40, width=200)
        self._loginUsernameEntry.pack(pady=20, padx=20)

        self._loginPasswordEntry = ctk.CTkEntry(master=self._loginFrame, placeholder_text='PIN', show='*',
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

        result = UserAlgo.login(self.user[0], self.user[1])
        if result:
            self._loginWindow.destroy()
            name  = db.win_name()
            mainwindow(name).run()
        else:
            message('Login Error!', 'Incorrect Number or PIN!')

    def back(self):
        self._loginWindow.destroy()
        choose().run()

    def run(self):
        self._loginWindow.mainloop()


class choose:
    def __init__(self):
        self._chooseWindow = ctk.CTk()
        self._chooseWindow.title('Login OR Register')
        self._chooseWindow.geometry('400x250')
        self._frame = ctk.CTkFrame(master=self._chooseWindow)
        self._frame.pack(pady=30, padx=20, fill='both', expand=True)
        self._login = ctk.CTkButton(master=self._frame, text='Login', height=40, width=200, command=self.login)
        self._login.pack(pady=10, padx=20)
        self._register = ctk.CTkButton(master=self._frame, text='Open Account', height=40, width=200,
                                       command=self.register)
        self._register.pack(pady=10, padx=20)
        self._quit = ctk.CTkButton(master=self._frame, text='Quit', height=40, width=200)
        self._quit.pack(pady=10, padx=20)

    def login(self):
        self._chooseWindow.destroy()
        LoginPage().run()

    def register(self):
        self._chooseWindow.destroy()
        RegisterPage().run()

    def run(self):
        self._chooseWindow.mainloop()


choose().run()
