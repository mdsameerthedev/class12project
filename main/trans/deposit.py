import customtkinter as ctk


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


deposit().run()
