import win32com.client as comctl
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from settings import *
import maskpass
import platform
import settings
import cursor
import socket
import psutil
import uuid
import time
import mail
import rich
import sys
import emu
import re
import os

time_i = datetime.now()


def setIntTime(arg):
    global time_i
    time_i = arg
    return

class Help:
    Verbose("VERBOSE: Inside Begin Block: commands/Help")

    def __init__(self):
        self.show_menu()

    @staticmethod
    def show_menu():
        Verbose("VERBOSE: Inside Process Block: commands/Help/show_menu")
        h = Table(title="Help Menu", box=None, title_style="")
        console = Console()
        h.add_column("")
        h.add_column("", width=7)
        h.add_column("", width=15)
        h.add_column("")

        for i in range(0, len(cmds)):
            h.add_row(cmds[i]["chr"], cmds[i]["name"], cmds[i]["args"], cmds[i]["description"])

        console.print(h)
        Verbose("VERBOSE: End Process Block: commands/Help/show_menu")

class Quit:
    Verbose("VERBOSE: Inside Begin Block: commands/Exit")

    def __init__(self):
        Verbose("VERBOSE: Inside Process Block: commands/Exit/__init__")
        Verbose("VERBOSE: End Process Block: commands/Exit/__init__")
        Clear()
        with open("vars.json", 'r') as f: data = json.load(f); settings_path = data['settings_path']
        with open(settings_path, 'r', encoding='utf-8') as file: settings = json.load(file)
        for profile in settings['profiles']['list']: profile['colorScheme'] = "Campbell"
        with open(settings_path, 'w', encoding='utf-8') as file: json.dump(settings, file, indent=4)
        wsh = comctl.Dispatch("WScript.Shell")
        wsh.SendKeys("{F11}")
        os.system("cmd")

class Clear:
    Verbose("VERBOSE: Inside Begin Block: commands/Clear")

    def __init__(self):
        Verbose("VERBOSE: Inside Process Block: commands/Clear/__init__")
        os.system("cls")
        Verbose("VERBOSE: End Process Block: commands/Clear/__init__")

class Test:
    Verbose("VERBOSE: Inside Begin Block: commands/Test")

    def __init__(self, args):
        Verbose("VERBOSE: Inside Process Block: commands/Test/__init__")
        print(int(args[0]) + int(args[1]))
        Verbose("VERBOSE: End Process Block: commands/Test/__init__")
        print("\033[92mFinished in " + str(datetime.now()-time_i) + "\033[0m")

class Theme:
    def __init__(self, args=""):
        try:
            if "_" in args[0]: args[0] = args[0].replace("_", " ")
            setTheme(args[0])
        except Exception as e: print(getTheme())

class Themes:
    def __init__(self):
        with open("vars.json", 'r') as f: data = json.load(f); settings_path = data['settings_path']
        with open(settings_path, 'r', encoding='utf-8') as file: settings = json.load(file)

        themes = []
        bgs = []
        fgs = []

        for theme in settings['schemes']:
            themes.append(theme['name'])
            hbg = theme['background'].lstrip("#")
            hfg = theme['foreground'].lstrip("#")
            bgs.append(tuple(int(hbg[i:i+2], 16) for i in (0, 2, 4)))
            fgs.append(tuple(int(hfg[i:i+2], 16) for i in (0, 2, 4)))

        for theme in themes: t = theme.replace(" ", "_"); themes[themes.index(theme)] = " "+t+" "

        for i in range(0, len(themes)):
            if themes[i].replace("_", " ").strip(" ") == getTheme():
                prev = "\033[4m"
                themes[i] = prev+themes[i]+"\033[24m"
            else:
                prev = f"\033[38;2;{fgs[i][0]};{fgs[i][1]};{fgs[i][2]}m\033[48;2;{bgs[i][0]};{bgs[i][1]};{bgs[i][2]}m"
                themes[i] = prev+themes[i]+"\033[0m"

        print(*themes)

class TermFX:
    @staticmethod
    def toggle_fx():
        with open("vars.json", 'r') as f: data = json.load(f); settings_path = data['settings_path']
        with open(settings_path, 'r', encoding='utf-8') as file: settings = json.load(file)

        for profile in settings['profiles']['list']:
            if 'experimental.retroTerminalEffect' in profile: profile['experimental.retroTerminalEffect'] = not profile['experimental.retroTerminalEffect']
            else: profile['experimental.retroTerminalEffect'] = True

        with open(settings_path, 'w', encoding='utf-8') as file: json.dump(settings, file, indent=4)

