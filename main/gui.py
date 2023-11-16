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

    def get_details(self, username):
        query = "select * from Account_Holders where `Account_Number` = %s"
        self.cursor.execute(query, (username,))
        data = self.cursor.fetchall()
        return data

    def win_name(self):
        return self.holdername


db = DataBase(host='localhost', usname='root', psswd='root@123')
db.is_connected()


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


class transaction:
    def __init__(self):
        self.transactionWindow = ctk.CTk()
        self.transactionWindow.geometry('600x500')
        self.transactionWindow.title('New Transaction')

        self.transFrame = ctk.CTkFrame(master=self.transactionWindow)
        self.transFrame.pack(pady=15, padx=15, fill='both', expand=True)

        self.transLabel = ctk.CTkLabel(master=self.transFrame, text='New Transaction', font=('Roboto', 30), width=500,
                                       height=35, anchor='nw')
        self.transLabel.pack(pady=10, padx=10)

        self.transchildFrame = ctk.CTkFrame(master=self.transFrame)
        self.transchildFrame.pack(pady=15, padx=15, fill='both', expand=True)

        self.transname = ctk.CTkEntry(master=self.transchildFrame, placeholder_text='Transaction Name ', height=50,
                                      width=450)
        self.transname.pack(pady=20)

        self.rname = ctk.CTkEntry(master=self.transchildFrame, placeholder_text="Receiver's Account Number ", height=50,
                                  width=450)
        self.rname.pack(pady=20)

        self.amount = ctk.CTkEntry(master=self.transchildFrame, placeholder_text='Amount ', height=50, width=450)
        self.amount.pack(pady=20)

        self.sendButton = ctk.CTkButton(master=self.transchildFrame, text='Transfer', height=50, width=200,
                                        font=('Helvetica', 15))
        self.sendButton.pack(pady=20, padx=20)

    def run(self):
        self.transactionWindow.mainloop()


class withdraw:
    def __init__(self):
        self.wdWindow = ctk.CTk()
        self.wdWindow.geometry('600x400')
        self.wdWindow.title('WithDraw Amount')

        self.wdFrame = ctk.CTkFrame(master=self.wdWindow)
        self.wdFrame.pack(pady=15, padx=15, fill='both', expand=True)

        self.wdLabel = ctk.CTkLabel(master=self.wdFrame, text='Withdraw', font=('Roboto', 30), width=500,
                                    height=35, anchor='nw')
        self.wdLabel.pack(pady=10, padx=10)

        self.wdchildFrame = ctk.CTkFrame(master=self.wdFrame)
        self.wdchildFrame.pack(pady=15, padx=15, fill='both', expand=True)

        self.wdamount = ctk.CTkEntry(master=self.wdchildFrame, placeholder_text='Amount', height=50,
                                     width=450)
        self.wdamount.pack(pady=20)

        self.wdreason = ctk.CTkEntry(master=self.wdchildFrame, placeholder_text="Reason", height=50,
                                     width=450)
        self.wdreason.pack(pady=20)

        self.wdButton = ctk.CTkButton(master=self.wdchildFrame, text='Widthdraw', height=50, width=200,
                                      font=('Helvetica', 15))
        self.wdButton.pack(pady=20, padx=20)

    def run(self):
        self.wdWindow.mainloop()


class deposit:
    def __init__(self):
        self.dWindow = ctk.CTk()
        self.dWindow.geometry('600x400')
        self.dWindow.title('Deposit Amount')

        self.dFrame = ctk.CTkFrame(master=self.dWindow)
        self.dFrame.pack(pady=15, padx=15, fill='both', expand=True)

        self.dLabel = ctk.CTkLabel(master=self.dFrame, text='Deposit', font=('Roboto', 30), width=500,
                                   height=35, anchor='nw')
        self.dLabel.pack(pady=10, padx=10)

        self.dchildFrame = ctk.CTkFrame(master=self.dFrame)
        self.dchildFrame.pack(pady=15, padx=15, fill='both', expand=True)

        self.damount = ctk.CTkEntry(master=self.dchildFrame, placeholder_text='Amount', height=50,
                                    width=450)
        self.damount.pack(pady=20)

        self.dreason = ctk.CTkEntry(master=self.dchildFrame, placeholder_text="Source", height=50,
                                    width=450)
        self.dreason.pack(pady=20)

        self.dButton = ctk.CTkButton(master=self.dchildFrame, text='Deposit', height=50, width=200,
                                     font=('Helvetica', 15))
        self.dButton.pack(pady=20, padx=20)

    def run(self):
        self.dWindow.mainloop()


