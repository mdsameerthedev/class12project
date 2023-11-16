import customtkinter as ctk
import customtkinter
import mysql.connector as mysql
import socket
import threading


#	GET IP	#

class IP:
    def init(self):

        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.connect(('8.8.8.8', 80))


        self.ipAddress = soc.getsockname()[0]
        soc.close()


    def repr(self):
        return self.ipAddress


#	#

# --------- CHAT SERVER & CLIENT	#
class Server:
    def init(self, HOST, PORT, MAX_SIZE):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((HOST, PORT))


        print("Server listening on {}:{}".format(HOST, PORT))

# Dictionary to store client addresses
        clients = {}
        username = server_socket.recvfrom(MAX_SIZE)
        clients.update(username)

        while True:
            data, addr = server_socket.recvfrom(MAX_SIZE)
            if addr not in clients:
                print("New connection from {}".format(addr))
                clients[addr] = None

            message = data.decode('utf-8')
            print(f"Received message from {addr}: {message}")

# Broadcast the message to all connected clients
            for client_addr in clients:
                if client_addr != addr:
                    server_socket.sendto(data, client_addr)


class Client:
    def init(self, host, port):
        self.receive_thread = None
        self.HOST = host


        self.PORT = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def receive_messages(self):
        while True:
            try:
                data, server_addr = self.client_socket.recvfrom(1024)
                print(data.decode('utf-8'))
            except:
                pass


    def start(self):
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()


        username = input('Username: ')
        self.client_socket.sendto(username.encode('utf-8'), (self.HOST, self.PORT))

        while True:
            message = input()
            if message == 'exit':
                    break
            self.client_socket.sendto(message.encode('utf-8'), (self.HOST, self.PORT))
            self.client_socket.close()


#	#


# ------- USER & CHATROOM MANAGEMENT	#

# LOGIN USER FORMAT
class LoginUser:
    def init(self, username, passwrd):
        self.username = username
        self.password = passwrd


    def print_user(self):
        user = [self.username, self.password]
        return user


# REGISTER USER FORMAT
class RegisterUser:
    def init(self, name, email, username, password):
         self.name = name
         self.username = username
         self.password = password
         self.email = email


    def print_user(self):
         user = [self.name, self.username, self.email, self.password]
         return user


# CHATROOM FORMAT
class ChatRoom:
    def init(self, roomname, port, password, limit):
        self.roomname = roomname
        self.port = port
        self.password = password
        self.limit = limit


    def send_to_db(self):
            return self.roomname, self.port, self.password, self.limit


# ROOM INFORMATION FORMAT
class RoomInfo:
    def init(self, master):

        self._info = ctk.CTkFrame(master=master, height=50, width=500, bg_color=('white', 'black'))
        self.info.pack(padx=5, pady=0)


#	#


# ---DATABASE CONNECTION--- #
class DataBase:
    def init(self, host, usname, psswd):
        self.host = host
        self.usname = usname
        self.psswd = psswd
        self.conn = mysql.connect(host=self.host, username=self.usname, password=self.psswd)
        self.cursor = self.conn.cursor()
        self.cursor.execute('use chatApplicationDatabase')


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

#	#

# --------GRAPHICAL USER INTERFACE	#
ctk.set_appearance_mode('dark')


# CHATROOM CREATE WINDOW
class CreateRoom:
    def init(self):
        self.room = None
        self._createWindow = customtkinter.CTk
        self._createWindow.geometry('600x500')
        self._createWindow.title('Create ChatRoom')
        self._createFrame = customtkinter.CTkFrame(
                            master=self._createWindow)  # Use CTk.Frame() instead of cCTk.CCTkFrame
        self._createFrame.pack(pady=12, padx=20, fill='both', expand=True)
        self.createLabel = customtkinter.CTkLabel(master=self._createFrame, text='Create Chatroom', font=('Roboto',

                                                                                                  30),width = 400, anchor = 'w')
        self.createLabel.pack(pady=20)

self.roomnameEntry = customtkinter.CTkEntry(master=self._createFrame, placeholder_text='Room Name', height=35,

                                            cCTk.CCTkEntry
self.roomnameEntry.pack(pady=12, padx=20)

width = 400,
font = ('Helvetica', 20))  # Use CTk.Entry() instead of


