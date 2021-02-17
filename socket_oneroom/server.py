import socket
import threading
import time
import random

HOST="127.0.0.1"
PORT=8080
ADDR=(HOST,PORT)
DISCONNECT_MESSAGE="disconnect"

serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversocket.bind(ADDR)
userdata=[] #使用者姓名
passdata=[] #使用者密碼
room=["empty","empty","empty","empty"]     #遊戲房間的人
roomstate=int(0) #房間是否開始遊戲
userstate={} #使用者狀態 -2:離線 -1:在大廳 0:在房間
usercharacter={} #使用者角色顏色
usercard={} #玩家手中現有的牌
usercard2={} #玩家手上原有的牌
userknow={} #玩家是否有收到牌改變的訊息
userknowplayerchange={} #玩家是否知道已經換下一個玩家了
usermoney={} #玩家的資金
playerchange=False
invitelist={} #看玩家是否有被邀請
leftcard=[] #剩餘卡牌
playerstate=[] #玩家是否可以繼續要牌
playerpoint={} #玩家的牌大小 -1代表過五關 0~21 代表牌面大小 >21
playergamble={} #玩家下注金額
nowplayer=int(0) #現在輪到誰
playeraction=int(0) #現在玩家做了什麼動作 0放棄 1要牌
initcheck=False #遊戲開始檢查
finish=False #遊戲結束
roommsg=[] #聊天室
def usernamexsit(username):
    for i in userdata:
        if(i==username):
            return True
    return False
def setuserinfo(username,password):
    wfile=open("username.txt","a")
    wfile.write(" "+username)
    userdata.append(username)
    wfile.close()
    wfile=open("userpass.txt","a")
    wfile.write(" "+password)
    passdata.append(password)
    wfile.close()
def setusercharacter(username,character):
    wfile=open("usercharacter.txt","a")
    wfile.write(" "+username+" "+character)
    usercharacter.update({username:character})
    wfile.close()

def setusermoney(username,money):
    money=str(money)
    wfile=open("usermoney.txt","a")
    wfile.write(" "+username+" "+money)
    usermoney.update({username:int(money)})
    wfile.close()

def checkname(username):
    print(userdata)
    print(username)
    for i in userdata:
        if(i==username):
            return True
    return False
def checkpass(username,password):
    for i in range(len(userdata)):
        if userdata[i]==username :
            if passdata[i]==password:
                return True
    return False
def checkusercharacter(username):
    if username in usercharacter:
       return usercharacter[username] 
    else:
        return "nocharacter" 
def enterroom(username):
    for i in range(4): #尋找房間空位
        if room[i]=="empty":
            room[i]=username
            userstate[username]=0
            break


def checkcardchange():
    global usercard,usercard2
    if usercard==usercard2:
        return True
    else:
        return False

def initroom():
    global initcheck,roomstate,usercard,usercard2,userknow,userknowplayerchange,playerchange,nowplayer,playerstate,room,finish,roommsg
    for i in range(len(room)):
        room[i]="empty"
    initcheck=False
    finish=False
    roomstate=int(0)
    usercard.clear()
    usercard2.clear()
    userknow.clear()
    userknowplayerchange.clear()
    playerchange=False 
    playerpoint.clear()
    nowplayer=int(0)
    roommsg.clear()
    playerstate.clear()
    print(f"len:{len(playerstate)}")

