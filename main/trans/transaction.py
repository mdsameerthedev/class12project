import customtkinter as ctk


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


transaction().run()