self.portEntry = customtkinter.CTkEntry(master=self._createFrame, placeholder_text='Port (1000-9999)',
                                        height=35,
                                        width=400, font=('Helvetica', 20))
self.portEntry.pack(pady=12, padx=20)

self.clientEntry = customtkinter.CTkEntry(master=self._createFrame, placeholder_text='Number of Clients',
                                          height=35, width=400,
                                          font=('Helvetica', 20))
self.clientEntry.pack(pady=12, padx=20)

self._passEntry = customtkinter.CTkEntry(master=self._createFrame, placeholder_text='Password', height=35,
                                         show='*', width=400, font=('Helvetica', 20))
self._passEntry.pack(pady=12, padx=20)

self._createButton = customtkinter.CTkButton(master=self._createFrame, text='Create', height=50, width=250,
                                             font=('Roboto', 20), command=self.get_values)
self._createButton.pack(pady=12, padx=20)


def get_values(self):
    roomname = self.roomnameEntry.get()
    port = self.portEntry.get()
    password = self._passEntry.get()
    limit = self.clientEntry.get()
    self.room = ChatRoom(
        roomname=roomname, port=port, password=password, limit=limit
    ).send_to_db()
    print(self.room)


self._createWindow.destroy()


def run(self): self._createWindow.mainloop()


# ACCOUNT DISPLAY FRAME
class AccountDisplay:
    def init(self, master, us):

        self._accountFrame = customtkinter.CTkFrame(master=master, corner_radius=10)
    self._accountFrame.pack(pady=10, padx=10, fill='both', expand=True)


self._label = customtkinter.CTkLabel(master=self._accountFrame, text='Account', font=('Roboto', 30), height=30,
                                     width=500, anchor='w')
self._label.pack(padx=20, pady=20)

self.Name = customtkinter.CTkLabel(master=self._accountFrame, text=f'Name: {us.print_user()[0]}', anchor='w',
                                   height=30, width=400)
self.Name.pack()

self.Name1 = customtkinter.CTkLabel(master=self._accountFrame, text=f'UserName: {us.print_user()[1]}',
                                    anchor='w', height=30, width=400)
self.Name1.pack()

self.Name2 = customtkinter.CTkLabel(master=self._accountFrame, text=f'E-Mail:  {us.print_user()[2]}',
                                    anchor='w', height=30, width=400)
self.Name2.pack()


# CHATROOM NAME DISPLAY TILE
class CTkChatRoomTile:
    def init(self, master, username, time):

        _frame = customtkinter.CTkFrame(master=master, height=60)


_frame.pack(pady=10, padx=20)

label = customtkinter.CTkLabel(master=_frame, text=username, font=('Roboto', 30), anchor='nw', height=40, width=500)

label.pack(padx=10, pady=5)

status_lab = customtkinter.CTkLabel(master=_frame, text=time, anchor='nw', height=30, width=500)
status_lab.pack(padx=12, pady=6)


# MAIN WINDOW
class App(customtkinter.CTk): def


init(self):
super().init()

self.title("SOCIAL SQUAD")
self.geometry("700x450")
self.resizable(False, False)

# set grid layout 1x2 self.grid_rowconfigure(0, weight=1) self.grid_columnconfigure(1, weight=1)

# load images with light and dark mode image
image_path = os.path.join(os.path.dirname(os.path.realpath(file)), "../test_images")
self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path,
                                                                 "CustomTkinter_logo_single.png")),
                                         size=(26, 26))
self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                               size=(500, 150))
self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                               size=(20, 20))
self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                         dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                         size=(20, 20))
self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                         dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                         size=(20, 20))
self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                             dark_image=Image.open(os.path.join(image_path, "add_user_light.png")),
                                             size=(20, 20))
self.add_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "add_chatroom.png")),
                                        size=(20, 20))

# create navigation frame
self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
self.navigation_frame.grid(row=0, column=0, sticky="nsew")
self.navigation_frame.grid_rowconfigure(4, weight=1)

self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" SOCIAL SQUAD",
                                                     image=self.logo_image, compound="left",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,

                                           command=self.home_button_event)

text = "Home",
fg_color = "transparent", text_color = ("gray10", "gray90"), hover_color = ("gray70", "gray30"),
image = self.home_image, anchor = "w",

