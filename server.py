from socket import *
from threading import Thread
import threading
import _thread
import tkinter
from tkinter import ttk
from tkinter import messagebox
from time import ctime 
import os
import ftplib
import sys
import time

class roomsRecord():
    def __init__(self):
        self.data = {}

    def getRawRooms(self):
        # print('use getRawRooms************************* ',self.data)
        return self.data

    def getAllRooms(self):
        strr = ''
        for i in self.data :
            strr = strr + str(i) + ';'
        return strr

    def addRoom(self, message):
        self.data[message]  = []
        
    def deleteRoom(self,message):
        for i in self.data:
            if(str(i) == message):
                self.data.pop(message)
                return self.getAllRooms()


server = None
serverTurn = 0
HOST_ADDR = gethostname()
HOST_PORT = 5000
CONNECTIONS_LIST = []
rooms = roomsRecord()
name = 'unknow'
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
server.bind((HOST_ADDR, HOST_PORT))
server.listen(5)
threadLock = threading.Lock()


def database(name,count,win):
    lose = int(count) - int(win)
    rate = (float(win)/float(count)) * 100
    try:
        if name != 'unknow':
            out = open("Allname.txt","a",encoding="utf-8") 
                
    except IOError:
        print("Error : can't find file or read data")
    else:
        if name != 'unknow':
            with out as c:
                c.write(name +" "+count+" "+win+" "+str(lose)+" "+str(rate))
                c.write("\n")
                c.close()

# def upload():
#     input = open("login.txt")
#     for line in input:
#         in1, in2, in3, in4 = line.split()
#     input.close()
#     ftp = ftplib.FTP(in1)
#     ftp.login(user=in2, passwd=in3)
#     ftp.cwd('Assigngroup1')
#     filename = 'Allname.txt'
#     ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
#     ftp.retrlines('LIST')
#     ftp.quit()
        
def updatedata():
    try: 
        f = open('Allname.txt')
    except IOError:
        print("Error : can't find file or read data")
    finally:
        datalist = []
        for i in f:
            name, count, win,lose,rate = i.split()
            datalist.append([name, int(count), int(win),int(lose),float(rate)])
        f.close()

        new = []
        for i in range(len(datalist)):
            n = datalist[i][0]
            c = datalist[i][1]
            w  = datalist[i][2]
            l = datalist[i][3]
            r = datalist[i][4]
            for j in range(i+1,len(datalist)):
                if datalist[j][0] == n:
                    c += datalist[j][1]
                    w += datalist[j][2]
                    l = c - w
                    r = (float(w)/float(c))*100
                    datalist[j][0] = '--'
                  
            if n != '--':
                new.append([n,c,w,l,r]) 
             
    try: 
        f = open('Allname.txt','w')
    except IOError:
        print("Error : can't find file or read data")
    finally:
        for i in range(len(new)):
            f.write(str(new[i][0])+" "+str(new[i][1]) +" " +str(new[i][2])+" " +str(new[i][3])+" " +str(new[i][4]))
            f.write("\n")
        f.close()
           
