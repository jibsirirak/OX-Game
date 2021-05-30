from socket import *
from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import simpledialog
import _thread
import ftplib
import sys
from tkinter import messagebox
import math

client = 0
clientTurn = 0
counter = 0
symbols = ''
symbols2  = ''
started = '0'
allroom  =[]
name = 'unknow'
statesocket = False

def play(root0):
    def sendWinner(msg):
        msg1 ,obj = msg.split('_')
        client.send(msg.encode('utf-8'))
        lbl5['text'] = msg1
        btn1['state']= tkinter.DISABLED
        btn2['state']= tkinter.DISABLED
        btn3['state']= tkinter.DISABLED
        btn4['state']= tkinter.DISABLED
        btn5['state']= tkinter.DISABLED
        btn6['state']= tkinter.DISABLED
        btn7['state']= tkinter.DISABLED
        btn8['state']= tkinter.DISABLED
        btn9['state']= tkinter.DISABLED
        global clientTurn
        clientTurn = started
        global counter
        counter = 0

    def check():
    #If Client - X is the winner   
        if(btn1['text'] == 'X'):
            if(btn2['text']=='X'):
                if(btn3['text']=='X'):
                    sendWinner('X-Winner_'+symbols)
            if(btn4['text']=='X'):
                if(btn7['text']=='X'):
                    sendWinner('X-Winner_'+symbols)
            if(btn5['text']=='X'):
                if(btn9['text']=='X'):
                    sendWinner('X-Winner_'+symbols)
        if(btn2['text'] == 'X'):
            if(btn5['text']=='X'):
                if(btn8['text']=='X'):
                    sendWinner('X-Winner_'+symbols)
        if(btn3['text'] == 'X'):
            if(btn5['text']=='X'):
                if(btn6['text']=='X'):
                    sendWinner('X-Winner_'+symbols)
        if(btn7['text'] == 'X'):
            if(btn8['text']=='X'):
                if(btn9['text']=='X'):
                    sendWinner('X-Winner_'+symbols)
        if(btn3['text'] == 'X'):
            if(btn5['text']=='X'):
                if(btn7['text']=='X'):
                    sendWinner('X-Winner_'+symbols)
            if(btn6['text']=='X'):
                if(btn9['text']=='X'):
                    sendWinner('X-Winner_'+symbols)
        
    #If Server - O is the Winner
        if(btn1['text'] == 'O'):
            if(btn2['text']=='O'):
                if(btn3['text']=='O'):
                    sendWinner('O-Winner_'+symbols)
            if(btn4['text']=='O'):
                if(btn7['text']=='O'):
                    sendWinner('O-Winner_'+symbols)
            if(btn5['text']=='O'):
                if(btn9['text']=='O'):
                    sendWinner('O-Winner_'+symbols)
        if(btn2['text'] == 'O'):
            if(btn5['text']=='O'):
                if(btn8['text']=='O'):
                    sendWinner('O-Winner_'+symbols)
        if(btn3['text'] == 'O'):
            if(btn5['text']=='O'):
                if(btn6['text']=='O'):
                    sendWinner('O-Winner_'+symbols)
        if(btn7['text'] == 'O'):
            if(btn8['text']=='O'):
                if(btn9['text']=='O'):
                    sendWinner('O-Winner_'+symbols)
        if(btn3['text'] == 'O'):
            if(btn5['text']=='O'):
                if(btn7['text']=='O'):
                    sendWinner('O-Winner_'+symbols)
            if(btn6['text']=='O'):
                if(btn9['text']=='O'):
                    sendWinner('O-Winner_'+symbols) 
        if(counter == 5):
                sendWinner('It\'s a Tie_'+symbols)

    def on_closing():
        global statesocket
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            msg  = 'leaveRoom_123'
            client.send(msg.encode('utf-8'))
            statesocket = False
            root0.deiconify()
            window.destroy()

    def on_serverClosing():
        global statesocket
        statesocket = False
        root0.deiconify()
        window.destroy()

    # ***************************************************************************************************************************************************
    def socketCreation ():    
        global client,clientTurn,symbols,symbols2,counter,started,statesocket
        client.send(('setName'+'_'+name).encode('utf-8'))
        statesocket = True
        while statesocket:
            try:
                msg= c.recv(2048).decode('utf-8')
                print('recive msg = ',msg)
                msg ,obj = msg.split('_')
            except :
                print('server disconnect')    
                break
            else:
                if msg =="serverLeaveRoom":
                     msg2 = 'leaveRoom_123'
                     client.send(msg2.encode('utf-8'))
                     on_serverClosing()
                    
                if msg == "showAllRooms":
                    print('All rooms is ')
                    for i in obj.split(';'):
                        print(i + ' ')
                    
                if msg == "startGame":
                    global symbols , symbols2
                    started = int(obj)
                    clientTurn = started
                    if started == 1:
                        symbols = 'X'
                        symbols2 ='O'
                    else:
                        symbols = 'O'
                        symbols2 = 'X'
                    print('start at ',started)
                    lbl2['text'] = 'Your symbol-'+symbols
                    lbl3['text'] = 'another-'+symbols2
                    lbl5['text'] = 'StartGame'
                if msg == "It\'s a Tie" :
                    counter = 5
                    check()
                if msg == 'another player offline' :
                    print('another player offline')
                    messagebox.showinfo("Alert", "Another player offline, YOU WIN!!!")
                    sendWinner(symbols+'-Winner_'+symbols)
                if ( msg == 'a' and clientTurn == 0):
                    if symbols == 'X' :
                        btn1['text']='O'
                    else:
                        btn1['text']='X'
                    btn1['state']= tkinter.DISABLED
                    clientTurn = 1
                    check()
                elif ( msg == 'b' and clientTurn == 0):
                    if symbols == 'X' :
                        btn2['text']='O'
                    else:
                        btn2['text']='X'
                    btn2['state']= tkinter.DISABLED
                    clientTurn = 1
                    check()
                elif ( msg == 'c' and clientTurn == 0):
                    if symbols == 'X' :
                        btn3['text']='O'
                    else:
                        btn3['text']='X'
                    btn3['state']= tkinter.DISABLED
                    clientTurn = 1
                    check()
                elif ( msg == 'd' and clientTurn == 0):
                    if symbols == 'X' :
                        btn4['text']='O'
                    else:
                        btn4['text']='X'
                    btn4['state']= tkinter.DISABLED
                    clientTurn = 1
                    check()
                elif ( msg == 'e' and clientTurn == 0):
                    if symbols == 'X' :
                        btn5['text']='O'
                    else:
                        btn5['text']='X'
                    btn5['state']= tkinter.DISABLED
                    clientTurn = 1
                    check()
                elif ( msg == 'f' and clientTurn == 0):
                    if symbols == 'X' :
                        btn6['text']='O'
                    else:
                        btn6['text']='X'
                    btn6['state']= tkinter.DISABLED
                    clientTurn = 1
                    check()
                elif ( msg == 'g' and clientTurn == 0):
                    if symbols == 'X' :
                        btn7['text']='O'
                    else:
                        btn7['text']='X'
                    btn7['state']= tkinter.DISABLED
                    clientTurn = 1
                    check()
                elif ( msg == 'h' and clientTurn == 0):
                    if symbols == 'X' :
                        btn8['text']='O'
                    else:
                        btn8['text']='X'
                    btn8['state']= tkinter.DISABLED
                    clientTurn = 1
                    check()
                elif ( msg == 'i' and clientTurn == 0):
                    if symbols == 'X' :
                        btn9['text']='O'
                    else:
                        btn9['text']='X'
                    btn9['state']= tkinter.DISABLED
                    clientTurn = 1
                    check()
        print('exit')
                    
    def sendbtn1 ():
        print('sendBtn1')
        global clientTurn,symbols
        if clientTurn == 1:
            clientTurn = 0
            msg = 'game_a'
            client.send(msg.encode('utf-8'))
            if symbols == 'X' :
                btn1['text']='X'
            else:
                btn1['text']='O'
            btn1['state']= tkinter.DISABLED
            print('useSetBtn1 : ',msg)
            global counter
            counter += 1
            check()
    def sendbtn2 ():
        print('sendBtn2')
        global clientTurn,symbols
        if clientTurn == 1:
            clientTurn = 0
            msg = 'game_b'
            client.send(msg.encode('utf-8'))
            print('send , ',msg)
            if symbols == 'X' :
                btn2['text']='X'
            else:
                btn2['text']='O'
            btn2['state']= tkinter.DISABLED
            global counter
            counter += 1
            check()
    def sendbtn3 ():
        print('sendBtn3')
        global clientTurn,symbols
        if clientTurn == 1:
            clientTurn = 0
            msg = 'game_c'
            client.send(msg.encode('utf-8'))
            if symbols == 'X' :
                btn3['text']='X'
            else:
                btn3['text']='O'
            btn3['state']= tkinter.DISABLED
            global counter
            counter += 1
            check()
    def sendbtn4 ():
        print('sendBtn4')
        global clientTurn,symbols
        if clientTurn == 1:
            clientTurn = 0
            msg = 'game_d'
            client.send(msg.encode('utf-8'))
            if symbols == 'X' :
                btn4['text']='X'
            else:
                btn4['text']='O'
            btn4['state']= tkinter.DISABLED
            global counter
            counter += 1
            check()
    def sendbtn5 ():
        print('sendBtn5')
        global clientTurn,symbols
        if clientTurn == 1:
            clientTurn = 0
            msg = 'game_e'
            client.send(msg.encode('utf-8'))
            if symbols == 'X' :
                btn5['text']='X'
            else:
                btn5['text']='O'
            btn5['state']= tkinter.DISABLED
            global counter
            counter += 1
            check()
    def sendbtn6 ():
        print('sendBtn6')
        global clientTurn,symbols
        if clientTurn == 1:
            clientTurn = 0
            msg = 'game_f'
            client.send(msg.encode('utf-8'))
            if symbols == 'X' :
                btn6['text']='X'
            else:
                btn6['text']='O'
            btn6['state']= tkinter.DISABLED
            global counter
            counter += 1
            check()
    def sendbtn7 ():
        print('sendBtn7')
        global clientTurn,symbols
        if clientTurn == 1:
            clientTurn = 0
            msg = 'game_g'
            client.send(msg.encode('utf-8'))
            if symbols == 'X' :
                btn7['text']='X'
            else:
                btn7['text']='O'
            btn7['state']= tkinter.DISABLED
            global counter
            counter += 1
            check()
    def sendbtn8 ():
        print('sendBtn8')
        global clientTurn,symbols
        if clientTurn == 1:
            clientTurn = 0
            msg = 'game_h'
            client.send(msg.encode('utf-8'))
            if symbols == 'X' :
                btn8['text']='X'
            else:
                btn8['text']='O'
            btn8['state']= tkinter.DISABLED
            global counter
            counter += 1
            check()
    def sendbtn9 ():
        print('sendBtn9')
        global clientTurn,symbols
        if clientTurn == 1:
            clientTurn = 0
            msg = 'game_i'
            client.send(msg.encode('utf-8'))
            if symbols == 'X' :
                btn9['text']='X'
            else:
                btn9['text']='O'
            btn9['state']= tkinter.DISABLED
            global counter
            counter += 1
            check()
    ###########################################################################################################################################################    ###############################
    #Creating a window
    window = Toplevel()
    window.title('CLIENT')
    window['bg']='gray98'
    window['padx']=10
    window['pady']=10
    #Label
    lbl = tkinter.Label(window,text='TIC-TAC-TOE')
    lbl['font']=35
    lbl['bg']='white'
    lbl.grid(column=2,row=0,padx=5,pady=5)
    #Label
    lbl2= tkinter.Label(window,text='')
    lbl2['font']=35
    lbl2['bg']='white'
    lbl2.grid(column=1,row=1,padx=5,pady=5)
    #Label
    lbl3 = tkinter.Label(window,text='')
    lbl3['font']=35
    lbl3['bg']='white'
    lbl3.grid(column=3,row=1,padx=5,pady=5)
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

    lb4 = tkinter.Label(window,text='Welcome  ' + name)
    lb4['font']=35
    lb4['bg']='white'
    lb4.grid(column=2,row=5,padx=5,pady=5)

    lbl5 = tkinter.Label(window,text='Waiting...')
    lbl5['font']=35
    lbl5['bg']='white'
    lbl5.grid(column=2,row=1,padx=5,pady=5)

    btn1['command']=sendbtn1
    btn2['command']=sendbtn2
    btn3['command']=sendbtn3
    btn4['command']=sendbtn4
    btn5['command']=sendbtn5
    btn6['command']=sendbtn6
    btn7['command']=sendbtn7
    btn8['command']=sendbtn8
    btn9['command']=sendbtn9
    
    _thread.start_new_thread(socketCreation, () )
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