class mainwindow:
    def __init__(self, win_name, details):
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

        self._accountFrame = ctk.CTkFrame(master=self.frame1, height=745, width=500)
        self._accountFrame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.deposit2 = ctk.CTkFrame(master=self.frame1, height=745, width=1045)
        self.deposit2.grid(row=1, column=1, pady=5, sticky='nsew', )
        size = 20
        self._label = ctk.CTkLabel(master=self._accountFrame, text='Account', font=('Roboto', 30), height=30, width=500,
                                   anchor='w')
        self._label.pack(padx=20, pady=20)
        self.Name = ctk.CTkLabel(master=self._accountFrame, text=f'Name: {details[0][2]}', anchor='w', height=30,
                                 font=('Roboto', size),
                                 width=400)
        self.Name.pack(pady=10)
        self.acc_No = ctk.CTkLabel(master=self._accountFrame, text=f'Account Number : {details[0][1]} ', anchor='w',
                                   font=('Roboto', size),
                                   height=30, width=400)
        self.acc_No.pack(pady=10)
        self.eMail = ctk.CTkLabel(master=self._accountFrame, text=f'E-Mail: {details[0][3]}', anchor='w',
                                  font=('Roboto', size),
                                  height=30, width=400)
        self.eMail.pack(pady=10)

        self.address = ctk.CTkLabel(master=self._accountFrame, text=f'Address: {details[0][4]}', anchor='w',
                                    font=('Roboto', size),
                                    height=30, width=400)
        self.address.pack(pady=10)

        self.type = ctk.CTkLabel(master=self._accountFrame, text=f'Account Type : {details[0][5]}', anchor='w',
                                 font=('Roboto', size),
                                 height=30, width=400)
        self.type.pack(pady=10)

        self.logout = ctk.CTkButton(master=self._accountFrame, text='Logout', text_color=('red', 'red'),
                                    font=('roboto', 20), height=50, width=100)
        self.logout.pack(pady=15)
        # --------_______________----------_________-------___________------__________------______----

        self.transaction = ctk.CTkButton(master=self.deposit2, text='Transfer', height=40, width=200)
        self.transaction.pack()

        self.wd = ctk.CTkButton(master=self.deposit2, text='Withdraw', height=40, width=200)
        self.wd.pack()

        self.transaction = ctk.CTkButton(master=self.deposit2, text='Transfer', height=40, width=200)
        self.transaction.pack()

    def run(self):
        self.main.mainloop()


class UserAlgo:
    @staticmethod
    def open_account(acc_no, holder_name, holder_email, holder_address, acc_pin):
        acc = (acc_no, holder_name, holder_email, holder_address, acc_pin)
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


class RegisterUser:
    def __init__(self, user):
        self.accno = user[0]
        self.name = user[1]
        self.email = user[2]
        self.address = user[3]
        self.pin = user[4]

    def print_user(self):
        user = (self.accno, self.name, self.email, self.address, self.pin)
        return user


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
        self._quit = ctk.CTkButton(master=self._frame, text='Quit', height=40, width=200, command=self.quit)
        self._quit.pack(pady=10, padx=20)

    def login(self):
        self._chooseWindow.destroy()
        LoginPage().run()

    def register(self):
        self._chooseWindow.destroy()
        RegisterPage().run()

    def quit(self):
        self._chooseWindow.destroy()

    def run(self):
        self._chooseWindow.mainloop()


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

        self.accnoEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Account Number ', height=45,
                                       width=400,
                                       font=('Helvetica', 20))
        self.accnoEntry.pack(pady=20, padx=20)

        self._nameEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Full Name ', height=45,
                                       width=400, font=('Helvetica', 20))
        self._nameEntry.pack(pady=20, padx=20)

        self._emailEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Email ID', height=45,
                                        width=400, font=('Helvetica', 20))
        self._emailEntry.pack(pady=20, padx=20)

        self._addEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Address', height=45,
                                      width=400, font=('Helvetica', 20))
        self._addEntry.pack(pady=20, padx=20)

        self._passEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='PIN', show='*',
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
        name = self.accnoEntry.get()
        username = self._nameEntry.get()
        email = self._emailEntry.get()
        address = self._addEntry.get()
        pin = self._passEntry.get()
        data = [name, username, email, address, pin]
        self.user = RegisterUser(data)
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
        accno = self._loginUsernameEntry.get()
        pin = self._loginPasswordEntry.get()
        data = [accno, pin]
        self.user_list.append(data)
        print(self.user_list)
        print(data)
        self.user = LoginUser(username=accno, passwrd=pin).print_user()

        result = UserAlgo.login(self.user[0], self.user[1])

        if result:
            self._loginWindow.destroy()
            name = db.win_name()
            edata = db.get_details(accno)
            print(edata)
            mainwindow(name, edata).run()
        else:
            message('Login Error!', 'Incorrect Number or PIN!')

    def back(self):
        self._loginWindow.destroy()
        choose().run()

    def run(self):
        self._loginWindow.mainloop()


choose().run()