class clientHandler(Thread):
    def __init__(self, client, address,rooms,name):
        Thread.__init__(self)
        self._client = client
        self._address = address
        self._name = name
        self._rooms = rooms
        self._currentRoom = 'null'
        self._opponent = ''
    
    def broadCastingMessage(self, activeClient, message):
        for socket in CONNECTIONS_LIST:
            if socket != server and socket != activeClient:
                try:
                    broadcastMessage = str.encode(message)
                    socket.send(broadcastMessage)  
                except:
                    print ("Client (%s) is offline" %self._address)
                    broadCastingMessage(socket, ("Client (%s) is offline" %self._address))
                    server.close()
                    CONNECTIONS_LIST.remove(socket)
                    print(CONNECTIONS_LIST)
    
    def run(self):
        allRooms  = self._rooms.getAllRooms()
        msg = 'showAllRooms_' + allRooms
        threadLock.acquire()
        self._client.send(str.encode(msg))
        threadLock.release()    
        while True:
            try:
                msg= self._client.recv(2048).decode('utf-8')
                print('msg = ',msg)
                msg,obj = msg.split('_')
            except :          
                if self._currentRoom !='null':
                    roomss = self._rooms.getRawRooms()
                    for i in roomss:
                        if(str(i) == self._currentRoom):
                            for j in roomss[i]:
                                if(j!=self._client):
                                    threadLock.acquire()
                                    self._client.send("another player offline" .encode())
                                    threadLock.release()
                                    self._client.close()
                                    CONNECTIONS_LIST.remove(self._client)
                            break
                
            else:
                if not msg:
                    print(str(self._address) + " disconnected")
                    self._client.close()
                    CONNECTIONS_LIST.remove(self._client)
                    break
                if msg == "exit":
                    self._client.close()
                    CONNECTIONS_LIST.remove(self._client)
                    print(CONNECTIONS_LIST)
                    break
                elif msg == "It\'s a Tie":
                    roomss = self._rooms.getRawRooms()
                    for i in roomss:
                        if(str(i) == self._currentRoom):
                            for j in roomss[i]:
                                if j != self._client:
                                    j.send("It\'s a Tie_123" .encode())

                    database(self._name,'1','0')
                    updatedata()
                    self._rooms.deleteRoom(self._currentRoom)
                    self._currentRoom = 'null'
                elif  msg == "X-Winner" :
                    if(obj == 'X'):
                        database(self._name,'1','1')
                    else:
                        database(self._name,'1','0')
                    updatedata()
                    self._rooms.deleteRoom(self._currentRoom)
                    self._currentRoom = 'null'
                elif  msg == "O-Winner":
                    if(obj == 'O'):
                        database(self._name,'1','1')
                    else:
                        database(self._name,'1','0')
                    updatedata()
                    self._rooms.deleteRoom(self._currentRoom)
                    self._currentRoom = 'null'
                elif msg == "setName":
                    self.name = obj
                    print('setName success name = ',self._name)
                elif msg == "createRoom":
                    tt = 0
                    roomss   = self._rooms.getRawRooms()
                    for i in roomss :
                        if(i == obj):   
                            print('Room is have already') 
                            msg = 'statuscreateRoom_'
                            self._client.send(str.encode(msg + "can't create Room"))   
                            tt=1
                    if tt == 0 : 
                        print("This room does not exist yet") 
                        msg = 'statuscreateRoom_'
                        self._client.send(str.encode(msg + "can create Room"))     
                        self._rooms.addRoom(obj)
                        time.sleep(1)
                        allRooms = self._rooms.getAllRooms()
                        msg = 'showAllRooms_' + allRooms
                        self._client.send(str.encode(msg))     
                elif msg == "joinRoom":
                    yy = 0
                    roomss   = self._rooms.getRawRooms()
                    for i in roomss :
                        if(i == obj):   
                            yy=1                
                            roomss[i].append(self._client)
                            self._currentRoom = obj 
                            if(len(roomss[i]) <= 2):
                                msg = 'statusRoom_'
                                self._client.send(str.encode(msg+'can join'))
                                print('can join')
                            if(len(roomss[i]) == 2):
                                k=['0','1']
                                p = 0
                                msg = 'startGame_'
                                threadLock.acquire()
                                for j in roomss[i]:
                                    j.send(str.encode(msg+k[p]))
                                    p=p+1
                                    print('send : ',j)
                                threadLock.release()
                            if(len(roomss[i]) > 2):
                                msg = 'statusRoom_'
                                self._client.send(str.encode(msg+"can't join"))
                                print("can't join")
                                roomss[i].remove(self._client)
                    # ---------- หาห้องไม่เจอ -------------------------------------------------
                    if yy == 0: 
                        msg = 'statusRoom_'
                        self._client.send(str.encode(msg+"This room does not have"))
                        print("can't find room")
                elif msg == "leaveRoom":
                    roomss = self._rooms.getRawRooms()
                    for i in roomss:
                        if(str(i) == self._currentRoom):
                            for j in roomss[i]:
                                if j != self._client:
                                    j.send("another player offline_123" .encode())
                                if j == self._client:
                                    database(self._name,'1','0')
                                    updatedata()
                            roomss[i].remove(self._client)
                           
                    self._client.close()
                    CONNECTIONS_LIST.remove(self._client)
                    print(CONNECTIONS_LIST)
                    break
                elif msg == "game":
                    print('useGame ')
                    roomss = self._rooms.getRawRooms()
                    for i in roomss :
                        if(str(i) == self._currentRoom):
                            for j in roomss[i]:
                                if j!= self._client :
                                    threadLock.acquire()
                                    j.send(str.encode(obj+'_cmd'))
                                    threadLock.release()
                elif msg =="deleteRoom":
                    allRooms = self._rooms.deleteRoom(obj)
                    msg = 'showAllRooms_' + allRooms
                    self.broadCastingMessage(self._client,msg)
                elif msg =="showAllRooms":
                    allRooms  = self._rooms.getAllRooms()
                    msg = 'showAllRooms_' + allRooms

                    threadLock.acquire()
                    self._client.send(str.encode(msg))
                    threadLock.release()                     
                else :
                    threadLock.acquire()
                    self.broadCastingMessage(self._client,msg)
                    threadLock.release()

