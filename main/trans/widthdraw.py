import customtkinter as ctk


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


withdraw().run()
