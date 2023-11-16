import customtkinter as ctk


messagebox = ctk.CTk()
messagebox.geometry('400x120')

message = 'HellowWorld'

label = ctk.CTkLabel(master=messagebox,text=message,height=80,width=400,anchor='center',font=('Roboto',20))
label.pack()
button = ctk.CTkButton(master=messagebox,text='Ok')
button.pack()
messagebox.mainloop()

