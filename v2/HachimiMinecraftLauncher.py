
from tkinter import ttk
import minecraft_launcher_lib
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *
import json
import requests
import subprocess
import sys
import os
import uuid
import multiprocessing


os.makedirs(".minecraft", exist_ok=True)
os.makedirs(".minecraft/versions", exist_ok=True)

PlayerName = "UnloggedIn"
UUID = ""
minecraft_directory = ".minecraft"

def RefreshUI():
    UserName["text"] = PlayerName
    WelcomeMsg["text"] = "欢迎！玩家 " + PlayerName

def Login():

    def ReturnLoginStatus():
        PlayerName = PlayerNameE.get()
        if (PlayerName!=""):
            PlayerName = PlayerNameE.get()
            UserName["text"] = PlayerName
            WelcomeMsg["text"] = "欢迎！玩家 " + PlayerName
            global UUID
            UUID = UUIDE.get()
            if (UUID != ""):
                UUID = UUIDE.get()
            else:
                UUID = str(uuid.uuid4())
            LoginType["text"] = "离线登录×"
            Loginpage.destroy()
        else:
            showwarning("提示","请输入合法有效的昵称")


    def MicrosoftLogin():
        showinfo("提示","微软账号登录制作中")


    Loginpage = Tk()
    Loginpage.title("登录账号")
    width = 400
    height = 230
    screenwidth = Loginpage.winfo_screenwidth()
    screenheight = Loginpage.winfo_screenheight()
    geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    Loginpage.geometry(geometry)
    Loginpage.resizable(width=False, height=False)
    Loginpage.iconbitmap('assets/icon.ico')

    PlayerNameinfo = Label(Loginpage,text="昵称",font=('幼圆',15))
    PlayerNameinfo.place(x=10, y=30, width=100, height=30)

    PlayerNameE = Entry(Loginpage)
    PlayerNameE.place(x=120, y=30, width=270, height=30)

    UUIDinfo = Label(Loginpage,text="UUID",font=('幼圆',15))
    UUIDinfo.place(x=10, y=70, width=100, height=30)

    UUIDE = Entry(Loginpage)
    UUIDE.place(x=120, y=70, width=270, height=30)

    Tips = Label(Loginpage,text="UUID为玩家的唯一标识符，留空启动器将自动为您生成",font=('幼圆',10))
    Tips.place(x=10, y=110, width=380, height=24)

    OfflineLogin = Button(Loginpage,text="离线登录",command=ReturnLoginStatus)
    OfflineLogin.place(x=80, y=160, width=100, height=40)

    MicrosoftLogin = Button(Loginpage,text="微软登录",command=MicrosoftLogin)
    MicrosoftLogin.place(x=200, y=160, width=100, height=40)


def HachimiPlaza():

    def DownSelectedVersion():
        if (SelectedSource=="" or SelectedDownVersion==""):
            showinfo("提示","请选择合法有效的下载源或游戏版本")
        else:
            showinfo("提示","下载进程已开始，若程序未响应，请耐心等待")
            current_max = 0

            def set_status(status: str):
                print(status)

            def set_progress(progress: int):
                if current_max != 0:
                    print(f"{progress}/{current_max}")

            def set_max(new_max: int):
                global current_max
                current_max = new_max

            callback = {
                "setStatus": set_status,
                "setProgress": set_progress,
                "setMax": set_max
            }

            minecraft_launcher_lib.install.install_minecraft_version(SelectedDownVersion.get(), minecraft_directory, callback)

    HachimiPlaza = Tk()
    HachimiPlaza.title("Hachimi Plaza 广场")
    width = 800
    height = 460
    screenwidth = HachimiPlaza.winfo_screenwidth()
    screenheight = HachimiPlaza.winfo_screenheight()
    geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    HachimiPlaza.geometry(geometry)
    HachimiPlaza.resizable(width=False, height=False)
    HachimiPlaza.iconbitmap('assets/icon.ico')

    infosource = Label(HachimiPlaza,text="下载源",font=('幼圆',15))
    infosource.place(x=10, y=10, width=80, height=40)

    SelectedSource = Combobox(HachimiPlaza, state="readonly")
    SelectedSource['values'] = ("mojang", "BMCLAPI(未开放)", "MCBBS下载源(未开放)", "Hachimi Minecraft API(未开放)")
    SelectedSource.place(x=10, y=60, width=240, height=30)

    infodownversion = Label(HachimiPlaza,text="游戏版本",font=('幼圆',15))
    infodownversion.place(x=10, y=100, width=120, height=40)

    DownVersions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
    DownVersionList = []
    for i in DownVersions:
        DownVersionList.append(i["id"])
    SelectedDownVersion = Combobox(HachimiPlaza, state="readonly")
    SelectedDownVersion['values'] = (DownVersionList)
    SelectedDownVersion.place(x=10, y=150, width=180, height=30)

    Download = Button(HachimiPlaza, text="下载",command=DownSelectedVersion)
    Download.place(x=200, y=150, width=50, height=30)

    infodowntask = Label(HachimiPlaza,text="下载进程",font=('幼圆',15))
    infodowntask.place(x=260, y=10, width=160, height=40)

    TaskProgress = Progressbar(HachimiPlaza, orient=HORIZONTAL)
    TaskProgress.place(x=260, y=100, width=240, height=24)

    infotaskname = Label(HachimiPlaza,text="暂无下载内容",font=('幼圆',12))
    infotaskname.place(x=260, y=60, width=240, height=30)

    infoforge = Label(HachimiPlaza,text="未完待续",font=('幼圆',30))
    infoforge.place(x=280, y=280, width=240, height=60)

    downtip = Label(HachimiPlaza, text="Tips:初次下载消耗时间可能较长,请耐心等待,时间大约5~10分钟。下载正在努力优化中。",font=('幼圆',12))
    downtip.place(x=10, y=420, width=780, height=30)


