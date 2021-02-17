import socket
import tkinter as tk
import threading
import time
import pygame
import tkinter.font as tkFont
import random
HOST="127.0.0.1"
PORT=8080
DISCONNECT_MESSAGE="disconnect"
ADDR=(HOST,PORT)

pygame.mixer.init()
track = pygame.mixer.music.load("sound/lobby.mp3")
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(ADDR)
print("[CLIENT CONNECT]")

username=""
roommember=[]
roomcolor=[]
cardpoint=[]
playercard={} #紀錄每個玩家現有手牌 若有更新才跑動畫
messagequeue=[]
gamblemoney=int(0)
tigerflag=False
createflag=False
def drawthread():
    global registerror,entererror,lobbyentry,finalcolor,player,_21_canvas,entererrorlabel,_21_card,_21_finish,_21_opencard,_21_return,_21_cleantable,_21_return2
    global lobby_money,_21_invitelistbt,registerrorlabel,track,tigerflag,createflag

    while True:
        time.sleep(0.05)
        if tigerflag==True:
            tigerflag=False
            playtiger()
        if createflag==True:
            createflag=False
            whitelight()
            delcreatecharacterlayout()
            setlobbylayout()
        if len(messagequeue)>0:
            x=messagequeue[0]
            messagequeue[0:1]=[]
            x=x.split()
            print(x)
            if x[0]=="registfail":
                track = pygame.mixer.music.load("sound/fail.mp3")
                pygame.mixer.music.play()
                registerror.set("username has been exited!")
                registerrorlabel.place(x=300,y=420)
            elif x[0]=="bye":
                break
            elif x[0]=="registsuccess":
                track = pygame.mixer.music.load("sound/registsuccess.mp3")
                pygame.mixer.music.play()
                time.sleep(0.3)
                registback()  
                entererror.set("regist success!!")
                entererrorlabel.place(x=600,y=415)
                  
            elif x[0]=="needcharacter":
                deluserentrylayout()
                setcreatecharacterlayout()
            elif x[0]=="enterroomfail":
                enterroomfail()
            elif x[0]=="enterroomsuccess":
                goto21()
            elif x[0]=="youareinvited":
                setinvite(x[1])
            elif x[0]=="entersuccess":
                track = pygame.mixer.music.load("sound/enterlobby.mp3")
                pygame.mixer.music.play()
                whitelight()
                finalcolor=x[1]
                deluserentrylayout()
                setlobbylayout()
            elif x[0]=="gamble":
                _21_return.place_forget()
                _21_invitelistbt.place_forget()
                _21_frame.place_forget()
                _21_secondlist.place_forget()
                setgamble(username)
            elif x[0]=="setuserinfo": #設定玩家資訊 名字 賭金
                setuserinfo(x[1],x[2])
            elif x[0]=="cardpoint":
                setcardpoint(x[1])
                time.sleep(0.5)
            elif x[0]=="gamestart":
                track = pygame.mixer.music.load("sound/遊戲開始.mp3")
                pygame.mixer.music.play()
                for i in roommember:
                    playercard[i]=""
                _21_gamestart=tk.PhotoImage(file="image/gamestart.png")
                _21_canvas.create_image(650,400,image=_21_gamestart)
                time.sleep(1)
                _21_cleantable=tk.PhotoImage(file="image/cleantable.png")
                _21_canvas.create_image(650,400,image=_21_cleantable)
            elif x[0]=="usermoney":
                tmp="資金:"
                tmp+=x[1]
                lobby_money.set(tmp)
            elif x[0]=="playeraction":
                playeraction(x[1],x[2])
            elif x[0]=="nowplayer":
                nplayer(x[1],x[2])
            elif x[0]=="finish":
                track = pygame.mixer.music.load("sound/遊戲結束.mp3")
                pygame.mixer.music.play()
                playercard.clear()
                _21_giveupcardbt.place_forget()
                _21_requestcardbt.place_forget()
                _21_canvas.create_image(650,400,image=_21_finish)
                time.sleep(1)
                _21_canvas.create_image(650,400,image=_21_opencard)
                time.sleep(1)
                _21_cleantable=tk.PhotoImage(file="image/cleantable.png")
                _21_canvas.create_image(650,400,image=_21_cleantable)
            elif x[0]=="opencard":
                opencard(username,x)
            elif x[0]=="refreshusercard": #更新每個人的牌
                refresh(x)
            elif x[0]=="invitelist":
                setlistbox(x)
            elif x[0]=="talklist1":
                settalklistbox(x)
            elif x[0]=="talklist2":
                inserttalklist(x)
            elif x[0]=="roommember":
                for i in range(1,len(x)):
                    if i%2==0:
                        if (i//2)-1>=len(roommember):
                            roommember.append(x[i-1])
                            roomcolor.append(x[i])
                        else :
                            roommember[(i//2)-1]=x[i-1]
                            roomcolor[(i//2)-1]=x[i]
                draw21character()

            elif x[0]=="enterfail":
                track = pygame.mixer.music.load("sound/fail.mp3")
                pygame.mixer.music.play()
                if x[1]=="noname":
                    entererror.set("查無此人")
                    entererrorlabel.place(x=600,y=415)
                else:
                    entererror.set("密碼錯誤")
                    entererrorlabel.place(x=600,y=415)
def whitelight():
    canvas2=tk.Canvas(window,width=1300,height=800)
    canvas2.create_rectangle(0,0,1300,800,fill="black")
    canvas2.place(x=0,y=0)
    for i in range(21):
        canvas2.create_oval(650-65*i,400-40*i,650+65*i,400+40*i,fill="white")
        time.sleep(0.01)
    time.sleep(0.5)
def accept():
    # dellobbylayout()
    trygoto21()
def refuse():
    dellobbyinvitebox()
def setinvite(inviteuser):
    global lobby_canvas,lobby_invitebox,lobby_invitemsg,lobby_inviterefuse,lobby_inviteuser,lobby_inviteaccept,lobby_ivstr
    tmp=tk.PhotoImage(file="image/invitebox.png")
    lobby_ivstr.set(inviteuser)
    for i in range(10):
        lobby_canvas.create_image(i*15,700,image=tmp)
        time.sleep(0.1)
    lobby_invitebox=tk.PhotoImage(file="image/invitebox.png")
    lobby_canvas.create_image(150,700,image=lobby_invitebox)
    lobby_inviteuser=tk.Label(window,font="微軟正黑體 16 bold",fg="MidnightBlue",bg="Plum",textvariable=lobby_ivstr)
    lobby_invitemsg=tk.Label(window,font="微軟正黑體 16 bold",fg="MidnightBlue",bg="Plum",text="邀請你一同遊玩")
    lobby_inviteaccept=tk.Button(window,text="接受",command=accept)
    lobby_inviterefuse=tk.Button(window,text="拒絕",command=refuse)
    lobby_inviteuser.place(x=100,y=660)
    lobby_invitemsg.place(x=100,y=690)
    lobby_inviterefuse.place(x=150,y=720)
    lobby_inviteaccept.place(x=100,y=720)
def enterroomfail():
    global lobby_canvas
    tmp=tk.PhotoImage(file="image/fullroom.png")
    lobby_canvas.create_image(430,270,image=tmp)
    time.sleep(2)
def shownumber(point,x,y):
    # print(f"x={x}")
    # print(f"y={y}")
    global _21_canvas,_21_fnumber,_21_snumber
    _21_snumber.append(tk.PhotoImage())
    _21_fnumber.append(tk.PhotoImage())
    a=len(_21_snumber)-1
    b=len(_21_fnumber)-1
    if (point//10)==0:
        _21_fnumber[b]=tk.PhotoImage(file="image/0.png")
    elif (point//10)==1:
         _21_fnumber[b]=tk.PhotoImage(file="image/1.png")
    elif (point//10)==2:
         _21_fnumber[b]=tk.PhotoImage(file="image/2.png")
    elif (point//10)==3:
         _21_fnumber[b]=tk.PhotoImage(file="image/3.png")
    if (point%10)==0:
        _21_snumber[a]=tk.PhotoImage(file="image/0.png")
    elif (point%10)==1:
        _21_snumber[a]=tk.PhotoImage(file="image/1.png")
    elif (point%10)==2:
        _21_snumber[a]=tk.PhotoImage(file="image/2.png")
    elif (point%10)==3:
        _21_snumber[a]=tk.PhotoImage(file="image/3.png")
    elif (point%10)==4:
        _21_snumber[a]=tk.PhotoImage(file="image/4.png")
    elif (point%10)==5:
        _21_snumber[a]=tk.PhotoImage(file="image/5.png")
    elif (point%10)==6:
        _21_snumber[a]=tk.PhotoImage(file="image/6.png")
    elif (point%10)==7:
        _21_snumber[a]=tk.PhotoImage(file="image/7.png")
    elif (point%10)==8:
        _21_snumber[a]=tk.PhotoImage(file="image/8.png")
    elif (point%10)==9:
        _21_snumber[a]=tk.PhotoImage(file="image/9.png")
    _21_canvas.create_image(x,y,image=_21_fnumber[b])
    _21_canvas.create_image(x+35,y,image=_21_snumber[a])
def showcardpoint(j,point):
    index=-1
    for i in range(4):
        if roommember[i]==username:
            index=i
            break
    # print(f"i={i}")
    # print(f"index={index}")
    if (j+4-index)%4==0: #中下
        shownumber(point,600,460)
    elif (j+4-index)%4==1: #右
        shownumber(point,800,360)
    elif (j+4-index)%4==2: #中上
        shownumber(point,600,260)
    elif (j+4-index)%4==3: #左
        shownumber(point,400,360)

def gif(x,y,imgpath):
    global _21_canvas
    
    for i in range(1,6):
        ipath=imgpath+str(i)+".png"
        photo=tk.PhotoImage(file=ipath)
        _21_canvas.create_image(x,y,image=photo)
        time.sleep(0.20)
def lossmoney(i,i2):
    global lobby_money,_21_canvas,_21_moneyinfo,_21_moneytext,gamblemone
    index=-1
    tmp=int(gamblemone[i2])
    for j in range(4):
        if roommember[j]==username:
            index=j
            break
    if i>0:                                     #玩家--------------------------
        track = pygame.mixer.music.load("sound/loss.mp3")
        pygame.mixer.music.play()
        _21_moneytext[i].set("賭金: 0")
        if (i+4-index)%4==0: #中下
            if tmp==20:
                gif(630,720,"image/m20")
            elif tmp==10:
                gif(630,720,"image/m10")
            elif tmp==5:
                gif(630,720,"image/m5")
        elif (i+4-index)%4==1: #右
            if tmp==20:
                gif(1140,390,"image/m20")
            elif tmp==10:
                gif(1140,390,"image/m10")
            elif tmp==5:
                gif(1140,390,"image/m5")
        elif (i+4-index)%4==2: #中上
            if tmp==20:
                gif(620,50,"image/m20")
            elif tmp==10:
                gif(620,50,"image/m10")
            elif tmp==5:
                gif(620,50,"image/m5")
        elif (i+4-index)%4==3: #左
            if tmp==20:
                gif(110,390,"image/m20")
            elif tmp==10:
                gif(110,390,"image/m10")
            elif tmp==5:
                gif(110,390,"image/m5")

    if roommember[i]==username:
        msg="loss "+str(tmp)
        clientsocket.send(msg.encode())
    
def earnmoney(i,i2):
    global lobby_money,_21_canvas,_21_moneytext,_21_moneyinfo,gamblemone
    index=-1
    tmp=int(gamblemone[i2])
    for j in range(4):
        if roommember[j]==username:
            index=j
            break
    if i>0:                                     #玩家--------------------------
        track = pygame.mixer.music.load("sound/win.mp3")
        pygame.mixer.music.play()
        msg="賭金"+str(tmp*2)
        _21_moneytext[i].set(msg)
        if (i+4-index)%4==0: #中下
            if tmp==20:
                gif(630,720,"image/p20")
            elif tmp==10:
                gif(630,720,"image/p10")
            elif tmp==5:
                gif(630,720,"image/p5")
        elif (i+4-index)%4==1: #右
            if tmp==20:
                gif(1140,390,"image/p20")
            elif tmp==10:
                gif(1140,390,"image/p10")
            elif tmp==5:
                gif(1140,390,"image/p5")
        elif (i+4-index)%4==2: #中上
            if tmp==20:
                gif(620,50,"image/p20")
            elif tmp==10:
                gif(620,50,"image/p10")
            elif tmp==5:
                gif(620,50,"image/p5")
        elif (i+4-index)%4==3: #左
            if tmp==20:
                gif(110,390,"image/p20")
            elif tmp==10:
                gif(110,390,"image/p10")
            elif tmp==5:
                gif(110,390,"image/p5")
    if roommember[i]==username:
        msg="win "+str(tmp)
        clientsocket.send(msg.encode())
def compare():
    for i in range(1,4):
        if(cardpoint[i]>21 and cardpoint[0]>21):
            print(f"{i:}tie")
        else:
            if cardpoint[0]==-1:
                lossmoney(i,i)      
                earnmoney(0,i)
            elif cardpoint[i]==-1 :
                earnmoney(i,i)
                lossmoney(0,i)
            elif cardpoint[i]>21:
                lossmoney(i,i)
                earnmoney(0,i)
            elif cardpoint[0]>21:
                earnmoney(i,i)
                lossmoney(0,i)
            elif cardpoint[i]<=cardpoint[0]:
                lossmoney(i,i)
                earnmoney(0,i)
            else:
                earnmoney(i,i)
                lossmoney(0,i)
        time.sleep(1)
            
def setcardpoint(point):
    global _21_return2
    point=int(point)
    cardpoint.append(point)
    print(f"cardpoint{cardpoint}")
    print(f"len:{len(cardpoint)}")
    showcardpoint(len(cardpoint)-1,point)
    if len(cardpoint)==4:
        compare()
        cardpoint.clear()
        _21_return2=tk.Button(window,text="返回大廳",font="微軟正黑體 24 bold",command=returntolobby)
        _21_return2.place(x=0,y=700)

def setuserinfo(player,money):
    global username,_21_playerinfo,_21_moneyinfo,_21_moneytext,gamblemone
    index=-1
    for i in range(4):
        if roommember[i]==username:
            index=i
            break
    for i in range(4):
        if roommember[i]==player:
            gamblemone[i]=money
            _21_moneytext[i].set("賭金: "+money)
            if (i+4-index)%4==0: #中下
                _21_playerinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",text="玩家: "+player)
                _21_playerinfo[i].place(x=700,y=680)
                if player==roommember[0]:
                    _21_moneyinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",text="莊家")
                else:
                    _21_moneyinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",textvariable=_21_moneytext[i])
                _21_moneyinfo[i].place(x=700,y=730)
            elif (i+4-index)%4==1: #右
                _21_playerinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",text="玩家: "+player)
                _21_playerinfo[i].place(x=1090,y=450)
                if player==roommember[0]:
                    _21_moneyinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",text="莊家")
                else:
                    _21_moneyinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",textvariable=_21_moneytext[i])
                _21_moneyinfo[i].place(x=1090,y=500)
            elif (i+4-index)%4==2: #中上
                _21_playerinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",text="玩家: "+player)
                _21_playerinfo[i].place(x=700,y=10)
                if player==roommember[0]:
                    _21_moneyinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",text="莊家")
                else:
                    _21_moneyinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",textvariable=_21_moneytext[i])
                _21_moneyinfo[i].place(x=700,y=60)
            elif (i+4-index)%4==3: #左
                _21_playerinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",text="玩家: "+player)
                _21_playerinfo[i].place(x=60,y=450)
                if player==roommember[0]:
                    _21_moneyinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",text="莊家")
                else:
                    _21_moneyinfo[i]=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",textvariable=_21_moneytext[i])
                _21_moneyinfo[i].place(x=60,y=500)

def cardmove(destx,desty,cardimg):
    global _21_canvas

    tmp2=tk.PhotoImage(file="image/cleansender.png")
    _21_canvas.create_image(100,50,image=tmp2)
    tmp=tk.PhotoImage(file="image/cardsender_1.png")
    _21_canvas.create_image(100,50,image=tmp)
    time.sleep(0.4)
    track = pygame.mixer.music.load("sound/sendcard.mp3")
    pygame.mixer.music.play()
    tmp=tk.PhotoImage(file="image/cardsender_2.png")
    _21_canvas.create_image(100,50,image=tmp)
    difx=(float(destx)-100)/20
    dify=(float(desty)-50)/20
    for i in range(20):
        tmpimg=tk.PhotoImage(file=cardimg)
        _21_canvas.create_image(100+difx*i,50+dify*i,image=tmpimg)
        time.sleep(0.01)
    time.sleep(0.1)
def refresh(x):
    global _21_canvas,_21_card,username
    index=-1
    for i in range(4):
        if roommember[i]==username:
            index=i
            break

    for i in range(4):
        if roommember[i]==x[1]:
            pcard=playercard[roommember[i]]
            pcard=pcard.split(" ")
            for j in range(2,len(x)):
                if j-2>=len(pcard)-1:
                    playercard[roommember[i]]=playercard[roommember[i]]+" "+x[j]
                    tmp=whichcard(x[j],i,j-2)
                    if (i+4-index)%4==0: #中下
                        cardmove(490+70*(j-2),570,tmp)
                        _21_canvas.create_image(490+70*(j-2),570,image=_21_card[i][j-2])
                    elif (i+4-index)%4==1: #右
                        _21_card[i][j-2]=tk.PhotoImage(file="image/pokerbackr.png")
                        cardmove(950,540-70*(j-2),"image/pokerbackr.png")
                        _21_canvas.create_image(950,540-70*(j-2),image=_21_card[i][j-2])
                    elif (i+4-index)%4==2: #中上
                        _21_card[i][j-2]=tk.PhotoImage(file="image/pokerback.png")
                        cardmove(755-70*(j-2),200,"image/pokerback.png")
                        _21_canvas.create_image(755-70*(j-2),200,image=_21_card[i][j-2])
                    elif (i+4-index)%4==3: #左
                        _21_card[i][j-2]=tk.PhotoImage(file="image/pokerbackr.png")
                        cardmove(300,250+70*(j-2),"image/pokerbackr.png")
                        _21_canvas.create_image(300,250+70*(j-2),image=_21_card[i][j-2])

def playeraction(state,x): #每個玩家的動作
    global _21_giveupcardbt,_21_requestcardbt,_21_action,_21_canvas
    _21_giveupcardbt.place_forget()
    _21_requestcardbt.place_forget() #不要在跑動畫時讓玩家操作按鈕
    if int(state)==0:
        track = pygame.mixer.music.load("sound/過.mp3")
        pygame.mixer.music.play()
    else:
        track = pygame.mixer.music.load("sound/來.mp3")
        pygame.mixer.music.play()
    nowplayer=int(x)
    index=-1
    for i in range(4):
        if roommember[i]==username:
            index=i
            break
    for i in range(4):
        if nowplayer==i:
            if (i+4-index)%4==0: #中下
                if int(state)==0:
                    img=tk.PhotoImage(file="image/passd.png") 
                    _21_canvas.create_image(670,650,image=img)
                else:
                    img=tk.PhotoImage(file="image/comed.png") 
                    _21_canvas.create_image(670,650,image=img)
            elif (i+4-index)%4==1: #右
                if int(state)==0:
                    img=tk.PhotoImage(file="image/passr.png") 
                    _21_canvas.create_image(1040,340,image=img)
                else:
                    img=tk.PhotoImage(file="image/comer.png") 
                    _21_canvas.create_image(1040,340,image=img)
            elif (i+4-index)%4==2: #中上
                if int(state)==0:
                    img=tk.PhotoImage(file="image/passt.png") 
                    _21_canvas.create_image(570,170,image=img)
                else:
                    img=tk.PhotoImage(file="image/comet.png") 
                    _21_canvas.create_image(570,170,image=img)
            elif (i+4-index)%4==3: #左
                if int(state)==0:
                    img=tk.PhotoImage(file="image/passl.png") 
                    _21_canvas.create_image(210,450,image=img)
                else:
                    img=tk.PhotoImage(file="image/comel.png") 
                    _21_canvas.create_image(210,450,image=img)
    
    time.sleep(1)

def gamble5():
    global gamblemoney
    gamblemoney=int(5)
    clientsocket.send("setgamble 5".encode())
    delgamble()
def gamble10():
    global gamblemoney
    gamblemoney=int(10)
    clientsocket.send("setgamble 10".encode())
    delgamble()
def gamble20():
    global gamblemoney
    gamblemoney=int(20)
    clientsocket.send("setgamble 20".encode())
    delgamble()
def setgamble(username):
    global _21_5bt,_21_10bt,_21_20bt,_21_canvas,_21_gambletext,_21_5img,_21_10img,_21_20img
    if username!=roommember[0]:        
        _21_5img=tk.PhotoImage(file="image/5money.png")
        _21_10img=tk.PhotoImage(file="image/10money.png")
        _21_20img=tk.PhotoImage(file="image/20money.png")
        _21_5bt=tk.Button(window,image=_21_5img,bd=0,width=110,height=110,command=gamble5)
        _21_10bt=tk.Button(window,image=_21_10img,bd=0,width=110,height=110,command=gamble10)
        _21_20bt=tk.Button(window,image=_21_20img,bd=0,width=110,height=110,command=gamble20)
        _21_5bt.place(x=400,y=450)
        _21_10bt.place(x=600,y=450)
        _21_20bt.place(x=800,y=450)
        _21_gambletext=tk.PhotoImage(file="image/gambletext.png")
        _21_canvas.create_image(650,350,image=_21_gambletext)
    else:
        delgamble()

def delgamble():
    global _21_5bt,_21_10bt,_21_20bt,_21_canvas,_21_gambletext,_21_cleantable
    _21_5bt.place_forget()
    _21_10bt.place_forget()
    _21_20bt.place_forget()
    _21_cleantable=tk.PhotoImage(file="image/waitgamble.png")
    _21_canvas.create_image(650,350,image=_21_cleantable)
def opencard(username,x):
    global _21_canvas,_21_card
    index=-1
    for i in range(4):
        if roommember[i]==username:
            index=i
            break

    for i in range(4):
        if roommember[i]==x[1]:
            for j in range(2,len(x)):              
                if (i+4-index)%4==0: #中下
                    tmp=whichcard(x[j],i,j-2)
                    _21_canvas.create_image(490+70*(j-2),570,image=_21_card[i][j-2])
                elif (i+4-index)%4==1: #右
                    whichcardr(x[j],i,j-2)
                    _21_canvas.create_image(950,540-70*(j-2),image=_21_card[i][j-2])
                elif (i+4-index)%4==2: #中上
                    whichcardt(x[j],i,j-2)
                    _21_canvas.create_image(755-70*(j-2),200,image=_21_card[i][j-2])
                elif (i+4-index)%4==3: #左
                    whichcardl(x[j],i,j-2)
                    _21_canvas.create_image(300,250+70*(j-2),image=_21_card[i][j-2])

def nplayer(state,x): 
    global _21_giveupcardbt,_21_requestcardbt,_21_canvas,_21_whitehole,_21_whiteholerecover
    nowplayer=int(x)
    index=-1
    for i in range(4):
        if roommember[i]==username:
            index=i
            break
    if index==nowplayer: #輪到自己的回合
        if state=="0":
            _21_requestcardbt.place(x=850,y=690)
        _21_giveupcardbt.place(x=360,y=690)
    else: #其他人的回合
        _21_giveupcardbt.place_forget()
        _21_requestcardbt.place_forget()
    
    for i in range(4):
        if nowplayer==i:
            if (i+4-index)%4==0: #中下
                _21_canvas.create_image(625,730,image=_21_whitehole)
            elif (i+4-index)%4==1: #右
                _21_canvas.create_image(1140,393,image=_21_whitehole)
            elif (i+4-index)%4==2: #中上
                _21_canvas.create_image(621,60,image=_21_whitehole)
            elif (i+4-index)%4==3: #左
                _21_canvas.create_image(110,393,image=_21_whitehole)
        else:
            if (i+4-index)%4==0: #中下
                _21_canvas.create_image(625,730,image=_21_whiteholerecover)
            elif (i+4-index)%4==1: #右
                _21_canvas.create_image(1140,393,image=_21_whiteholerecover)
            elif (i+4-index)%4==2: #中上
                _21_canvas.create_image(621,60,image=_21_whiteholerecover)
            elif (i+4-index)%4==3: #左
                _21_canvas.create_image(110,393,image=_21_whiteholerecover)
    draw21character()
def draw21character(): 
    global _21_canvas,player,roomcolor,roommember,_21_crown
    index=-1
    for i in range(4):
        if roommember[i]==username:
            index=i
            break
    for i in range(4):
        if len(player)<=i:
            tmp=tk.PhotoImage()
            player.append(tmp)
        if roomcolor[(index+i)%4]=="empty":
            player[i]=tk.PhotoImage(file="image/empty.png")
        elif roomcolor[(index+i)%len(roommember)]=="gray":
            player[i]=tk.PhotoImage(file="image/character_gray_small.png")
        elif roomcolor[(index+i)%len(roommember)]=="blue":
            player[i]=tk.PhotoImage(file="image/character_blue_small.png")
        elif roomcolor[(index+i)%len(roommember)]=="red":
            player[i]=tk.PhotoImage(file="image/character_red_small.png")
        elif roomcolor[(index+i)%len(roommember)]=="green":
            player[i]=tk.PhotoImage(file="image/character_green_small.png")
        elif roomcolor[(index+i)%len(roommember)]=="purple":
            player[i]=tk.PhotoImage(file="image/character_purple_small.png")
        elif roomcolor[(index+i)%len(roommember)]=="yellow":
            player[i]=tk.PhotoImage(file="image/character_yellow_small.png")
        if i==0:
            _21_canvas.create_image(630,720,image=player[i])
        elif i==1:
            _21_canvas.create_image(1140,390,image=player[i])
        elif i==2:
            _21_canvas.create_image(620,50,image=player[i])
        elif i==3:
            _21_canvas.create_image(110,390,image=player[i])
        if (index+i)%4==0:
            _21_crown=tk.PhotoImage(file="image/crown.png")
            if i==0:
                _21_canvas.create_image(630,670,image=_21_crown)
            elif i==1:
                _21_canvas.create_image(1140,340,image=_21_crown)
            elif i==2:
                _21_canvas.create_image(620,0,image=_21_crown)
            elif i==3:
                _21_canvas.create_image(110,340,image=_21_crown)
def listenthread():
    while True:
        x=clientsocket.recv(200).decode() 
        messagequeue.append(x)

def whichcard(wcard,i,j): 
    global _21_card
    if(wcard=="1"):
        _21_card[i][j]=tk.PhotoImage(file="image/h1.png")
        return "image/h1.png"
    elif(wcard=="2"):
        _21_card[i][j]=tk.PhotoImage(file="image/h2.png")
        return "image/h2.png"
    elif(wcard=="3"):
        _21_card[i][j]=tk.PhotoImage(file="image/h3.png")
        return "image/h3.png"
    elif(wcard=="4"):
        _21_card[i][j]=tk.PhotoImage(file="image/h4.png")
        return "image/h4.png"
    elif(wcard=="5"):
        _21_card[i][j]=tk.PhotoImage(file="image/h5.png")
        return "image/h5.png"
    elif(wcard=="6"):
        _21_card[i][j]=tk.PhotoImage(file="image/h6.png")
        return "image/h6.png"
    elif(wcard=="7"):
        _21_card[i][j]=tk.PhotoImage(file="image/h7.png")
        return "image/h7.png"
    elif(wcard=="8"):
        _21_card[i][j]=tk.PhotoImage(file="image/h8.png")
        return "image/h8.png"
    elif(wcard=="9"):
        _21_card[i][j]=tk.PhotoImage(file="image/h9.png")
        return "image/h9.png"
    elif(wcard=="10"):
        _21_card[i][j]=tk.PhotoImage(file="image/h10.png")
        return "image/h10.png"
    elif(wcard=="11"):
        _21_card[i][j]=tk.PhotoImage(file="image/h11.png")
        return "image/h11.png"
    elif(wcard=="12"):
        _21_card[i][j]=tk.PhotoImage(file="image/h12.png")
        return "image/h12.png"
    elif(wcard=="13"):
        _21_card[i][j]=tk.PhotoImage(file="image/h13.png")
        return "image/h13.png"
    elif(wcard=="14"):
        _21_card[i][j]=tk.PhotoImage(file="image/i1.png")
        return "image/i1.png"
    elif(wcard=="15"):
        _21_card[i][j]=tk.PhotoImage(file="image/i2.png")
        return "image/i2.png"
    elif(wcard=="16"):
        _21_card[i][j]=tk.PhotoImage(file="image/i3.png")
        return "image/i3.png"
    elif(wcard=="17"):
        _21_card[i][j]=tk.PhotoImage(file="image/i4.png")
        return "image/i4.png"
    elif(wcard=="18"):
        _21_card[i][j]=tk.PhotoImage(file="image/i5.png")
        return "image/i5.png"
    elif(wcard=="19"):
        _21_card[i][j]=tk.PhotoImage(file="image/i6.png")
        return "image/i6.png"
    elif(wcard=="20"):
        _21_card[i][j]=tk.PhotoImage(file="image/i7.png")
        return "image/i7.png"
    elif(wcard=="21"):
        _21_card[i][j]=tk.PhotoImage(file="image/i8.png")
        return "image/i8.png"
    elif(wcard=="22"):
        _21_card[i][j]=tk.PhotoImage(file="image/i9.png")
        return "image/i9.png"
    elif(wcard=="23"):
        _21_card[i][j]=tk.PhotoImage(file="image/i10.png")
        return "image/i10.png"
    elif(wcard=="24"):
        _21_card[i][j]=tk.PhotoImage(file="image/i11.png")
        return "image/i11.png"
    elif(wcard=="25"):
        _21_card[i][j]=tk.PhotoImage(file="image/i12.png")
        return "image/i12.png"
    elif(wcard=="26"):
        _21_card[i][j]=tk.PhotoImage(file="image/i13.png")
        return "image/i13.png"
    elif(wcard=="27"):
        _21_card[i][j]=tk.PhotoImage(file="image/d1.png")
        return "image/d1.png"
    elif(wcard=="28"):
        _21_card[i][j]=tk.PhotoImage(file="image/d2.png")
        return "image/d2.png"
    elif(wcard=="29"):
        _21_card[i][j]=tk.PhotoImage(file="image/d3.png")
        return "image/d3.png"
    elif(wcard=="30"):
        _21_card[i][j]=tk.PhotoImage(file="image/d4.png")
        return "image/d4.png"
    elif(wcard=="31"):
        _21_card[i][j]=tk.PhotoImage(file="image/d5.png")
        return "image/d5.png"
    elif(wcard=="32"):
        _21_card[i][j]=tk.PhotoImage(file="image/d6.png")
        return "image/d6.png"
    elif(wcard=="33"):
        _21_card[i][j]=tk.PhotoImage(file="image/d7.png")
        return "image/d7.png"
    elif(wcard=="34"):
        _21_card[i][j]=tk.PhotoImage(file="image/d8.png")
        return "image/d8.png"
    elif(wcard=="35"):
        _21_card[i][j]=tk.PhotoImage(file="image/d9.png")
        return "image/d9.png"
    elif(wcard=="36"):
        _21_card[i][j]=tk.PhotoImage(file="image/d10.png")
        return "image/d10.png"
    elif(wcard=="37"):
        _21_card[i][j]=tk.PhotoImage(file="image/d11.png")
        return "image/d11.png"
    elif(wcard=="38"):
        _21_card[i][j]=tk.PhotoImage(file="image/d12.png")
        return "image/d12.png"
    elif(wcard=="39"):
        _21_card[i][j]=tk.PhotoImage(file="image/d13.png")
        return "image/d13.png"
    elif(wcard=="40"):
        _21_card[i][j]=tk.PhotoImage(file="image/m1.png")
        return "image/m1.png"
    elif(wcard=="41"):
        _21_card[i][j]=tk.PhotoImage(file="image/m2.png")
        return "image/m2.png"
    elif(wcard=="42"):
        _21_card[i][j]=tk.PhotoImage(file="image/m3.png")
        return "image/m3.png"
    elif(wcard=="43"):
        _21_card[i][j]=tk.PhotoImage(file="image/m4.png")
        return "image/m4.png"
    elif(wcard=="44"):
        _21_card[i][j]=tk.PhotoImage(file="image/m5.png")
        return "image/m5.png"
    elif(wcard=="45"):
        _21_card[i][j]=tk.PhotoImage(file="image/m6.png")
        return "image/m6.png"
    elif(wcard=="46"):
        _21_card[i][j]=tk.PhotoImage(file="image/m7.png")
        return "image/m7.png"
    elif(wcard=="47"):
        _21_card[i][j]=tk.PhotoImage(file="image/m8.png")
        return "image/m8.png"
    elif(wcard=="48"):
        _21_card[i][j]=tk.PhotoImage(file="image/m9.png")
        return "image/m9.png"
    elif(wcard=="49"):
        _21_card[i][j]=tk.PhotoImage(file="image/m10.png")
        return "image/m10.png"
    elif(wcard=="50"):
        _21_card[i][j]=tk.PhotoImage(file="image/m11.png")
        return "image/m11.png"
    elif(wcard=="51"):
        _21_card[i][j]=tk.PhotoImage(file="image/m12.png")
        return "image/m12.png"
    elif(wcard=="52"):
        _21_card[i][j]=tk.PhotoImage(file="image/m13.png")
        return "image/m13.png"
def whichcardl(wcard,i,j): 
    global _21_card
    if(wcard=="1"):
        _21_card[i][j]=tk.PhotoImage(file="image/h1l.png")
    elif(wcard=="2"):
        _21_card[i][j]=tk.PhotoImage(file="image/h2l.png")
    elif(wcard=="3"):
        _21_card[i][j]=tk.PhotoImage(file="image/h3l.png")
    elif(wcard=="4"):
        _21_card[i][j]=tk.PhotoImage(file="image/h4l.png")
    elif(wcard=="5"):
        _21_card[i][j]=tk.PhotoImage(file="image/h5l.png")
    elif(wcard=="6"):
        _21_card[i][j]=tk.PhotoImage(file="image/h6l.png")
    elif(wcard=="7"):
        _21_card[i][j]=tk.PhotoImage(file="image/h7l.png")
    elif(wcard=="8"):
        _21_card[i][j]=tk.PhotoImage(file="image/h8l.png")
    elif(wcard=="9"):
        _21_card[i][j]=tk.PhotoImage(file="image/h9l.png")
    elif(wcard=="10"):
        _21_card[i][j]=tk.PhotoImage(file="image/h10l.png")
    elif(wcard=="11"):
        _21_card[i][j]=tk.PhotoImage(file="image/h11l.png")
    elif(wcard=="12"):
        _21_card[i][j]=tk.PhotoImage(file="image/h12l.png")
    elif(wcard=="13"):
        _21_card[i][j]=tk.PhotoImage(file="image/h13l.png")
    elif(wcard=="14"):
        _21_card[i][j]=tk.PhotoImage(file="image/i1l.png")
    elif(wcard=="15"):
        _21_card[i][j]=tk.PhotoImage(file="image/i2l.png")
    elif(wcard=="16"):
        _21_card[i][j]=tk.PhotoImage(file="image/i3l.png")
    elif(wcard=="17"):
        _21_card[i][j]=tk.PhotoImage(file="image/i4l.png")
    elif(wcard=="18"):
        _21_card[i][j]=tk.PhotoImage(file="image/i5l.png")
    elif(wcard=="19"):
        _21_card[i][j]=tk.PhotoImage(file="image/i6l.png")
    elif(wcard=="20"):
        _21_card[i][j]=tk.PhotoImage(file="image/i7l.png")
    elif(wcard=="21"):
        _21_card[i][j]=tk.PhotoImage(file="image/i8l.png")
    elif(wcard=="22"):
        _21_card[i][j]=tk.PhotoImage(file="image/i9l.png")
    elif(wcard=="23"):
        _21_card[i][j]=tk.PhotoImage(file="image/i10l.png")
    elif(wcard=="24"):
        _21_card[i][j]=tk.PhotoImage(file="image/i11l.png")
    elif(wcard=="25"):
        _21_card[i][j]=tk.PhotoImage(file="image/i12l.png")
    elif(wcard=="26"):
        _21_card[i][j]=tk.PhotoImage(file="image/i13l.png")
    elif(wcard=="27"):
        _21_card[i][j]=tk.PhotoImage(file="image/d1r.png")
    elif(wcard=="28"):
        _21_card[i][j]=tk.PhotoImage(file="image/d2r.png")
    elif(wcard=="29"):
        _21_card[i][j]=tk.PhotoImage(file="image/d3r.png")
    elif(wcard=="30"):
        _21_card[i][j]=tk.PhotoImage(file="image/d4r.png")
    elif(wcard=="31"):
        _21_card[i][j]=tk.PhotoImage(file="image/d5r.png")
    elif(wcard=="32"):
        _21_card[i][j]=tk.PhotoImage(file="image/d6r.png")
    elif(wcard=="33"):
        _21_card[i][j]=tk.PhotoImage(file="image/d7r.png")
    elif(wcard=="34"):
        _21_card[i][j]=tk.PhotoImage(file="image/d8r.png")
    elif(wcard=="35"):
        _21_card[i][j]=tk.PhotoImage(file="image/d9r.png")
    elif(wcard=="36"):
        _21_card[i][j]=tk.PhotoImage(file="image/d10r.png")
    elif(wcard=="37"):
        _21_card[i][j]=tk.PhotoImage(file="image/d11l.png")
    elif(wcard=="38"):
        _21_card[i][j]=tk.PhotoImage(file="image/d12l.png")
    elif(wcard=="39"):
        _21_card[i][j]=tk.PhotoImage(file="image/d13l.png")
    elif(wcard=="40"):
        _21_card[i][j]=tk.PhotoImage(file="image/m1l.png")
    elif(wcard=="41"):
        _21_card[i][j]=tk.PhotoImage(file="image/m2l.png")
    elif(wcard=="42"):
        _21_card[i][j]=tk.PhotoImage(file="image/m3l.png")
    elif(wcard=="43"):
        _21_card[i][j]=tk.PhotoImage(file="image/m4l.png")
    elif(wcard=="44"):
        _21_card[i][j]=tk.PhotoImage(file="image/m5l.png")
    elif(wcard=="45"):
        _21_card[i][j]=tk.PhotoImage(file="image/m6l.png")
    elif(wcard=="46"):
        _21_card[i][j]=tk.PhotoImage(file="image/m7l.png")
    elif(wcard=="47"):
        _21_card[i][j]=tk.PhotoImage(file="image/m8l.png")
    elif(wcard=="48"):
        _21_card[i][j]=tk.PhotoImage(file="image/m9l.png")
    elif(wcard=="49"):
        _21_card[i][j]=tk.PhotoImage(file="image/m10l.png")
    elif(wcard=="50"):
        _21_card[i][j]=tk.PhotoImage(file="image/m11l.png")
    elif(wcard=="51"):
        _21_card[i][j]=tk.PhotoImage(file="image/m12l.png")
    elif(wcard=="52"):
        _21_card[i][j]=tk.PhotoImage(file="image/m13l.png")

def whichcardt(wcard,i,j): 
    global _21_card
    if(wcard=="1"):
        _21_card[i][j]=tk.PhotoImage(file="image/h1t.png")
    elif(wcard=="2"):
        _21_card[i][j]=tk.PhotoImage(file="image/h2t.png")
    elif(wcard=="3"):
        _21_card[i][j]=tk.PhotoImage(file="image/h3t.png")
    elif(wcard=="4"):
        _21_card[i][j]=tk.PhotoImage(file="image/h4t.png")
    elif(wcard=="5"):
        _21_card[i][j]=tk.PhotoImage(file="image/h5t.png")
    elif(wcard=="6"):
        _21_card[i][j]=tk.PhotoImage(file="image/h6t.png")
    elif(wcard=="7"):
        _21_card[i][j]=tk.PhotoImage(file="image/h7t.png")
    elif(wcard=="8"):
        _21_card[i][j]=tk.PhotoImage(file="image/h8t.png")
    elif(wcard=="9"):
        _21_card[i][j]=tk.PhotoImage(file="image/h9t.png")
    elif(wcard=="10"):
        _21_card[i][j]=tk.PhotoImage(file="image/h10t.png")
    elif(wcard=="11"):
        _21_card[i][j]=tk.PhotoImage(file="image/h11t.png")
    elif(wcard=="12"):
        _21_card[i][j]=tk.PhotoImage(file="image/h12t.png")
    elif(wcard=="13"):
        _21_card[i][j]=tk.PhotoImage(file="image/h13t.png")
    elif(wcard=="14"):
        _21_card[i][j]=tk.PhotoImage(file="image/i1t.png")
    elif(wcard=="15"):
        _21_card[i][j]=tk.PhotoImage(file="image/i2t.png")
    elif(wcard=="16"):
        _21_card[i][j]=tk.PhotoImage(file="image/i3t.png")
    elif(wcard=="17"):
        _21_card[i][j]=tk.PhotoImage(file="image/i4t.png")
    elif(wcard=="18"):
        _21_card[i][j]=tk.PhotoImage(file="image/i5t.png")
    elif(wcard=="19"):
        _21_card[i][j]=tk.PhotoImage(file="image/i6t.png")
    elif(wcard=="20"):
        _21_card[i][j]=tk.PhotoImage(file="image/i7t.png")
    elif(wcard=="21"):
        _21_card[i][j]=tk.PhotoImage(file="image/i8t.png")
    elif(wcard=="22"):
        _21_card[i][j]=tk.PhotoImage(file="image/i9t.png")
    elif(wcard=="23"):
        _21_card[i][j]=tk.PhotoImage(file="image/i10t.png")
    elif(wcard=="24"):
        _21_card[i][j]=tk.PhotoImage(file="image/i11t.png")
    elif(wcard=="25"):
        _21_card[i][j]=tk.PhotoImage(file="image/i12t.png")
    elif(wcard=="26"):
        _21_card[i][j]=tk.PhotoImage(file="image/i13t.png")
    elif(wcard=="27"):
        _21_card[i][j]=tk.PhotoImage(file="image/d1.png")
    elif(wcard=="28"):
        _21_card[i][j]=tk.PhotoImage(file="image/d2.png")
    elif(wcard=="29"):
        _21_card[i][j]=tk.PhotoImage(file="image/d3.png")
    elif(wcard=="30"):
        _21_card[i][j]=tk.PhotoImage(file="image/d4.png")
    elif(wcard=="31"):
        _21_card[i][j]=tk.PhotoImage(file="image/d5.png")
    elif(wcard=="32"):
        _21_card[i][j]=tk.PhotoImage(file="image/d6.png")
    elif(wcard=="33"):
        _21_card[i][j]=tk.PhotoImage(file="image/d7.png")
    elif(wcard=="34"):
        _21_card[i][j]=tk.PhotoImage(file="image/d8.png")
    elif(wcard=="35"):
        _21_card[i][j]=tk.PhotoImage(file="image/d9.png")
    elif(wcard=="36"):
        _21_card[i][j]=tk.PhotoImage(file="image/d10.png")
    elif(wcard=="37"):
        _21_card[i][j]=tk.PhotoImage(file="image/d11t.png")
    elif(wcard=="38"):
        _21_card[i][j]=tk.PhotoImage(file="image/d12t.png")
    elif(wcard=="39"):
        _21_card[i][j]=tk.PhotoImage(file="image/d13t.png")
    elif(wcard=="40"):
        _21_card[i][j]=tk.PhotoImage(file="image/m1t.png")
    elif(wcard=="41"):
        _21_card[i][j]=tk.PhotoImage(file="image/m2t.png")
    elif(wcard=="42"):
        _21_card[i][j]=tk.PhotoImage(file="image/m3t.png")
    elif(wcard=="43"):
        _21_card[i][j]=tk.PhotoImage(file="image/m4t.png")
    elif(wcard=="44"):
        _21_card[i][j]=tk.PhotoImage(file="image/m5t.png")
    elif(wcard=="45"):
        _21_card[i][j]=tk.PhotoImage(file="image/m6t.png")
    elif(wcard=="46"):
        _21_card[i][j]=tk.PhotoImage(file="image/m7t.png")
    elif(wcard=="47"):
        _21_card[i][j]=tk.PhotoImage(file="image/m8t.png")
    elif(wcard=="48"):
        _21_card[i][j]=tk.PhotoImage(file="image/m9t.png")
    elif(wcard=="49"):
        _21_card[i][j]=tk.PhotoImage(file="image/m10t.png")
    elif(wcard=="50"):
        _21_card[i][j]=tk.PhotoImage(file="image/m11t.png")
    elif(wcard=="51"):
        _21_card[i][j]=tk.PhotoImage(file="image/m12t.png")
    elif(wcard=="52"):
        _21_card[i][j]=tk.PhotoImage(file="image/m13t.png")
def whichcardr(wcard,i,j): 
    global _21_card
    if(wcard=="1"):
        _21_card[i][j]=tk.PhotoImage(file="image/h1r.png")
    elif(wcard=="2"):
        _21_card[i][j]=tk.PhotoImage(file="image/h2r.png")
    elif(wcard=="3"):
        _21_card[i][j]=tk.PhotoImage(file="image/h3r.png")
    elif(wcard=="4"):
        _21_card[i][j]=tk.PhotoImage(file="image/h4r.png")
    elif(wcard=="5"):
        _21_card[i][j]=tk.PhotoImage(file="image/h5r.png")
    elif(wcard=="6"):
        _21_card[i][j]=tk.PhotoImage(file="image/h6r.png")
    elif(wcard=="7"):
        _21_card[i][j]=tk.PhotoImage(file="image/h7r.png")
    elif(wcard=="8"):
        _21_card[i][j]=tk.PhotoImage(file="image/h8r.png")
    elif(wcard=="9"):
        _21_card[i][j]=tk.PhotoImage(file="image/h9r.png")
    elif(wcard=="10"):
        _21_card[i][j]=tk.PhotoImage(file="image/h10r.png")
    elif(wcard=="11"):
        _21_card[i][j]=tk.PhotoImage(file="image/h11r.png")
    elif(wcard=="12"):
        _21_card[i][j]=tk.PhotoImage(file="image/h12r.png")
    elif(wcard=="13"):
        _21_card[i][j]=tk.PhotoImage(file="image/h13r.png")
    elif(wcard=="14"):
        _21_card[i][j]=tk.PhotoImage(file="image/i1r.png")
    elif(wcard=="15"):
        _21_card[i][j]=tk.PhotoImage(file="image/i2r.png")
    elif(wcard=="16"):
        _21_card[i][j]=tk.PhotoImage(file="image/i3r.png")
    elif(wcard=="17"):
        _21_card[i][j]=tk.PhotoImage(file="image/i4r.png")
    elif(wcard=="18"):
        _21_card[i][j]=tk.PhotoImage(file="image/i5r.png")
    elif(wcard=="19"):
        _21_card[i][j]=tk.PhotoImage(file="image/i6r.png")
    elif(wcard=="20"):
        _21_card[i][j]=tk.PhotoImage(file="image/i7r.png")
    elif(wcard=="21"):
        _21_card[i][j]=tk.PhotoImage(file="image/i8r.png")
    elif(wcard=="22"):
        _21_card[i][j]=tk.PhotoImage(file="image/i9r.png")
    elif(wcard=="23"):
        _21_card[i][j]=tk.PhotoImage(file="image/i10r.png")
    elif(wcard=="24"):
        _21_card[i][j]=tk.PhotoImage(file="image/i11r.png")
    elif(wcard=="25"):
        _21_card[i][j]=tk.PhotoImage(file="image/i12r.png")
    elif(wcard=="26"):
        _21_card[i][j]=tk.PhotoImage(file="image/i13r.png")
    elif(wcard=="27"):
        _21_card[i][j]=tk.PhotoImage(file="image/d1r.png")
    elif(wcard=="28"):
        _21_card[i][j]=tk.PhotoImage(file="image/d2r.png")
    elif(wcard=="29"):
        _21_card[i][j]=tk.PhotoImage(file="image/d3r.png")
    elif(wcard=="30"):
        _21_card[i][j]=tk.PhotoImage(file="image/d4r.png")
    elif(wcard=="31"):
        _21_card[i][j]=tk.PhotoImage(file="image/d5r.png")
    elif(wcard=="32"):
        _21_card[i][j]=tk.PhotoImage(file="image/d6r.png")
    elif(wcard=="33"):
        _21_card[i][j]=tk.PhotoImage(file="image/d7r.png")
    elif(wcard=="34"):
        _21_card[i][j]=tk.PhotoImage(file="image/d8r.png")
    elif(wcard=="35"):
        _21_card[i][j]=tk.PhotoImage(file="image/d9r.png")
    elif(wcard=="36"):
        _21_card[i][j]=tk.PhotoImage(file="image/d10r.png")
    elif(wcard=="37"):
        _21_card[i][j]=tk.PhotoImage(file="image/d11r.png")
    elif(wcard=="38"):
        _21_card[i][j]=tk.PhotoImage(file="image/d12r.png")
    elif(wcard=="39"):
        _21_card[i][j]=tk.PhotoImage(file="image/d13r.png")
    elif(wcard=="40"):
        _21_card[i][j]=tk.PhotoImage(file="image/m1r.png")
    elif(wcard=="41"):
        _21_card[i][j]=tk.PhotoImage(file="image/m2r.png")
    elif(wcard=="42"):
        _21_card[i][j]=tk.PhotoImage(file="image/m3r.png")
    elif(wcard=="43"):
        _21_card[i][j]=tk.PhotoImage(file="image/m4r.png")
    elif(wcard=="44"):
        _21_card[i][j]=tk.PhotoImage(file="image/m5r.png")
    elif(wcard=="45"):
        _21_card[i][j]=tk.PhotoImage(file="image/m6r.png")
    elif(wcard=="46"):
        _21_card[i][j]=tk.PhotoImage(file="image/m7r.png")
    elif(wcard=="47"):
        _21_card[i][j]=tk.PhotoImage(file="image/m8r.png")
    elif(wcard=="48"):
        _21_card[i][j]=tk.PhotoImage(file="image/m9r.png")
    elif(wcard=="49"):
        _21_card[i][j]=tk.PhotoImage(file="image/m10r.png")
    elif(wcard=="50"):
        _21_card[i][j]=tk.PhotoImage(file="image/m11r.png")
    elif(wcard=="51"):
        _21_card[i][j]=tk.PhotoImage(file="image/m12r.png")
    elif(wcard=="52"):
        _21_card[i][j]=tk.PhotoImage(file="image/m13r.png")
#註冊
def regist():
    global registname,registpass,registerror,track,registerrorlabel
    if registname.get()=="":
        track = pygame.mixer.music.load("sound/fail.mp3")
        pygame.mixer.music.play()
        registerror.set("username cannt be empty!!")
        registerrorlabel.place(x=300,y=420)
    elif registpass.get()=="":
        track = pygame.mixer.music.load("sound/fail.mp3")
        pygame.mixer.music.play()
        registerror.set("password cannt be empty!!")
        registerrorlabel.place(x=300,y=420)
    else:
        msg="regist "+registname.get()+" "+registpass.get()
        clientsocket.send(msg.encode())

#登入
def enter():
    global entername,enterpass,entererror,username,entererrorlabel
    msg="enter "+entername.get()+" "+enterpass.get()
    if entername.get()=="":
        track = pygame.mixer.music.load("sound/fail.mp3")
        pygame.mixer.music.play()
        entererror.set("username cannt be empty!")
        entererrorlabel.place(x=600,y=415)
    elif enterpass.get()=="":
        track = pygame.mixer.music.load("sound/fail.mp3")
        pygame.mixer.music.play()
        entererror.set("password cannt be empty!")
        entererrorlabel.place(x=600,y=415)
    # print (f"entername:{entername.get()} enterpass:{enterpass.get()}")
    else:
        username=entername.get()
        clientsocket.send(msg.encode())

#從註冊畫面回到登入畫面
def registback():
    delregistlayout()
    setuserentrylayout()

#從創建角色畫面回到登入畫面
def createback():
    track = pygame.mixer.music.load("sound/back.mp3")
    pygame.mixer.music.play()
    delcreatecharacterlayout()
    setuserentrylayout()

#從創建角色面跳轉到大廳
def createtolobby():
    global finalcolor,username,createflag
    msg="createsuccess "+username+" "+finalcolor
    clientsocket.send(msg.encode())
    track = pygame.mixer.music.load("sound/enterlobby.mp3")
    pygame.mixer.music.play()
    createflag=True
#創建角色顏色
def setgray():
    global create_character,create_canvas,create_circlephoto,finalcolor
    track = pygame.mixer.music.load("sound/selectcharacter.mp3")
    pygame.mixer.music.play()
    create_circlephoto=tk.PhotoImage(file="image/curcle_gray.png")
    create_canvas.create_image(450,700,image=create_circlephoto)
    create_character=tk.PhotoImage(file="image/character_gray.png")
    create_canvas.create_image(450,400,image=create_character)
    finalcolor="gray"
def setpurple():
    global create_character,create_canvas,create_circlephoto,finalcolor
    track = pygame.mixer.music.load("sound/selectcharacter.mp3")
    pygame.mixer.music.play()
    create_circlephoto=tk.PhotoImage(file="image/curcle_purple.png")
    create_canvas.create_image(450,700,image=create_circlephoto)
    create_character=tk.PhotoImage(file="image/character_purple.png")
    create_canvas.create_image(450,400,image=create_character)
    finalcolor="purple"
def setyellow():
    global create_character,create_canvas,create_circlephoto,finalcolor
    track = pygame.mixer.music.load("sound/selectcharacter.mp3")
    pygame.mixer.music.play()
    create_circlephoto=tk.PhotoImage(file="image/curcle_yellow.png")
    create_canvas.create_image(450,700,image=create_circlephoto)
    create_character=tk.PhotoImage(file="image/character_yellow.png")
    create_canvas.create_image(450,400,image=create_character)
    finalcolor="yellow"
def setgreen():
    global create_character,create_canvas,create_circlephoto,finalcolor
    track = pygame.mixer.music.load("sound/selectcharacter.mp3")
    pygame.mixer.music.play()
    create_circlephoto=tk.PhotoImage(file="image/curcle_green.png")
    create_canvas.create_image(450,700,image=create_circlephoto)
    create_character=tk.PhotoImage(file="image/character_green.png")
    create_canvas.create_image(450,400,image=create_character)
    finalcolor="green"
def setblue():
    global create_character,create_canvas,create_circlephoto,finalcolor
    track = pygame.mixer.music.load("sound/selectcharacter.mp3")
    pygame.mixer.music.play()
    create_circlephoto=tk.PhotoImage(file="image/curcle_blue.png")
    create_canvas.create_image(450,700,image=create_circlephoto)
    create_character=tk.PhotoImage(file="image/character_blue.png")
    create_canvas.create_image(450,400,image=create_character)
    finalcolor="blue"
def setred():
    global create_character,create_canvas,create_circlephoto,finalcolor
    track = pygame.mixer.music.load("sound/selectcharacter.mp3")
    pygame.mixer.music.play()
    create_circlephoto=tk.PhotoImage(file="image/curcle_red.png")
    create_canvas.create_image(450,700,image=create_circlephoto)
    create_character=tk.PhotoImage(file="image/character_red.png")
    create_canvas.create_image(450,400,image=create_character)
    finalcolor="red"
#創建角色介面
def setcreatecharacterlayout():
    # global create_circlelabel,create_labellabel,create_characterlabel,create_colorselectbglabel
    global create_circlephoto,create_label,create_character,create_colorselectbg,create_canvas,create_backbutton,create_decidebutton,create_bg,create_colorselect
    global create_bluecolor,create_graycolor,create_greencolor,create_purplecolor,create_redcolor,create_yellowcolor
    create_canvas=tk.Canvas(width=1300,height=800)
    create_canvas.place(x=0,y=0)
    create_bg=tk.PhotoImage(file="image/create_bg.png")
    create_canvas.create_image(650,400,image=create_bg)
    create_circlephoto=tk.PhotoImage(file="image/curcle_blue.png")
    create_canvas.create_image(450,700,image=create_circlephoto)
    create_label=tk.PhotoImage(file="image/create_label.png")
    create_canvas.create_image(125,75,image=create_label)
    create_character=tk.PhotoImage(file="image/character_blue.png")
    create_canvas.create_image(450,400,image=create_character)
    create_colorselectbg=tk.PhotoImage(file="image/colorselectbg.png")
    create_canvas.create_image(1000,350,image=create_colorselectbg)
    create_colorselect=tk.PhotoImage(file="image/colorselect.png")
    create_canvas.create_image(1000,120,image=create_colorselect)
    create_decidebutton=tk.Button(window, text="確認",width=15,height=4,command= createtolobby)
    create_decidebutton.place(x=1010,y=700)
    create_backbutton=tk.Button(window, text="返回",width=15,height=4,command = createback)
    create_backbutton.place(x=870,y=700)
    create_graycolor=tk.Button(window,bg="gray",width=8,height=4,command=setgray)
    create_graycolor.place(x=915,y=200)
    create_bluecolor=tk.Button(window,bg="blue",width=8,height=4,command=setblue)
    create_bluecolor.place(x=1020,y=200)
    create_redcolor=tk.Button(window,bg="red",width=8,height=4,command=setred)
    create_redcolor.place(x=915,y=325)
    create_yellowcolor=tk.Button(window,bg="yellow",width=8,height=4,command=setyellow)
    create_yellowcolor.place(x=1020,y=325)
    create_greencolor=tk.Button(window,bg="green",width=8,height=4,command=setgreen)
    create_greencolor.place(x=915,y=450)
    create_purplecolor=tk.Button(window,bg="purple",width=8,height=4,command=setpurple)
    create_purplecolor.place(x=1020,y=450)
    # create_circlelabel=tk.Label(window,image=create_circlephoto)
    # create_circlelabel.place(x=-250,y=300)

    # create_labellabel=tk.Label(window,image=create_label)
    # create_labellabel.place(x=0,y=0)

    # create_characterlabel=tk.Label(window,image=create_character)
    # create_characterlabel.place(x=105,y=200)
    
    # create_colorselectbglabel=tk.Label(window,image=create_colorselectbg)
    # create_colorselectbglabel.place(x=250,y=100)
def delcreatecharacterlayout():
    global create_bluecolor,create_graycolor,create_greencolor,create_purplecolor,create_redcolor,create_yellowcolor,create_canvas,create_backbutton,create_decidebutton
    create_canvas.place_forget()
    create_redcolor.place_forget()
    create_yellowcolor.place_forget()
    create_graycolor.place_forget()
    create_bluecolor.place_forget()
    create_greencolor.place_forget()
    create_purplecolor.place_forget()
    create_backbutton.place_forget()
    create_decidebutton.place_forget()
#設置註冊畫面
def setregistlayout():
    global registbackbutton,registbutton,registnameentry,registpassentry,registname,registpass,registnamebg,registpassbg,registerrorlabel,registerror,registbgimg,registcanvas
    registcanvas=tk.Canvas(width=1300,height=800)
    registcanvas.place(x=0,y=0)
    registbgimg=tk.PhotoImage(file="image/registbg.png")
    registcanvas.create_image(650,400,image=registbgimg)
    
    registnamebg=tk.PhotoImage(file="image/registnamebg.png")
    registcanvas.create_image(100,300,image=registnamebg)
    registpassbg=tk.PhotoImage(file="image/registpassbg.png")
    registcanvas.create_image(100,380,image=registpassbg)

    registnameentry=tk.Entry(window,relief="groove",selectborderwidth=4,textvariable=registname)
    registnameentry.place(x=180,y=290)
    registpassentry=tk.Entry(window,relief="groove",selectborderwidth=4,textvariable=registpass)
    registpassentry.place(x=180,y=370)

    registbackbutton=tk.Button(window,text="返回",command = registback)
    registbackbutton.place(x=180,y=420)
    registbutton=tk.Button(window,text="確認",command = regist)
    registbutton.place(x=240,y=420)
    registerrorlabel=tk.Label(window,fg="red",height=1,font=20,bg="black",textvariable=registerror)

    
#delete 註冊畫面
def delregistlayout():
    global registbackbutton,registbutton,registnameentry,registpassentry,registerrorlabel,registname,registpass,registerror,registcanvas
    registcanvas.place_forget()
    registbackbutton.place_forget()
    registbutton.place_forget()
    registnameentry.place_forget()
    registpassentry.place_forget()
    registerrorlabel.place_forget()
    registpass.set("")
    registname.set("")
    registerror.set("")

#進入註冊畫面
def enterregist():
    track = pygame.mixer.music.load("sound/enterlobby.mp3")
    pygame.mixer.music.play()
    deluserentrylayout()
    setregistlayout()

#設置登入畫面
def setuserentrylayout():
    print("test2")
    global usrnameentry,usrnameentrybutton,usrpassentry,usrregistbutton,usrnameimg,usrpassimg,entername,enterpass,entererror,entererrorlabel,entry_canvas,entry_bg
    entry_canvas=tk.Canvas(width=1300,height=800)
    entry_canvas.place(x=0,y=0)
    entry_bg=tk.PhotoImage(file="image/entrybg.png")
    entry_canvas.create_image(650,400,image=entry_bg)
    usrnameimg=tk.PhotoImage(file="image/userimg.png")
    entry_canvas.create_image(460,290,image=usrnameimg)
    usrpassimg=tk.PhotoImage(file="image/passimg.png")
    entry_canvas.create_image(460,370,image=usrpassimg)
    # usrnamelabel=tk.Label(window,text="帳號")
    # usrnamelabel.place(x=480,y=100)
    # usrpasslabel=tk.Label(window,text="密碼")
    # usrpasslabel.place(x=480,y=130)
    usrnameentry=tk.Entry(window,bd=3,width=25,textvariable=entername)
    usrnameentry.place(x=520,y=277,height=30)
    usrpassentry=tk.Entry(window,show='*',bd=3,width=25,textvariable=enterpass)
    usrpassentry.place(x=520,y=357,height=30)
    usrnameentrybutton=tk.Button(window,text="登入",command = enter)
    usrnameentrybutton.place(x=520,y=415)
    usrregistbutton=tk.Button(window,text="註冊",command = enterregist)
    usrregistbutton.place(x=560,y=415)
    # errorbg=tk.PhotoImage(file="image/errorbg.png")
    entererrorlabel=tk.Label(window,fg="orangered",height=1,font=20,bg="DimGray",textvariable=entererror)
    # entererrorlabel.place(x=520,y=445)
    
#delete 登入畫面
def deluserentrylayout():
    global usrnameentry,usrnameentrybutton,usrpassentry,usrregistbutton,entererrorlabel,entername,enterpass,entererror,entry_canvas
    entry_canvas.delete("all")
    entry_canvas.place_forget()
    usrnameentry.place_forget()
    usrpassentry.place_forget()
    usrnameentrybutton.place_forget()
    usrregistbutton.place_forget()
    entererrorlabel.place_forget()
    entername.set("")
    enterpass.set("")
    entererror.set("")

#delete 21畫面
def del21():
    global _21_canvas,_21_giveupcardbt,_21_requestcardbt,_21_return,_21_return2,_21_cardsenderinfo,_21_playerinfo,_21_moneyinfo,_21_talkbt,_21_sendtalkbt,_21_invitelistbt
    _21_canvas.delete("all")
    _21_canvas.place_forget()
    _21_invitelistbt.place_forget()
    _21_sendtalkbt.place_forget()
    _21_giveupcardbt.place_forget()
    _21_return.place_forget()
    _21_requestcardbt.place_forget()
    _21_cardsenderinfo.place_forget()
    _21_talkbt.place_forget()
    for i in range(4):
        _21_return2.place_forget()
        _21_playerinfo[i].place_forget()
        _21_moneyinfo[i].place_forget()
        _21_talkbt.place_forget()
    deltalklistbox()
    dellistbox()

def requestcard():
    clientsocket.send("requestcard".encode())
def giveupcard():
    clientsocket.send("giveupcard".encode())
def returntolobby():
    track = pygame.mixer.music.load("sound/back.mp3")
    pygame.mixer.music.play()
    del21()
    setlobbylayout()
    clientsocket.send("returntolobby".encode())

def action(event,selectname):
    global _21_secondlist
    if(_21_secondlist.get(_21_secondlist.curselection())=="邀請"):
        msg="inviteuser "+selectname
        clientsocket.send(msg.encode())
    _21_secondlist.place_forget()   

def secondlist(event):
    global _21_secondlist,_21_invitelist
    _21_secondlist=tk.Listbox(window,height=2)
    _21_secondlist.insert("end","邀請")
    _21_secondlist.insert("end","取消")
    selectname=_21_invitelist.get(_21_invitelist.curselection())
    tmpy=int(_21_invitelist.curselection()[0])
    _21_secondlist.bind("<Double-Button-1>",lambda event: action(event,selectname))
    _21_secondlist.place(x=950,y=550+tmpy*20)

def setlistbox(x):
    global _21_invitelist,_21_scrollbar,_21_frame
    _21_frame=tk.Frame(window,relief="flat",highlightcolor="green",highlightbackground="green",highlightthickness=6,width=200,height=200)
    _21_frame.place(x=1100,y=570)
    _21_invitelist=tk.Listbox(_21_frame,font="微軟正黑體 24 bold")       
    _21_scrollbar=tk.Scrollbar(_21_frame,command=_21_invitelist.yview)
    _21_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
    _21_invitelist=tk.Listbox(_21_frame,yscrollcommand=_21_scrollbar.set)
    for i in range(1,len(x)):
        _21_invitelist.insert("end",x[i])
    _21_invitelist.pack()
    _21_invitelist.bind("<Button-3>",secondlist)
def dellistbox():
    global _21_invitelist,_21_scrollbar,_21_frame
    _21_frame.place_forget()

def listboxop():
    global listboxflag
    if listboxflag==True:
        listboxflag=False
        dellistbox()
    else:
        listboxflag=True
        clientsocket.send("invitelist".encode()) #向server 要求邀請列表
def inserttalklist(x):
    global _21_talklist
    _21_talklist.delete("1.0","end")
    for i in range(1,len(x)):
        _21_talklist.insert("end",x[i])
        _21_talklist.insert(tk.INSERT,'\n') 
    _21_talklist.yview_moveto(1)

def settalklistbox(x):
    global _21_talklist,_21_scrollbart,_21_framet,talklistboxflag
    print("set")
    talklistboxflag=True
    _21_framet=tk.Frame(window,relief="ridge",highlightcolor="blue",highlightbackground="blue",highlightthickness=0,width=247,height=200)
    _21_framet.place(x=0,y=565)
    _21_framet.propagate(0)
    _21_talklist=tk.Text(_21_framet,width=10,height=10)       
    _21_scrollbart=tk.Scrollbar(_21_framet,command=_21_talklist.yview)
    _21_scrollbart.pack(side=tk.RIGHT,fill=tk.Y)
    _21_talklist=tk.Text(_21_framet,yscrollcommand=_21_scrollbart.set)
    for i in range(1,len(x)):
        _21_talklist.insert("end",x[i])
        _21_talklist.insert(tk.INSERT,'\n')
    
    _21_talklist.configure(font=("微軟正黑體", 14, "bold"),bg="Azure")
    _21_talklist.yview_moveto(1)
    _21_talklist.pack()

def deltalklistbox():
    global _21_talklist,_21_scrollbart,_21_framet
    print("delete")
    _21_framet.place_forget()

def talkop():
    global talklistboxflag
    if talklistboxflag==True:
        print(f"flag={talklistboxflag}")
        talklistboxflag=False
        deltalklistbox()
        deltalklistbox()
        deltalklistbox()
    else:
        print(f"flag={talklistboxflag}")
        clientsocket.send("talklist".encode()) #向server 要求對話列表
def sendtalk():
    global _21_msg,_21_entry
    if(_21_msg.get()!=""):
        msg="talk "+username+" "+_21_msg.get()
        clientsocket.send(msg.encode())
        _21_entry.delete("0","end")
def set21layout():
    global _21_canvas,_21_bg,_21_waituser,_21_giveupcardbt,_21_requestcardbt,_21_whitehole,_21_whiteholerecover,_21_finish,_21_opencard,_21_return,_21_cardsender,_21_cardsenderinfo
    global _21_invitelistbt,_21_invitephoto,_21_tolobby,_21_talkimg,_21_talkbt,_21_sendtalkbg,_21_sendtalkimg,_21_sendtalkbt,_21_entry,_21_msg,talklistboxflag
    global _21_requestimg,_21_giveupimg
    talklistboxflag=False
    _21_canvas=tk.Canvas(width=1300,height=800)
    _21_canvas.place(x=0,y=0)
    _21_bg=tk.PhotoImage(file="image/ground.png")
    _21_canvas.create_image(650,400,image=_21_bg)
    _21_waituser=tk.PhotoImage(file="image/waiting.png")
    _21_opencard=tk.PhotoImage(file="image/opencard.png")
    _21_finish=tk.PhotoImage(file="image/finish.png")
    _21_canvas.create_image(650,400,image=_21_waituser)
    _21_requestimg=tk.PhotoImage(file="image/needcard.png")
    _21_requestcardbt=tk.Button(window,relief="flat",image=_21_requestimg,bd=0,width=170,height=100,command=requestcard)
    # _21_requestcardbt.place(x=700,y=650)
    _21_giveupimg=tk.PhotoImage(file="image/giveup.png")
    _21_giveupcardbt=tk.Button(window,relief="flat",image=_21_giveupimg,bd=0,width=170,height=105,command=giveupcard)
    # _21_giveupcardbt.place(x=500,y=650)
    _21_tolobby=tk.PhotoImage(file="image/21tolobby.png")
    _21_return=tk.Button(window,relief="flat",image=_21_tolobby,bd=0,width=106,height=95,command=returntolobby)
    _21_return.place(x=1170,y=5)
    _21_whitehole=tk.PhotoImage(file="image/whitehole.png")
    _21_whiteholerecover=tk.PhotoImage(file="image/whiteholerecover.png")
    _21_cardsender=tk.PhotoImage(file="image/cardsender_origin.png")
    _21_canvas.create_image(100,50,image=_21_cardsender)
    _21_cardsenderinfo=tk.Label(window,bg="black",fg="white",font="微軟正黑體 24 bold",text="發牌員")
    _21_cardsenderinfo.place(x=40,y=120)
    _21_invitephoto=tk.PhotoImage(file="image/invitepy.png")
    _21_invitelistbt=tk.Button(window,image=_21_invitephoto,command=listboxop)
    _21_invitelistbt.place(x=1100,y=750)

    _21_talkimg=tk.PhotoImage(file="image/talk.png")
    _21_talkbt=tk.Button(window,relief="flat",image=_21_talkimg,bd=0,width=100,height=60,command=talkop)
    _21_talkbt.place(x=250,y=730)
    _21_sendtalkbg=tk.PhotoImage(file="image/sendtalkbg.png")
    _21_canvas.create_image(120,780,image=_21_sendtalkbg)
    _21_sendtalkimg=tk.PhotoImage(file="image/sendtalk.png")
    _21_sendtalkbt=tk.Button(window,relief="flat",image=_21_sendtalkimg,bd=0,width=61,height=30,command=sendtalk)
    _21_sendtalkbt.place(x=180,y=765)
    _21_entry=tk.Entry(window,width=22,textvariable=_21_msg)
    _21_entry.place(x=5,y=770)


def trygoto21():
    msg="21 "+username
    clientsocket.send(msg.encode())
#進入21點
def goto21():
    track = pygame.mixer.music.load("sound/enterlobby.mp3")
    pygame.mixer.music.play()
    dellobbylayout()
    set21layout()

def tigerrunning():
    global tiger_canvas,tiger_play,tiger_machine
    tmp = []
    for i in range(4):
        tmp.append(tk.PhotoImage())
    track = pygame.mixer.music.load("sound/tigermusic2.mp3")
    pygame.mixer.music.play()
    r1=random.randint(8,10)
    r2=random.randint(18,20)
    r3=random.randint(28,30)
    l1=tk.PhotoImage()
    l2=tk.PhotoImage()
    m1=tk.PhotoImage()
    m2=tk.PhotoImage()
    ri1=tk.PhotoImage()
    ri2=tk.PhotoImage()
    x1=int(0)
    x2=int(0)
    x3=int(0)
    for i in range(31):
        tmp[0]=tk.PhotoImage(file="image/1.png")
        tmp[1]=tk.PhotoImage(file="image/2.png")
        tmp[2]=tk.PhotoImage(file="image/3.png")
        tmp[3]=tk.PhotoImage(file="image/0.png")
        if i%3==0: #left 10  mid 20 right 30
            if i<=r1:
                tiger_canvas.create_image(540,345,image=tmp[0])
                tiger_canvas.create_image(570,345,image=tmp[3])
                l1=tmp[0]
                l2=tmp[3]
                if i==r1:
                    tiger_canvas.create_image(540,345,image=l1)
                    tiger_canvas.create_image(570,345,image=l2)
                    x1=1
            if i<=r2:
                tiger_canvas.create_image(625,345,image=tmp[1])
                tiger_canvas.create_image(655,345,image=tmp[3])
                m1=tmp[1]
                m2=tmp[3]
                if i==r2:
                    tiger_canvas.create_image(625,345,image=m1)
                    tiger_canvas.create_image(655,345,image=m2)
                    x2=2
            if i<=r3:
                tiger_canvas.create_image(720,345,image=tmp[2])
                tiger_canvas.create_image(750,345,image=tmp[3])
                ri1=tmp[2]
                ri2=tmp[3]
                if i==r3:
                    tiger_canvas.create_image(720,345,image=ri1)
                    tiger_canvas.create_image(750,345,image=ri2)
                    x3=3
        elif i%3==1: #left 30  mid 10 right 20
            if i<=r1:
                tiger_canvas.create_image(540,345,image=tmp[2])
                tiger_canvas.create_image(570,345,image=tmp[3])
                l1=tmp[2]
                l2=tmp[3]
                if i==r1:
                    tiger_canvas.create_image(540,345,image=l1)
                    tiger_canvas.create_image(570,345,image=l2)
                    x1=3
            if i<=r2:
                tiger_canvas.create_image(625,345,image=tmp[0])
                tiger_canvas.create_image(655,345,image=tmp[3])
                m1=tmp[0]
                m2=tmp[3]
                if i==r2:
                    tiger_canvas.create_image(625,345,image=m1)
                    tiger_canvas.create_image(655,345,image=m2)
                    x2=1
            if i<=r3:
                tiger_canvas.create_image(720,345,image=tmp[1])
                tiger_canvas.create_image(750,345,image=tmp[3])
                ri1=tmp[1]
                ri2=tmp[3]
                if i==r3:
                    tiger_canvas.create_image(720,345,image=ri1)
                    tiger_canvas.create_image(750,345,image=ri2)
                    x3=2
        elif i%3==2: #left 20  mid 30 right 10
            if i<=r1:
                tiger_canvas.create_image(540,345,image=tmp[1])
                tiger_canvas.create_image(570,345,image=tmp[3])
                l1=tmp[1]
                l2=tmp[3]
                if i==r1:
                    tiger_canvas.create_image(540,345,image=l1)
                    tiger_canvas.create_image(570,345,image=l2)
                    x1=2
            if i<=r2:
                tiger_canvas.create_image(625,345,image=tmp[2])
                tiger_canvas.create_image(655,345,image=tmp[3])
                m1=tmp[2]
                m2=tmp[3]
                if i==r2:
                    tiger_canvas.create_image(625,345,image=m1)
                    tiger_canvas.create_image(655,345,image=m2)
                    x2=3
            if i<=r3:
                tiger_canvas.create_image(720,345,image=tmp[0])
                tiger_canvas.create_image(750,345,image=tmp[3])
                ri1=tmp[0]
                ri2=tmp[3]
                if i==r3:
                    tiger_canvas.create_image(720,345,image=ri1)
                    tiger_canvas.create_image(750,345,image=ri2)
                    x3=1
        time.sleep(0.1)
    print(f"x1={x1} x2={x2} x3={x3}")
    if x1==x2 and x2==x3:
        if x1==1:
            print("get 10")
            clientsocket.send("win 20".encode())
        elif x1==2:
            print("get 20")
            clientsocket.send("win 30".encode())
        else:
            print("get 30")
            clientsocket.send("win 40".encode())
    elif x1!=x2 and x2!=x3 and x1!=x3:
        print("QQ")
    else:
        clientsocket.send("win 10".encode())
    time.sleep(0.1)
    clientsocket.send("clientmoney".encode())
    time.sleep(1)
    tiger_play.place(x=850,y=140)
    tiger_machine=tk.PhotoImage(file="image/tiger1.png")
    tiger_canvas.create_image(620,250,image=tiger_machine)
def tryplaytiger():
    global tigerflag
    clientsocket.send("loss 10".encode())
    time.sleep(0.1)
    clientsocket.send("clientmoney".encode())
    time.sleep(0.1)
    tigerflag=True
def playtiger():
    global tiger_canvas,tiger_play,tiger_machine
    tiger_play.place_forget()
    time.sleep(0.5)
    tiger_machine=tk.PhotoImage(file="image/tiger2.png")
    tiger_canvas.create_image(620,250,image=tiger_machine)
    time.sleep(0.5)
    tiger_machine=tk.PhotoImage(file="image/tiger3.png")
    tiger_canvas.create_image(620,250,image=tiger_machine)
    tigerrunning()
    
def gototiger():
    dellobbylayout()
    dellobbyinvitebox()
    settiger()
    clientsocket.send("entertiger".encode())
def settiger():
    global tiger_bg,tiger_return,tiger_canvas,tiger_machine,tiger_play,tiger_playimg,lobby_username,lobby_moneylabel
    tiger_canvas=tk.Canvas(width=1300,height=800)
    tiger_canvas.place(x=0,y=0)
    tiger_bg=tk.PhotoImage(file="image/tigerbg.png")
    tiger_canvas.create_image(650,400,image=tiger_bg)
    tiger_machine=tk.PhotoImage(file="image/tiger1.png")
    tiger_canvas.create_image(620,250,image=tiger_machine)
    tiger_playimg=tk.PhotoImage(file="image/playtiger.png")
    tiger_play=tk.Button(window,relief="flat",image=tiger_playimg,activebackground="black",borderwidth=0,width=60,height=50,command=tryplaytiger)
    tiger_play.place(x=850,y=140)
    tiger_return=tk.Button(window,text="返回大廳",font="微軟正黑體 24 bold",command=tigertolobby)
    tiger_return.place(x=0,y=700)
    lobby_username=tk.Label(window,pady=0,padx=0,fg='white',bg='DimGray',font="微軟正黑體 24 bold",text="玩家: "+username)
    lobby_username.place(x=950,y=40)
    lobby_moneylabel=tk.Label(window,pady=0,padx=0,fg='white',bg='DimGray',font="微軟正黑體 24 bold",textvariable=lobby_money)
    lobby_moneylabel.place(x=950,y=100)
def deltiger():
    global tiger_bg,tiger_return,tiger_canvas,tiger_machine,tiger_play,lobby_username,lobby_moneylabel
    tiger_canvas.delete("all")
    tiger_canvas.place_forget()
    tiger_return.place_forget()
    tiger_play.place_forget()
    lobby_moneylabel.place_forget()
    lobby_username.place_forget()


def tigertolobby():
    track = pygame.mixer.music.load("sound/back.mp3")
    pygame.mixer.music.play()
    deltiger()
    setlobbylayout()
    clientsocket.send("tigertolobby".encode())
#設置大廳介面
def setlobbylayout():
    global lobbyentry,lobbyentrylabel,finalcolor,lobby_canvas,lobby_character,lobby_circle,lobby_bg,lobby_gamelist,lobby_21point,lobby_21pointbutton
    global lobby_money,lobby_moneylabel,lobby_username,lobby_tiger,lobby_tigerimg
    
    track = pygame.mixer.music.load("sound/lobby.mp3")
    pygame.mixer.music.play()
    clientsocket.send("clientmoney".encode())
    lobby_canvas=tk.Canvas(width=1300,height=800)
    lobby_canvas.place(x=0,y=0)
    lobby_bg=tk.PhotoImage(file="image/pokerbg.png")
    lobby_canvas.create_image(600,400,image=lobby_bg)
    lobby_gamelist=tk.PhotoImage(file="image/gamelist.png")
    lobby_canvas.create_image(150,250,image=lobby_gamelist)
    lobby_21point=tk.PhotoImage(file="image/21point.png")
    lobby_21pointbutton=tk.Button(window,relief="flat",bg='black',activebackground="black",bd=0,image=lobby_21point,width=215,height=75,command = trygoto21)    
    lobby_21pointbutton.place(x=50,y=320)
    lobby_tigerimg=tk.PhotoImage(file="image/tigerimg.png")
    lobby_tiger=tk.Button(window,relief="flat",bg='black',activebackground="black",bd=0,image=lobby_tigerimg,width=215,height=75,command = gototiger)
    lobby_tiger.place(x=50,y=420)
    if(finalcolor=="red"):
        lobby_character=tk.PhotoImage(file="image/character_red_small.png")
        lobby_circle=tk.PhotoImage(file="image/curcle_red_small.png")
    elif(finalcolor=="blue"):
        lobby_character=tk.PhotoImage(file="image/character_blue_small.png")
        lobby_circle=tk.PhotoImage(file="image/curcle_blue_small.png")
    elif(finalcolor=="green"):
        lobby_character=tk.PhotoImage(file="image/character_green_small.png")
        lobby_circle=tk.PhotoImage(file="image/curcle_green_small.png")
    elif(finalcolor=="purple"):
        lobby_character=tk.PhotoImage(file="image/character_purple_small.png")
        lobby_circle=tk.PhotoImage(file="image/curcle_purple_small.png")
    elif(finalcolor=="yellow"):
        lobby_character=tk.PhotoImage(file="image/character_yellow_small.png")
        lobby_circle=tk.PhotoImage(file="image/curcle_yellow_small.png")
    elif(finalcolor=="gray"):
        lobby_character=tk.PhotoImage(file="image/character_gray_small.png")    
        lobby_circle=tk.PhotoImage(file="image/curcle_gray_small.png")
    lobby_canvas.create_image(140,140,image=lobby_circle)
    lobby_canvas.create_image(140,90,image=lobby_character)
    lobby_username=tk.Label(window,padx=0,pady=0,justify='left',fg='white',bg='black',font="微軟正黑體 24 bold",text="玩家: "+username)
    lobby_username.place(x=250,y=40)
    lobby_moneylabel=tk.Label(window,padx=0,pady=0,justify='left',fg='white',bg='black',font="微軟正黑體 24 bold",textvariable=lobby_money)
    lobby_moneylabel.place(x=250,y=100)

def dellobbyinvitebox():
    global lobby_canvas,lobby_inviteaccept,lobby_inviterefuse,lobby_invitemsg,lobby_inviteuser,lobby_clean
    lobby_inviteuser.place_forget()
    lobby_inviterefuse.place_forget()
    lobby_invitemsg.place_forget()
    lobby_inviteaccept.place_forget()
    lobby_clean=tk.PhotoImage(file="image/cleaninvitebox.png")
    lobby_canvas.create_image(150,700,image=lobby_clean)
#delete 大廳畫面
def dellobbylayout():
    global lobby_canvas,lobby_moneylabel,lobby_money,lobby_username,lobby_21pointbutton,lobby_tiger
    pygame.mixer.music.fadeout(1000)
    dellobbyinvitebox()
    lobby_canvas.delete("all")
    lobby_canvas.place_forget()
    lobby_username.place_forget()
    lobby_moneylabel.place_forget()
    # lobby_money.set("")
    lobby_21pointbutton.place_forget()
    lobby_tiger.place_forget()
    


window=tk.Tk()
window.geometry('1300x800')
window.title("mywindow")
#老虎機宣告
tiger_canvas=tk.Canvas()
tiger_bg=tk.PhotoImage()
tiger_return=tk.Button()
tiger_machine=tk.PhotoImage()
tiger_machine2=tk.PhotoImage()
tiger_play=tk.Button()
tiger_playimg=tk.PhotoImage()

#21點宣告
_21_canvas=tk.Canvas()
_21_bg=tk.PhotoImage()
_21_waituser=tk.PhotoImage()
_21_opencard=tk.PhotoImage()
_21_finish=tk.PhotoImage()
_21_requestcardbt=tk.Button()
_21_requestimg=tk.PhotoImage()
_21_giveupcardbt=tk.Button()
_21_giveupimg=tk.PhotoImage()
_21_cardpile=tk.PhotoImage()
cardphoto=tk.PhotoImage()
_21_card=[[cardphoto]*5 for i in range(4)]
player=[]
_21_whitehole=tk.PhotoImage()
_21_whiteholerecover=tk.PhotoImage()
_21_return=tk.Button()
_21_action=tk.Label()
_21_5img=tk.PhotoImage()
_21_10img=tk.PhotoImage()
_21_20img=tk.PhotoImage()
_21_5bt=tk.Button()
_21_10bt=tk.Button()
_21_20bt=tk.Button()
_21_gambletext=tk.PhotoImage()
_21_cleantable=tk.PhotoImage()
_21_playerinfo=[]
_21_moneyinfo=[]
for i in range(4):
    _21_moneyinfo.append(tk.Label())
    _21_playerinfo.append(tk.Label())
_21_moneytext=[]
for i in range(4):
    _21_moneytext.append(tk.StringVar())
gamblemone=[]
for i in range(4):
    gamblemone.append("")
_21_crown=tk.PhotoImage()
_21_fnumber=[]
_21_snumber=[]
_21_return2=tk.Button()
_21_cardsender=tk.PhotoImage()
_21_cardsenderinfo=tk.Label()
#-----邀請藍
_21_invitelist=tk.Listbox()
_21_scrollbar=tk.Scrollbar()
_21_invitelistbt=tk.Button()
_21_frame=tk.Frame()
_21_invitephoto=tk.PhotoImage()
listboxflag=False
_21_secondlist=tk.Listbox()
_21_tolobby=tk.PhotoImage()
#-----對話框
_21_talkimg=tk.PhotoImage()
_21_talkbt=tk.Button()
_21_sendtalkbg=tk.PhotoImage()
_21_sendtalkimg=tk.PhotoImage()
_21_sendtalkbt=tk.Button()
_21_entry=tk.Entry()
_21_msg=tk.StringVar()
talklistboxflag=False
_21_framet=tk.Frame()
_21_talklist=tk.Text()
_21_scrollbart=tk.Scrollbar()


#創建角色宣告
create_canvas=tk.Canvas()
create_bg=tk.PhotoImage()
create_circlephoto=tk.PhotoImage()
create_label=tk.PhotoImage()
create_character=tk.PhotoImage()
create_colorselectbg=tk.PhotoImage()
create_backbutton=tk.Button()
create_decidebutton=tk.Button()
create_redcolor=tk.Button()
create_bluecolor=tk.Button()
create_greencolor=tk.Button()
create_graycolor=tk.Button()
create_yellowcolor=tk.Button()
create_purplecolor=tk.Button()
create_colorselect=tk.PhotoImage()
finalcolor="blue"
# create_circlelabel=tk.Label()
# create_labellabel=tk.Label()/
# create_characterlabel=tk.Label()
# create_colorselectbglabel=tk.Label()


#大廳宣告
lobbyentrylabel=tk.Label()
lobbyentry=tk.StringVar()
lobby_canvas=tk.Canvas()
lobby_bg=tk.PhotoImage()
lobby_character=tk.PhotoImage()
lobby_circle=tk.PhotoImage()
lobby_bg=tk.PhotoImage()
lobby_gamelist=tk.PhotoImage()
lobby_21point=tk.PhotoImage()
lobby_username=tk.Label()
lobby_moneylabel=tk.Label()
lobby_money=tk.StringVar()
lobby_21pointbutton=tk.Button()
lobby_tiger=tk.Button()
lobby_tigerimg=tk.PhotoImage()
lobby_invitebox=tk.PhotoImage()
lobby_inviteuser=tk.Label()
lobby_invitemsg=tk.Label()
lobby_inviteaccept=tk.Button()
lobby_inviterefuse=tk.Button()
lobby_ivstr=tk.StringVar()
lobby_clean=tk.PhotoImage()

# 登入畫面宣告
usrnameimg=tk.PhotoImage()
usrpassimg=tk.PhotoImage()
usrpasslabel=tk.Label()
usrnameentry=tk.Entry()
usrnameentrybutton=tk.Button()
usrpassentry=tk.Entry()
usrregistbutton=tk.Button()
entry_canvas=tk.Canvas()
entrybg=tk.PhotoImage()

#註冊畫面宣告
registcanvas=tk.Canvas()
registnamebg=tk.PhotoImage()
registpassbg=tk.PhotoImage()
registnameentry=tk.Entry()
registpassentry=tk.Entry()
registbutton=tk.Button()
registbackbutton=tk.Button()
registbgimg=tk.PhotoImage()

#regist error message
registerror=tk.StringVar()
registerrorlabel=tk.Label()


#enter error message
entererror=tk.StringVar()
entererrorlabel=tk.Label()

entername=tk.StringVar()
enterpass=tk.StringVar()
registname=tk.StringVar()
registpass=tk.StringVar()

setuserentrylayout()

label=[]
var=[]

thread = threading.Thread(target=listenthread)
thread.start()
thread2= threading.Thread(target=drawthread)
thread2.start()
def onclose():
    clientsocket.send(DISCONNECT_MESSAGE.encode())
    pygame.mixer.music.stop()
    window.destroy()

window.protocol("WM_DELETE_WINDOW",onclose)
window.mainloop()