self.home_button.grid(row=1, column=0, sticky="ew")

self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                              border_spacing=10, text="Your ChatRooms", fg_color="transparent",
                                              text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                              image=self.chat_image, anchor="w", command=self.frame_2_button_event)
self.frame_2_button.grid(row=2, column=0, sticky="ew")

self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                              border_spacing=10, text="Account", fg_color="transparent",
                                              text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                              image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
self.frame_3_button.grid(row=3, column=0, sticky="ew")

self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                        values=["Light", "Dark", "System"],

                                                        command=self.change_appearance_mode_event)
self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

# create home frame
self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
self.home_frame.grid_columnconfigure(0, weight=1)

self.chatroom_label = customtkinter.CTkLabel(master=self.home_frame, text='Home', width=600, anchor='w',
                                             font=('Roboto', 40))
self.chatroom_label.grid(row=0, column=0, padx=8)

self.chatroomframe = customtkinter.CTkScrollableFrame(master=self.home_frame, height=375, width=600)
self.chatroomframe.grid(row=1, column=0, pady=5, padx=9)

# create second frame
self.second_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")

self._create_room = customtkinter.CTkButton(master=self.second_frame, image=self.add_image,
                                            text='Create ChatRoom', width=450, height=50, command=self.show_create)
self._create_room.pack(pady=20, padx=10)

self.users = [['Mohamed Sameer', 'ACTIVE'], ['Narendhra Prasadh', 'ACTIVE'], ['Vishal', 'ACTIVE'],
              ['Nadeem', 'INACTIVE'], ['Abdul', 'INACTIVE']]
for username, status in self.users:
    CTkChatRoomTile(master=self.second_frame, username=username, time=status)

# create third frame
self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
us = User(
    name="Mohamed Sameer", username='sameer', password='my_secret', email='thismyemail@domaim.com'
)
AccountDisplay(master=self.third_frame, us=us)

# select default frame
self.select_frame_by_name("home")


def select_frame_by_name(self, name):


# set button color for selected button
self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