def instantrefresh(conn,username):
    flag=False
    gamestartflag=False
    finishflag=False
    gambleflag=False
    msglen=int(0) #偵測有人傳訊息
    global initcheck,roomstate,usercard,usercard2,userknow,userknowplayerchange,playerchange,nowplayer,playerstate
    while True:
        if userstate[username]==0: #玩家在房間內
            if len(roommsg)>msglen: #有人傳訊息
                msglen=len(roommsg)
                talklist(conn,2)
                time.sleep(0.05)
            if roomstate!=4:  #該房間還沒開始
                msg="roommember "
                for i in room:
                    msg+=" "
                    msg+=i
                    msg+=" "
                    if i=="empty":
                        msg+="empty"
                    else:
                        msg+=usercharacter[i]
                conn.send(msg.encode())
                count=0
                for i in range(4):
                    if room[i]!="empty":
                        count+=1
                if count==4 : #四人到齊 準備開始
                    if flag==False:
                        roomstate+=1
                        finishflag=False
                        flag=True
            else:
                if finish==False:
                    if initcheck==False: #遊戲開始初始化
                        initcheck=True
                        for i in range(4):
                            playerstate.append(0)
                        for i in range(1,53):  #初始卡牌
                            leftcard.append(i)
                        for i in room: #初始玩家手牌
                            playergamble[i]=0
                            playerpoint[i]=0
                            usercard[i]=" "
                            userknow[i]=0
                            userknowplayerchange[i]=0
                   
                    if gamestartflag==False: #遊戲開始 
                        if gambleflag==False: #叫玩家下注
                            conn.send("gamble".encode())
                            gambleflag=True
                        if checkgamble()==False: #等待玩家都下賭注
                            continue   

                        conn.send("gamestart".encode())
                        gamestartflag=True
                        time.sleep(0.1)
                        for i in room:
                            smsg="setuserinfo "
                            smsg+=i
                            smsg+=" "
                            smsg+=str(playergamble[i])
                            conn.send(smsg.encode())
                            time.sleep(0.1)
                        conn.send("nowplayer 0 0".encode())
                        time.sleep(0.1)
                    
                    if checkcardchange()==False:  #牌改變了
                        if userknow[username]==0:
                            userknow[username]=1
                            for i in room:  #傳送給玩家 四個玩家分別有的卡片
                                msg="refreshusercard "+i
                                msg+=usercard[i]
                                conn.send(msg.encode())
                                time.sleep(0.1)
                        flagtmp=True
                        for i in room:
                            if userknow[i]==0:
                                flagtmp=False
                        if flagtmp==True:#等到四個人都收到改變的訊息
                            for i in room:
                                userknow[i]=0
                            for i in usercard:
                                usercard2[i]=usercard[i]
                    if playerchange==True:        #換下一個玩家
                        # print(userknowplayerchange)
                        # print(f"nowplayer{nowplayer}")
                        if userknowplayerchange[username]==0:
                            userknowplayerchange[username]=1
                            changeplayer(conn)
                        flagtmp=True
                        for i in room:
                            if userknowplayerchange[i]==0:
                                flagtmp=False
                        if flagtmp==True:
                            for i in room:
                                userknowplayerchange[i]=0
                            nowplayer+=1
                            playerchange=False
                else: #遊戲結束
                    if finishflag==False:
                        conn.send("finish".encode())
                        time.sleep(1)
                        for i in room:  #開牌
                            msg="opencard "+i
                            msg+=usercard[i]
                            conn.send(msg.encode())
                            time.sleep(0.1)
                        for i in room:
                            msg="cardpoint "
                            print(f"i={i} playerpoint[{i}]={playerpoint[i]}")
                            msg+=str(playerpoint[i])
                            conn.send(msg.encode())
                            time.sleep(0.1)
                        finishflag=True
                        flag=False
                        userstate[username]=-2
                        gamestartflag=False
                        gambleflag=False
                        msglen=int(0)
                        initroom()
        elif userstate[username]==-1:
            
            if invitelist[username]!="empty":
                msg="youareinvited "+invitelist[username]
                invitelist[username]="empty"
                conn.send(msg.encode())                

            
        time.sleep(0.5)

def setgamble(username,money):
    playergamble[username]=money
    # print(f"playergamble{playergamble}")
def checkgamble():
    cnt=int(0)
    for i in room:
        if i=="empty":
            continue
        if int(playergamble[i])>0:
            cnt+=1
    if cnt==3:
        return True
    else:
        return False
def changeplayer(conn):
    global nowplayer,playerstate,playerpoint,usercard,playeraction
    smsg=""
    if playeraction==0:
        smsg="playeraction 0 "+str((nowplayer)%4)
    else:
        smsg="playeraction 1 "+str((nowplayer)%4)
    conn.send(smsg.encode())
    # time.sleep(1)
    #換到下一個玩家回合
    np=(nowplayer+1)%4
    username=room[np]
    x=usercard[username]
    x=x.split()
    print(f"nextplayer={username}")
    if playerstate[np]==1 or playerpoint[username]>21 or len(x)==5: #已經放棄或牌面超過21點或過五關 只能選擇放棄要牌
        smsg="nowplayer 1 "+str(np)
    else:
        smsg="nowplayer 0 "+str(np)
    conn.send(smsg.encode())    
  
def giveyoucard(conn,username): #玩家要牌
    global playerpoint
    x=random.randint(0,len(leftcard)-1) #隨機從剩餘牌中挑一張牌
    usercard[username]+=" "
    usercard[username]+=str(leftcard[x]) #新增至玩家手牌
    calplayerpoint(username,leftcard[x])
    leftcard[x:x+1]=[] #扣除那張牌
    print(f"usercard:{usercard}")

def calplayerpoint(username,card):
    global playerpoint
    playerpoint[username]+=(card%13)
    if card%13==0:
        playerpoint[username]+=13
    if playerpoint[username]>21: #爆掉了
        # playerpoint[username]=-1
        # giveupcard(username)
        return
    x=usercard[username]
    x=x.split()
    if len(x)==5: #過五關
        playerpoint[username]=-1

def checkfinish():
    cnt=int(0)    
    for i in range(4):
        print(f"playerstate[{i}]:{playerstate[i]}")
        if playerstate[i]==1:
            cnt+=1
    if cnt==4:
        return True
    else:
        return False
def giveupcard(username):
    global playerstate,room,finish
    for i in range(len(room)):
        if username==room[i]:
            playerstate[i]=1
            break
    if checkfinish()==True:
        finish=True
