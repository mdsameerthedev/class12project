import customtkinter as ctk
from screeninfo import get_monitors


class user:
    def __init__(self, name, email, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.email = email

    def print_user(self):
        user = (self.name, self.username, self.email, self.password)
        return user


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

        self._accountFrame = ctk.CTkFrame(master=self.frame1, height=745, width=500)
        self._accountFrame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.deposit2 = ctk.CTkFrame(master=self.frame1, height=745, width=1045)
        self.deposit2.grid(row=1, column=1, pady=5, sticky='nsew')

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

        self.transaction = ctk.CTkButton(master=self.deposit2, text='Transfer', height=40, width=200)
        self.transaction.pack()

    def run(self):
        self.main.mainloop()


mainwindow('sameer').run()