# show selected frame
if name == "home":
    self.home_frame.grid(row=0, column=1, sticky="nsew") else:
    self.home_frame.grid_forget()
    if name == "frame_2":
        self.second_frame.grid(row=0, column=1, sticky="nsew") else:
        self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew") else:
            self.third_frame.grid_forget()


            def home_button_event(self):
                self.select_frame_by_name("home")


            def frame_2_button_event(self):
                self.select_frame_by_name("frame_2")


            def frame_3_button_event(self):
                self.select_frame_by_name("frame_3")


            @staticmethod
            def change_appearance_mode_event(new_appearance_mode):
                customtkinter.set_appearance_mode(new_appearance_mode)


            @staticmethod
            def show_create():
                CreateRoom().run()


            # AUTHENTICATION CHOOSE WINDOW
            class choose:
                def init(self): self._chooseWindow = ctk.CTk


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
                def init(self): self.user = None


            self._loginWindow = ctk.CTk
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

            self._back = ctk.CTkButton(master=self._loginFrame, text='Return to Previous Window!', command=self.back)
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
                def


            init(self):
            self.user = None
            self._registerWindow = ctk.CTk  # Use CTk.CTk() instead of cCTk.CCTk() self._registerWindow.title('Register') self._registerWindow.geometry('600x750')

            self._registerFrame = ctk.CTkFrame(master=self._registerWindow)  # Use CTk.Frame() instead of cCTk.CCTkFrame
            self._registerFrame.pack(pady=20, padx=20, fill='both', expand=True)

            self._registerLabel = ctk.CTkLabel(master=self._registerFrame, text='Register',
                                               font=('Roboto', 40))  # Use CTk.Label() instead of cCTk.CCTkLabel
            self._registerLabel.pack(pady=20, padx=20)

            self.nameEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Name', height=45,
                                          width=400, font=('Helvetica', 20))  # Use CTk.Entry() instead of
            cCTk.CCTkEntry
            self.nameEntry.pack(pady=20, padx=20)

            self._usernameEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Username', height=45,
                                               width=400, font=('Helvetica', 20))
            self._usernameEntry.pack(pady=20, padx=20)

            self._emailEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Email ID', height=45,
                                            width=400,
                                            font=('Helvetica', 20))
            self._emailEntry.pack(pady=20, padx=20)

            self._passEntry = ctk.CTkEntry(master=self._registerFrame, placeholder_text='Password', show='*', height=45,
                                           width=400, font=('Helvetica', 20))
            self._passEntry.pack(pady=20, padx=20)

            self._RegisterButton = ctk.CTkButton(master=self._registerFrame, text='Register', height=50, width=200,
                                                 command=self.get_values,

                                                 font=('Roboto', 20))  # Use CTk.Button() instead of cCTk.CCTkButton
            self._RegisterButton.pack(pady=20, padx=20)

            self.user_list = []
            self._back = ctk.CTkButton(master=self._registerFrame, text='Return to Previous Window!', command=self.back)
            self._back.pack()


            def get_values(self):
                name = self.nameEntry.get()


            username = self._usernameEntry.get()
            email = self._emailEntry.get()
            password = self._passEntry.get()

            data = [name, username, email, password]
            self.user_list.append(data)
            self.user = User(name=self.user_list[0][0], username=self.user_list[0][1], email=self.user_list[0][2],
                             password=self.user_list[0][3],

                             )
            print(self.user_list)
            print(self.user.print_user())
            return self.user, self.user_list


            def back(self):
                self._registerWindow.destroy()


            choose().run()


            def run(self):
                self._registerWindow.mainloop()


            # CHAT BUBBLE
            class CTkChatBubble:
                def init(self, master, username, message, time):

                    self._Buble = ctk.CTkFrame(master=master, height=65, width=380, border_color=('black', 'white'),
                                               border_width=2)


            self._Buble.pack(pady=3)
            self._Buble.pack_propagate(0)

            self._username = ctk.CTkLabel(master=self._Buble, text=username, text_color=('black', 'white'), height=15,
                                          width=350, anchor='nw', font=('monospace', 10, 'bold'))
            self._username.pack(pady=5)

            self._message = ctk.CTkLabel(master=self._Buble, text=message, height=15, width=350, anchor='nw')
            self._message.pack()
            self._time = ctk.CTkLabel(master=self._Buble, text=time, height=4, width=355, anchor='ne',
                                      text_color=('grey30', 'grey50'))
            self._time.pack()


            # CHAT WINDOW
            class ChatUI:
                def init(self, chatroomname): self._chatWindow = ctk.CTk

                self._chatWindow.geometry('600x509')
                self._chatWindow.title(chatroomname)


            self.infoFrame = ctk.CTkFrame(master=self._chatWindow, height=60, width=590)
            self.infoFrame.pack(padx=5, pady=0)
            self.infoFrame.pack_propagate(0)

            self.roomlabel = ctk.CTkLabel(master=self.infoFrame, text=chatroomname, height=60, width=550, anchor='w',
                                          font=('Helvetica', 25)).pack(padx=10)

            self.menu = ctk.CTkButton(master=self.infoFrame, text=':', height=50, width=20)
            self.menu.pack(side='right')

            self.chatFrame = ctk.CTkScrollableFrame(master=self._chatWindow, height=370, width=570)
            self.chatFrame.pack(pady=5)
            # Ensure the row expands

            self.textbox_frame = ctk.CTkFrame(master=self._chatWindow, height=53, width=590)
            self.textbox_frame.pack(pady=1)
            self.textbox_frame.pack_propagate(0)

            self.text = ctk.CTkEntry(master=self.textbox_frame, placeholder_text='Message', height=52, width=590)
            self.text.pack()
            self.text.bind("<Return>", print('clicked'))

            self.send = ctk.CTkButton(master=self.textbox_frame)
            self.send.pack()


            def get_message(self):
                message = self.text.get()


            return message


            @staticmethod
            def add_chat_bubble():
                chat_bubble = buble


            # Optionally, you can customize chat_bubble further if needed.
            return chat_bubble


            def add_info(self):
                info = RoomInfo(master=self.infoFrame)
                return info


            def run(self):
                self._chatWindow.mainloop()


            if name == ' main ':
                db = DataBase(host='localhost', usname='root', psswd='root@123')
                db.is_connected()
            choose().run()