class ls:
    def __init__(self, args=""):

        if args=="":
            with open("vars.json", 'r') as f: data = json.load(f); settings_path = data['settings_path']
            self.listDir(data['dir'])
        elif ":" in args[0]:
            if os.path.isdir(args[0]): self.listDir(args[0])
            else: InvalidDirectory(args[0])
        else:
            with open("vars.json", 'r') as f: data = json.load(f); settings_path = data['settings_path']
            dir = data['dir']
            arg = args[0][:len(args[0]) - 1] if args[0][-1] == "\\" else args[0]
            if dir[-1] != "\\": dir = dir + "\\"
            if arg[0] == "\\": arg = arg[1:]

            if os.path.isdir(dir + arg): self.listDir(dir + arg)
            else: InvalidDirectory(arg)

    def listDir(self, arg):
        directory = os.listdir(arg)
        dir = Table(box=None, title_style="")
        console = Console()
        dir.add_column("", width=24)
        dir.add_column("")
        dir.add_column("", width=12, justify="right")
        dir.add_column("")

        for file in directory:
            f = f"{arg}\\{file}"
            dateA = str(time.ctime(os.path.getatime(f)))
            ftype = "<DIR>" if os.path.isdir(f) else ""
            size = str(round(os.path.getsize(f)/1024, 2))+" KB"
            name = f"\033[7m\033[94m{file}\033[0m" if os.path.isdir(f) else f"\033[93m{file}\033[0m"

            dir.add_row(dateA, ftype, size, name)

        print("\n"+arg)
        console.print(dir)
        print("")

class cd:
    def __init__(self, args):
        setDir(args[0])

class Emu:
    def __init__(self, args=""):
        try: emu.run(args[0])
        except: emu.run(args)

class Mail:
    def __init__(self):
        mail.main()

class Sysinfo:
    def __init__(self):
        try:
            info = {}
            info['Platform']=platform.system()
            info['Platform Release']=platform.release()
            info['Platform Version']=platform.version()
            info['Architecture']=platform.machine()
            info['Hostname']=socket.gethostname()
            info['IP Address']=socket.gethostbyname(socket.gethostname())
            info['MAC Address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
            info['Processor']=platform.processor()
            info['RAM']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
            for i in info:
                label = f"\033[93m{i}\033[0m"
                print(label,"::",info.get(i))
        except Exception as e:
            print("unexpected error")

class Home:
    def __init__(self):
        os.system("cls")
        with open("vars.json", 'r') as f: data = json.load(f)
        setTheme(data['theme'])
        with open("logo.txt") as f: print(f.read())
        print(data['version'])
        print("-" * 50)
        if data["desc"]=="" or data["desc"].isspace(): self.desc="'help' to display a list of commands"
        else: self.desc=data["desc"]
        print(self.desc)
        print("-" * 50)

    def login(self):
        with open("vars.json", 'r') as f: data = json.load(f)
        if data['username'] == 0:
            print("\033[91mUsername not detected", end="\033[0m \n")
            data['username'] = self.editUsr()

        if data['password'] == 0:
            print("\033[91mPassword not detected", end="\033[0m \n")
            data['password'] = self.editPswd()

        with open("vars.json", 'w') as f: json.dump(data, f, indent=4)

        print("\033[93mLogin")
        while True:
            try:
                if data['username'] == input("\033[93mUsername: "):
                    if data['password'] == getpass("\033[93mPassword: "):
                        print("\033[92mLogin Successful\n", end="\033[0m \n")
                        break
                    else: InvalidCredentials()
                else: InvalidCredentials()
            except Exception as e:
                InvalidCredentials()
        f.close()

    @staticmethod
    def editUsr():
        with open("vars.json", 'r') as f: data = json.load(f)
        usr = ""  # secondary credential var
        data['username'] = input("\033[33mSet Username: ")
        while data['username'] != usr:
            usr = input("\033[33mRetype Username: ")
            print("", end="\033[0m \n")
            if data["username"] != usr:
                print("\033[91mUsernames do not match", end="\033[0m \n")
        f.close()
        return usr

    @staticmethod
    def editPswd():
        with open("vars.json", 'r') as f:
            data = json.load(f)
        pswd = ""  # secondary credential var
        data['password'] = getpass("\033[33mSet Password: ")
        while data['password'] != pswd:
            pswd = getpass("\033[33mRetype Password: ")
            print("", end="\033[0m \n")
            if data['password'] != pswd:
                print("\033[91mPasswords do not match", end="\033[0m \n")
        f.close()
        return pswd

class screenSaver:
    def __init__(self):
        Clear()
        print("\n"*15)
        with open("logo.txt") as f: print(f.read())
        with open("vars.json", 'r') as f: data = json.load(f)
        usr = data["username"]
        cols, rows = os.get_terminal_size()
        usr = usr.center(cols)
        print("\n"+usr)
        cursor.hide()
        loggedout = True
        while loggedout:
            if getpass("") == data["password"]: Clear(); Home(); loggedout = False
            else: print("\033[34;97H\033[31mIncorrect Password\033[0m"); time.sleep(.2)