connectserver=[]
def wait_accept():  
    global CONNECTIONS_LIST,connectserver
    while True: 
            print('Waiting for connection...')
            client, address = server.accept()            
            print('...connected from:', address)
            try:
                msg= client.recv(2048).decode('utf-8')
            except :
                print('error in wait')
                break
            else:
                if msg == 'play with host':
                    print('connectserver: ',connectserver)
                    if len(connectserver) == 0:
                        print('host mode')
                        threadLock.acquire()
                        connectserver.append(client)
                        threadLock.release()
                        client.send(str.encode("can join"))
                        _thread.start_new_thread(guiXO, () )
                    else:
                        print('host mode Full!!')
                        client.send(str.encode("can't join"))
                if msg == 'multiplayer':
                    print('multi mode')
                    threadLock.acquire()
                    CONNECTIONS_LIST.append(client)
                    threadLock.release()
                    handler = clientHandler(client,address,rooms,name)
                    handler.start() 
  
class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def guiXO(): 
    global client 
    def socketCreation ():
        global serverTurn,connectserver,client
        name = ''
        client = connectserver[0]
        client.send(str.encode("startGame_"+'1'))     
        while True:
            try:
                msg= client.recv(2048).decode('utf-8')
                print('recive msg = ',msg)
                msg ,obj = msg.split('_')
                
            except :
                print('player disconnect')    
                break
            else:
                if msg == "leaveRoom":
                    connectserver.remove(client)
                    break
                if msg == "setName":
                    name = obj
                    print('setName success name = ',name)
                if msg == "game":
                    if ( obj == 'a' and serverTurn == 0 ):
                        btn1['text']='X'
                        btn1['state']= tkinter.DISABLED
                        serverTurn = 1
                    elif ( obj == 'b' and serverTurn == 0 ):
                        btn2['text']='X'
                        btn2['state']= tkinter.DISABLED
                        serverTurn = 1
                    elif ( obj == 'c' and serverTurn == 0 ):
                        btn3['text']='X'
                        btn3['state']= tkinter.DISABLED
                        serverTurn = 1
                    elif ( obj == 'd' and serverTurn == 0 ):
                        btn4['text']='X'
                        btn4['state']= tkinter.DISABLED
                        serverTurn = 1
                    elif ( obj == 'e' and serverTurn == 0 ):
                        btn5['text']='X'
                        btn5['state']= tkinter.DISABLED
                        serverTurn = 1
                    elif ( obj == 'f' and serverTurn == 0 ):
                        btn6['text']='X'
                        btn6['state']= tkinter.DISABLED
                        serverTurn = 1
                    elif ( obj == 'g' and serverTurn == 0 ):
                        btn7['text']='X'
                        btn7['state']= tkinter.DISABLED
                        serverTurn = 1
                    elif ( obj == 'h' and serverTurn == 0 ):
                        btn8['text']='X'
                        btn8['state']= tkinter.DISABLED
                        serverTurn = 1
                    elif ( obj == 'i' and serverTurn == 0 ):
                        btn9['text']='X'
                        btn9['state']= tkinter.DISABLED
                        serverTurn = 1
                
                if (msg == 'O-Winner' or msg == 'X-Winner' or msg == 'It\'s a Tie'):
                    if msg == "It\'s a Tie":
                        database(name,'1','0')
                        database('server','1','0')
                        updatedata()   
                    elif  msg == "X-Winner" :
                        if(obj == 'X'):
                            database(name,'1','1')
                        else:
                            database('server','1','0')
                        updatedata()
                    elif  msg == "O-Winner":
                        if(obj == 'O'):
                            database('server','1','1')
                        else:
                            database(name,'1','0')
                        updatedata()
                  

                    lbl4 = tkinter.Label(window,text=msg)
                    lbl5['text'] = msg
                    lbl4['font']=35
                    lbl4['bg']='white'
                    lbl4.grid(column=2,row=1,padx=5,pady=5)
                    btn1['state']= tkinter.DISABLED
                    btn2['state']= tkinter.DISABLED
                    btn3['state']= tkinter.DISABLED
                    btn4['state']= tkinter.DISABLED
                    btn5['state']= tkinter.DISABLED
                    btn6['state']= tkinter.DISABLED
                    btn7['state']= tkinter.DISABLED
                    btn8['state']= tkinter.DISABLED
                    btn9['state']= tkinter.DISABLED
                    serverTurn = 0

        print('exit')            
    def sendbtn1 ():
        global serverTurn
        if serverTurn == 1:
            serverTurn = 0
            msg = 'a_cmd'
            client.send(msg.encode('utf-8'))
            btn1['text']='O'
            btn1['state']= tkinter.DISABLED
    def sendbtn2 ():
        global serverTurn
        if serverTurn == 1:
            serverTurn = 0
            msg = 'b_cmd'
            client.send(msg.encode('utf-8'))
            btn2['text']='O'
            btn2['state']= tkinter.DISABLED
    def sendbtn3 ():
        global serverTurn
        if serverTurn == 1:
            serverTurn = 0
            msg = 'c_cmd'
            client.send(msg.encode('utf-8'))
            btn3['text']='O'
            btn3['state']= tkinter.DISABLED
    def sendbtn4 ():  
        global serverTurn
        if serverTurn == 1:
            serverTurn = 0
            msg = 'd_cmd'
            client.send(msg.encode('utf-8'))
            btn4['text']='O'
            btn4['state']= tkinter.DISABLED
    def sendbtn5 ():
        global serverTurn
        if serverTurn == 1:
            serverTurn = 0
            msg = 'e_cmd'
            client.send(msg.encode('utf-8'))
            btn5['text']='O'
            btn5['state']= tkinter.DISABLED
    def sendbtn6 ():
        global serverTurn
        if serverTurn == 1:
            serverTurn = 0
            msg = 'f_cmd'
            client.send(msg.encode('utf-8'))
            btn6['text']='O'
            btn6['state']= tkinter.DISABLED
    def sendbtn7 ():
        global serverTurn
        if serverTurn == 1:
            serverTurn = 0
            msg = 'g_cmd'
            client.send(msg.encode('utf-8'))
            btn7['text']='O'
            btn7['state']= tkinter.DISABLED
    def sendbtn8 ():
        global serverTurn
        if serverTurn == 1:
            serverTurn = 0
            msg = 'h_cmd'
            client.send(msg.encode('utf-8'))
            btn8['text']='O'
            btn8['state']= tkinter.DISABLED
    def sendbtn9 ():
        global serverTurn
        if serverTurn == 1:
            serverTurn = 0
            msg = 'i_cmd'
            client.send(msg.encode('utf-8'))
            btn9['text']='O'
            btn9['state']= tkinter.DISABLED
    ##########################################################################################################################      
    #Creating a window
    window = tkinter.Tk()
    window.title('SERVER')
    window['bg']='gray98'
    window['padx']=10
    window['pady']=10
    #Label
    lbl = tkinter.Label(window,text='TIC-TAC-TOE')
    lbl['font']=35
    lbl['bg']='white'
    lbl.grid(column=2,row=0,padx=5,pady=5)
    #Label
    lbl2= tkinter.Label(window,text='Client-X')
    lbl2['font']=35
    lbl2['bg']='white'
    lbl2.grid(column=1,row=1,padx=5,pady=5)
    #Label
    lbl3 = tkinter.Label(window,text='Server-O')
    lbl3['font']=35
    lbl3['bg']='white'
    lbl3.grid(column=3,row=1,padx=5,pady=5)

    lbl5 = tkinter.Label(window,text='StartGame')
    lbl5['font']=35
    lbl5['bg']='white'
    lbl5.grid(column=2,row=1,padx=5,pady=5)
    #Button
    btn1 = tkinter.Button(window)
    btn1['relief']=tkinter.GROOVE
    btn1['bg']='white'
    btn1['fg']='green'
    btn1['activebackground']='ivory3'
    btn1['padx']=3
    btn1['font']=35
    btn1['width']= 10
    btn1['height']= 5
    btn1.grid(column=1,row=2,padx=5,pady=5)
    #Button
    btn2 = tkinter.Button(window)
    btn2['relief']=tkinter.GROOVE
    btn2['bg']='white'
    btn2['fg']='green'
    btn2['activebackground']='ivory3'
    btn2['padx']=3
    btn2['font']=35
    btn2['width']= 10
    btn2['height']= 5
    btn2.grid(column=2,row=2,padx=5,pady=5)
    #Button
    btn3 = tkinter.Button(window)
    btn3['relief']=tkinter.GROOVE
    btn3['bg']='white'
    btn3['fg']='green'
    btn3['activebackground']='ivory3'
    btn3['padx']=3
    btn3['font']=35
    btn3['width']= 10
    btn3['height']= 5
    btn3.grid(column=3,row=2,padx=5,pady=5)
    #Button
    btn4 = tkinter.Button(window)
    btn4['relief']=tkinter.GROOVE
    btn4['bg']='white'
    btn4['fg']='green'
    btn4['activebackground']='ivory3'
    btn4['padx']=3
    btn4['font']=35
    btn4['width']= 10
    btn4['height']= 5
    btn4.grid(column=1,row=3,padx=5,pady=5)
    #Button
    btn5 = tkinter.Button(window)
    btn5['relief']=tkinter.GROOVE
    btn5['bg']='white'
    btn5['fg']='green'
    btn5['activebackground']='ivory3'
    btn5['padx']=3
    btn5['font']=35
    btn5['width']= 10
    btn5['height']= 5
    btn5.grid(column=2,row=3,padx=5,pady=5)
    #Button
    btn6 = tkinter.Button(window)
    btn6['relief']=tkinter.GROOVE
    btn6['bg']='white'
    btn6['fg']='green'
    btn6['activebackground']='ivory3'
    btn6['padx']=3
    btn6['font']=35
    btn6['width']= 10
    btn6['height']= 5
    btn6.grid(column=3,row=3,padx=5,pady=5)
    #Button
    btn7 = tkinter.Button(window)
    btn7['relief']=tkinter.GROOVE
    btn7['bg']='white'
    btn7['fg']='green'
    btn7['activebackground']='ivory3'
    btn7['padx']=3
    btn7['font']=35
    btn7['width']= 10
    btn7['height']= 5
    btn7.grid(column=1,row=4,padx=5,pady=5)
    #Button
    btn8 = tkinter.Button(window)
    btn8['relief']=tkinter.GROOVE
    btn8['bg']='white'
    btn8['fg']='green'
    btn8['activebackground']='ivory3'
    btn8['padx']=3
    btn8['font']=35
    btn8['width']= 10
    btn8['height']= 5
    btn8.grid(column=2,row=4,padx=5,pady=5)
    #Button
    btn9 = tkinter.Button(window)
    btn9['relief']=tkinter.GROOVE
    btn9['bg']='white'
    btn9['fg']='green'
    btn9['activebackground']='ivory3'
    btn9['padx']=3
    btn9['font']=35
    btn9['width']= 10
    btn9['height']= 5
    btn9.grid(column=3,row=4,padx=5,pady=5)

    btn1['command']=sendbtn1
    btn2['command']=sendbtn2
    btn3['command']=sendbtn3
    btn4['command']=sendbtn4
    btn5['command']=sendbtn5
    btn6['command']=sendbtn6
    btn7['command']=sendbtn7
    btn8['command']=sendbtn8
    btn9['command']=sendbtn9
    
    t1 = StoppableThread(target=socketCreation)
    t1.start()  
    print('checkkkkkkkkkkkkkkkkkkkk1111111111111111111 ',t1.stopped())
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):        
            t1.stop()
            msg  = 'serverLeaveRoom_123'
            print('checkkkkkkkkkkkkkkkkkkkk 2222222222222222222 ',t1.stopped())
            client.send(msg.encode('utf-8'))
            time.sleep(1)
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing) 
    window.mainloop()
                                