def LaunchGame():
    if (LoginType["text"]=="未登录?"):
        showwarning("提示","您未登录")
    else:
        if (GameVersion.get()=="" or GameVersion.get()=="没有游戏捏,前往HachimiPlaza逛一下吧"):
            showwarning("提示","请选择游戏版本")
        else:
            options = {
                "username": PlayerName,
                "uuid": UUID,
                "token": UUID,
                "LauncherName": "Hachimi Minecraft Launcher",
                "LauncherVersion": "0.0.1"
            }
            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(GameVersion.get(),
                                                                                     minecraft_directory,
                                                                                     options)
            #Launch_process = multiprocessing.Process(target=subprocess.call(minecraft_command))
            #Launch_process.start()
            subprocess.call(minecraft_command)


root = Tk()
root.title("Hachimi Minecraft Launcher")
width = 800
height = 460
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(geometry)
root.resizable(width=False, height=False)
root.iconbitmap('assets/icon.ico')

#Background = PhotoImage(file=r"assets/bg.gif")
#Bg = Label(text="Background",image=Background)
#Bg.place(x=0, y=0, width=800, height=460)

LaunchIcon = PhotoImage(file=r"assets/Launch.gif")
Launch = Button(text="启动游戏",image=LaunchIcon,command=LaunchGame)
Launch.place(x=610, y=390, width=180, height=60)

WelcomeMsg = Label(text="欢迎！请您登录游戏账号",font=('幼圆',20))
WelcomeMsg.place(x=10, y=390, width=520, height=60)

infouser = Label(text="账户",font=('幼圆',15))
infouser.place(x=10, y=10, width=80, height=40)

UserName = Label(text="UnloggedIn",font=('幼圆',15))
UserName.place(x=10, y=60, width=240, height=30)

LoginType = Label(text="未登录?",font=('幼圆',12))
LoginType.place(x=10, y=100, width=150, height=30)

infogameversion = Label(text="游戏",font=('幼圆',15))
infogameversion.place(x=10, y=140, width=80, height=40)

Versions = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)
VersionList = []
for i in Versions:
    VersionList.append(i["id"])
if (VersionList==[]):
    VersionList = ["没有游戏捏,前往HachimiPlaza逛一下吧"]
GameVersion = Combobox(state="readonly")
GameVersion['values'] = (VersionList)
GameVersion.place(x=10, y=190, width=240, height=30)

infomore = Label(text="更多",font=('幼圆',15))
infomore.place(x=10, y=230, width=80, height=40)

SettingsIcon = PhotoImage(file=r"assets/Settings.gif")
Settings = Button(text="设置",image=SettingsIcon)
Settings.place(x=10, y=280, width=100, height=30)

MutiplayerIcon = PhotoImage(file=r"assets/Multiplayer.gif")
Multiplayer = Button(text="多人游戏",image=MutiplayerIcon)
Multiplayer.place(x=10, y=320, width=100, height=30)

Status = Label(text="启动器版本v2.0.1-alpha",font=('幼圆',10))
Status.place(x=10, y=360, width=780, height=20)

PlazaIcon = PhotoImage(file=r"assets/Plaza.gif")
HachimiPlaza = Button(text="Hachimi Plaza",image=PlazaIcon,command=HachimiPlaza)
HachimiPlaza.place(x=300, y=20, width=200, height=200)

NewsIcon = PhotoImage(file=r"assets/News.gif")
News = Button(text="News",image=NewsIcon)
News.place(x=540, y=20, width=200, height=320)

LoginIcon = PhotoImage(file=r"assets/Login.gif")
Login = Button(text="登录",image=LoginIcon,command=Login)
Login.place(x=170, y=100, width=80, height=30)

multiprocessing.freeze_support()
root.mainloop()