def download():
        input = open("login.txt")
        for line in input:
            in1, in2, in3, in4 = line.split()
        input.close()
        ftp = ftplib.FTP(in1)
        ftp.login(user=in2,passwd=in3)
        ftp.cwd('Assigngroup1')
        filename = 'Allname.txt'
        localfile = open(filename, 'wb')
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()
        ftp.retrlines('LIST')
        ftp.quit()
    
def gui():
    root0 = tkinter.Tk()
    root0.title("Tic Tac Toe")
    
    canvas = tkinter.Canvas(root0, height=500, width=800,bg="light sea green", relief=GROOVE,bd=10)
    canvas.pack()
    
    frame = tkinter.Frame(root0, bg='skyblue', bd=10, relief=RIDGE)
    frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.8, anchor='n')

    lbl = tkinter.Label(frame, text="Please Enter Your Name:",font=('Courier', 18),bg='skyblue')
    lbl.place(relwidth=0.9, relheight=0.1)

    entry = tkinter.Entry(frame, font=18)
    entry.place(relwidth=0.55, relheight=0.1,rely = 0.15,relx = 0.05)
       
    def getName():
        global name
        name = entry.get()
        lbl = tkinter.Label(frame, text="Welcome " +name,font=('Courier', 18),bg='skyblue')
        lbl.place(relwidth=1, relheight=0.1,rely=0.3)
        print('name: ',name)
    
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

    def guiRoom():
        root0.withdraw()
        global client,c,allroom   
        c =socket(AF_INET,SOCK_STREAM)
        c.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        host = gethostname()
        port = 5000
        c.connect((host,port))
        client =c 
        client.send(('multiplayer').encode('utf-8'))

        root = tkinter.Tk()
        root.title("Tic Tac Toe")
        
        canvas = tkinter.Canvas(root, height=500, width=800,bg="light sea green", relief=GROOVE,bd=10)
        canvas.pack()
            
        frame = tkinter.Frame(root, bg='skyblue', relief=GROOVE,bd=10)
        frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.8, anchor='n')
       
        def popup():
            roomCode = simpledialog.askstring("Create Room", "Name")
            if roomCode:
                client.send(('createRoom'+'_'+roomCode).encode('utf-8'))
                
        def showRooms():
            global allroom
            state = 0
            while True:
                try:
                    msg= client.recv(2048).decode('utf-8')
                    print('recive msg = ',msg)
                    msg ,obj = msg.split('_')
                except:
                    print('error join room')
                    break
                if msg == "showAllRooms":
                    allroom = []
                    for i in obj.split(';'):
                        if i != '':
                            allroom.append(i)
                    listbox1.delete(0, END)
                    for x in allroom:  
                        listbox1.insert(END, x)
                    print('allroom: ',allroom)
                elif msg == 'statuscreateRoom' :
                    if obj == "can't create Room":
                            messagebox.showerror("Alert", "Room is have already!")
                    if obj == "can create Room" :
                            messagebox.showinfo("Alert", "Create room success!")
                elif msg == 'statusRoom':
                    if obj == "can't join":
                        messagebox.showerror("Alert",'Room is full!!!.')
                    if obj == "can join":
                        state = 1
                        root.destroy()
                        break
                    if obj == "This room does not have":
                       messagebox.showerror("Alert","Don't have this room.")
            if state == 1:
                play(root0)
        def reRoom():
            client.send(("showAllRooms"+'_'+'123').encode('utf-8'))

        frame1 = tkinter.Frame(frame, bg='Powder Blue', relief=GROOVE,bd=10)
        frame1.place(rely=0.05,relwidth=0.5, relheight=0.9, relx=0.01)
        
        listbox1=Listbox(frame1, background="white", fg="black",  
                 highlightbackground="blue",highlightthickness=10,  
                 selectbackground="green",highlightcolor="red")  
        listbox1.place(rely=0.15,relwidth=0.7, relheight=0.65, relx=0.15)  
 
        btnAdd = tkinter.Button(frame1,text="Create Room",font=('Courier', 13), bg='#fab1a0',command=popup)
        btnAdd.place(relx=0.49, relwidth=0.5, relheight=0.1,rely=0.01)
        
        reroombutton = tkinter.Button(frame1, text='ReRoom', font=('Courier', 16),bg='#fab1a0',command = reRoom)
        reroombutton.place(relx=0.25, relwidth=0.5, relheight=0.1,rely = 0.85)
  
        lbl = tkinter.Label(frame, text="Room Number:" ,font=('Courier', 14),bg='skyblue')
        lbl.place(relwidth=0.3, relheight=0.1,relx=0.565)
        
        entry = tkinter.Entry(frame, font=('Courier', 16))
        entry.place(relwidth=0.3, relheight=0.1,rely = 0.1,relx=0.6)
        
        def sent_joint():       
            text = entry.get()
            print("joint :" + text)
            client.send(('joinRoom'+'_'+text).encode('utf-8'))

        def backtoMenu():
            client.send(('exit'+'_'+'111').encode('utf-8'))
            client.close()
            root.destroy()
            root0.deiconify()
                           
        btnEnter = tkinter.Button(frame,text="Enter",font=('Courier', 16), bg='#fab1a0',command=sent_joint)
        btnEnter.place(relx=0.65, relwidth=0.2, relheight=0.1,rely=0.25)

        backbutton = tkinter.Button(frame, text='Back', font=('Courier', 16),bg='Powder Blue', command=backtoMenu)
        backbutton.place(relx=0.7, relwidth=0.25, relheight=0.1,rely = 0.85)

        root.resizable(0,0)    
        root.protocol("WM_DELETE_WINDOW", backtoMenu)
        _thread.start_new_thread(showRooms, () )
        root.mainloop()

    def modeHost():
        global client,c
        c =socket(AF_INET,SOCK_STREAM)
        c.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        host = gethostname()
        port = 5000
        c.connect((host,port))
        client =c 
        client.send(('play with host').encode('utf-8'))
        try:
            msg= client.recv(2048).decode('utf-8')
            print('recive msg = ',msg)
        except:
            print('error join room')
        if msg == "can't join":
            messagebox.showinfo("Alert", "HOST is playing with other player")
            client.close()
        if msg == "can join":
            play(root0)
            client.close()
    
    button = tkinter.Button(frame, text='Ok', font=40,command=getName,bg="#fab1a0")
    button.place(relx=0.65, relwidth=0.3, relheight=0.1,rely = 0.15)
    
    button = tkinter.Button(frame, text='Play with Host', font=40,bg="Powder Blue",command=modeHost)
    button.place(relx=0.35, relwidth=0.3, relheight=0.1,rely = 0.45)
        
    button = tkinter.Button(frame, text='Play with another', font=40,bg="Powder Blue",command=guiRoom)
    button.place(relx=0.35, relwidth=0.3, relheight=0.1 ,rely = 0.65)
        
    button = tkinter.Button(frame, text='Hall of Fame', font=40,bg="Powder Blue" ,command=Hall)
    button.place(relx=0.35, relwidth=0.3, relheight=0.1,rely = 0.85)
        
    root0.resizable(0,0) 
    root0.mainloop()

# download()
gui()


    