def gui():
    root = tkinter.Tk()
    root.title("Tic Tac Toe")
    canvas = tkinter.Canvas(root, height=500, width=800,bg="white")
    canvas.pack()
    img = tkinter.PhotoImage(file="ox_logo1.png")    
    photoimage = img.subsample(1, 1) 
    button = tkinter.Button(canvas, image = img ).pack(ipadx = 10,ipady = 10)

    def Hall():  
        def show():     
            try: 
                f = open('Allname.txt')
            except IOError:
                print("Error : can't find file or read data")
            finally:
                datalist = []
                for i in f:
                    name, count, win,lose,rate = i.split()
                    rate = float(rate)
                    datalist.append([name, count, win,lose,"{0:.2f}".format(rate)])
                print(datalist)
                f.close()

            tempList = datalist
            tempList.sort(key=lambda e: e[4], reverse=True)
            for record in listBox.get_children():
		            listBox.delete(record)
            for i, (name,count,win,lose,rate) in enumerate(tempList, start=1):
                listBox.insert("", "end", values=(name,count,win,lose,rate))
           
        scores = tkinter.Tk() 
        label = tkinter.Label(scores, text="Hall of Fame", font=("Courier",25)).grid(row=0, columnspan=3)
        
        cols = ('Name', 'Played time', 'Win','Lose','Win rate')
        listBox = ttk.Treeview(scores, columns=cols, show='headings')   
        for col in cols:
            listBox.heading(col, text=col)    
            listBox.grid(row=1, column=0, columnspan=2)
        
        show()
        showScores = tkinter.Button(scores, bg="#fab1a0", font=('Courier',13),text="Refresh", width=15, command=show).grid(row=2, column=1)
        scores.mainloop()
    
        
    button = tkinter.Button(canvas, text='Hall of Fame',font=("Arial",13),bg="white" ,command=Hall)
    button.place(relx=0.35, relwidth=0.3, relheight=0.1,rely = 0.84)      
    root.resizable(0,0) 
    _thread.start_new_thread(wait_accept, () )   
    root.mainloop()

  
gui()
# upload()
     