def savemoneyindate():
    wfile=open("usermoney.txt","w")
    key=usermoney.keys()
    for i in key:
        wfile.write(" ")
        wfile.write(i)
        wfile.write(" ")
        wfile.write(str(usermoney[i]))
    wfile.close()
def changemoney(lw,username,money):
    if lw==0: #輸錢
        usermoney[username]-=int(money)
    else: #贏錢
        usermoney[username]+=int(money)  
    savemoneyindate()#存入資料庫

def talk(username,msg,conn):
    roommsg.append(username+">>"+msg)
    time.sleep(0.05)

def talklist(conn,op):
    smsg="talklist"+str(op)
    for i in roommsg:
        smsg=smsg+" "+i
    conn.send(smsg.encode())
def handle_client(conn ,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    global playerchange,playeraction
    connected =True
    username=""
    while connected:
        msg=conn.recv(200).decode()
        if msg:
            x=msg.split()
            if x[0]=="enter":
                if checkname(x[1]):
                    if checkpass(x[1],x[2]):
                        username=x[1]
                        thread2=threading.Thread(target=instantrefresh,args=(conn,x[1]))
                        thread2.start()
                        smsg=""
                        character=checkusercharacter(x[1])
                        if character=="nocharacter":
                            smsg="needcharacter"
                        else:
                            userstate[x[1]]=-1
                            time.sleep(0.1)
                            smsg="entersuccess "+character
                        conn.send(smsg.encode())
                    else:
                        conn.send("enterfail passworderror".encode())
                else:
                    conn.send("enterfail noname".encode())
            elif x[0]=="regist" :
                if usernamexsit(x[1]):
                    conn.send("registfail usernameexit".encode())
                    continue
                setuserinfo(x[1],x[2])
                setusermoney(x[1],100)
                userstate.update({x[1]:-2})
                conn.send("registsuccess".encode())
            elif x[0]=="inviteuser":
                invitelist[x[1]]=username
            elif x[0]=="createsuccess":
                setusercharacter(x[1],x[2])
                invitelist.update({x[1]:"empty"})
                userstate[x[1]]=-1
            elif x[0]=="invitelist":
                key=userstate.keys()
                smsg="invitelist"
                for i in key:
                    if userstate[i]==-1:
                        smsg=smsg+" "+i
                conn.send(smsg.encode())
            elif x[0]=="21": #玩家進入21點房間
                if roomstate==4:
                    conn.send("enterroomfail".encode())
                else:
                    enterroom(x[1])
                    conn.send("enterroomsuccess".encode())
            elif x[0]=="setgamble": #設定玩家的賭金
                setgamble(username,x[1])
            elif x[0]=="requestcard": #玩家要牌
                giveyoucard(conn,username)
                playerchange=True
                playeraction=1
            elif x[0]=="clientmoney": #玩家的資金
                smsg="usermoney "+str(usermoney[username])
                conn.send(smsg.encode())
            elif x[0]=="giveupcard": #玩家放棄要牌
                giveupcard(username)
                playerchange=True
                playeraction=0
            elif x[0]=="talk": #玩家講話
                talk(x[1],x[2],conn)
            elif x[0]=="talklist": #傳送最新的對話紀錄
                talklist(conn,1)
            elif x[0]=="loss":
                changemoney(0,username,x[1])
            elif x[0]=="win":
                changemoney(1,username,x[1])
            elif x[0]=="returntolobby": #玩家離開房間
                exitroom(username)
                userstate[username]=-1
            elif x[0]=="entertiger": #進入老虎機 不能邀請
                userstate[username]=1
            elif x[0]=="tigertolobby": #回到大廳
                userstate[username]=-1
            elif msg==DISCONNECT_MESSAGE: #玩家離線
                conn.send("bye".encode())
                break
            print(f"[{addr}] {msg}")
    exitroom(username)
    userstate[username]=-2    
    conn.close()
    print("disconnect")

def exitroom(username):
    if username!="" and userstate[username]==0:
        index=-1
        for i in range(len(room)):
            if room[i]==username:
                index=i
                break
        room[index]="empty"

def start():
    serversocket.listen()
    print("server is listening...")
    while True:
        conn , addr =serversocket.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

def init():
    rfile=open("username.txt","r")
    msg=rfile.read()
    msg=msg.split()
    for i in msg:
        userstate.update({i:-2})
        invitelist.update({i:"empty"})
        userdata.append(i)
    rfile.close()
    rfile=open("userpass.txt","r")
    msg=rfile.read()
    msg=msg.split()
    for i in msg:
        passdata.append(i)
    rfile.close()
    rfile=open("usercharacter.txt","r")
    msg=rfile.read()
    msg=msg.split()
    for i in range(len(msg)):
        if i%2==1:
            usercharacter.update({msg[i-1]:msg[i]})
    rfile.close()
    rfile=open("usermoney.txt","r")
    msg=rfile.read()
    msg=msg.split()
    for i in range(len(msg)):
        if i%2==1:
            usermoney[msg[i-1]]=int(msg[i])
    rfile.close()
    

init()
start()
