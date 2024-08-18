import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk



PORT = 40000
HOST = '127.0.0.1'
ADDRESS = (HOST, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)
 
# GUI class for the chat
class GUICHAT:
    
    def __init__(self):
        
        
        self.Window = Tk()
        self.Window.withdraw()
 
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Enter name")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # Enter NAme label
        self.pls = Label(self.login,
                         text="Enter name",
                         justify=CENTER)
 
        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # name label
        self.labelName = Label(self.login,
                               text="Name: ")
 
        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)
 
        # create a entry box for
        # type the message
        self.entryName = Entry(self.login)
 
        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)
 
        # set the focus of the cursor
        self.entryName.focus()
 
        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         command=lambda: self.goAhead(self.entryName.get()))
 
        self.go.place(relx=0.4,
                      rely=0.55)
        self.Window.mainloop()
 
    def goAhead(self, name):
        
        self.layout(name)
 
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()
 
    # CHAT BOX
    def layout(self, name):

        

        
 
        self.name = name
        
        self.Window.deiconify()
        self.Window.title("CHAT")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="black")
        self.labelHead = Label(self.Window,
                               bg="black",
                               fg="white",
                               text=self.name,
                               font ="bold",
                               pady=5)
 
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="white")
 
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
 
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="black",
                             fg="white",
                             padx=5,
                             pady=5)
 
        self.textCons.place(relheight=0.745,
                            relwidth=0.63,
                            rely=0.08)
 
        self.labelBottom = Label(self.Window,
                                 bg="white",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="light gray",
                              fg="blue")
 
        # into gui
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
 
        self.entryMsg.focus()
 
        # Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                bg="blue",
                                command=lambda: self.sendButton(self.entryMsg.get()))
 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")

        
                              
 
        # scroll bar
        scrollbar = Scrollbar(self.textCons)
 
        
        # into the gui 
        scrollbar.place(relheight=1,
                        relx=0.974)
 
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)
        
        # peers list
        
        
        
        loginframe = Frame(self.Window,
                             width=400,
                             height=400,
                          bg = "white")
        loginframe.place(x=300, y=50)
        peerlist = Label(loginframe,
                         text = "Peers",
                         font = 12,
                         fg = "black",
                    bg = "white")


        peerlist.place (x = 5, y= 5)

        loginlist = Listbox (loginframe)
        loginlist.place ( x = 10 , y = 30)
        loginlist.insert(END, name)
        
        
        
       

        
 
    # sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
 
    # receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
 
                # if the messages from the server is NAME send the client's name
                if message == 'name':
                    client.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")
 
                    self.textCons.config(state=DISABLED)
        
            except:
                # an error will be printed on the command line or console if there's an error
                print("ERROR")
                client.close()
                break
 
    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break
 
 
# create a GUI class object
g = GUICHAT()
