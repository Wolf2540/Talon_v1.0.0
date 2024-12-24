from datetime import datetime
from getpass import getpass
import json
import os

pages = [
        {"symbol": "$", "name": "home", "desc": "default page"},
        {"symbol": "#", "name": "test", "desc": "test page"}
]

cmds = [
    {"chr": "h", "name": "help", "args": f"\[none]", "description": "opens help menu", "function": "commands.Help"},
    {"chr": "q", "name": "quit", "args": f"\[none]", "description": "exits program", "function": "commands.Quit"},
    {"chr": "clr", "name": "clear", "args": f"\[none]", "description": "clear screen", "function": "commands.Clear"},
    {"chr": "t", "name": "test", "args": f"\[int],\[int]", "description": "test cmd", "function": "commands.Test"},
    {"chr": "", "name": "pages", "args": f"\[none]", "description": "lists available pages", "function": "page.listPages"},
    {"chr": "p", "name": "page", "args": f"\[str]", "description": "changes page", "function": "page.setPage"},
    {"chr": "", "name": "thread", "args": f"\[none]", "description": "multithreading test", "function": "commands.Thread"},
    {"chr": "", "name": "home", "args": f"\[none]", "description": "return to home screen", "function": "commands.Home"},
    {"chr": "t", "name": "theme", "args": f"\[mix]", "description": "change terminal theme", "function": "commands.Theme"},
    {"chr": "", "name": "themes", "args": f"\[none]", "description": "list available themes", "function": "commands.Themes"},
    {"chr": "", "name": "fx", "args": f"\[none]", "description": "toggle Terminal effects", "function": "commands.TermFX.toggle_fx"},
    {"chr": "", "name": "ls", "args": f"\[mix]", "description": "list files in current directory", "function": "commands.ls"},
    {"chr": "", "name": "cd", "args": f"\[str]", "description": "changes directory", "function": "commands.cd"},
    {"chr": "", "name": "mail", "args": f"\[none]", "description": "open mail", "function": "commands.Mail"},
    {"chr": "", "name": "sysinfo", "args": f"\[none]", "description": "show system info", "function": "commands.Sysinfo"},
    {"chr": "", "name": "emu", "args": f"\[mix]", "description": "begin Emu session", "function": "commands.Emu"},
    {"chr": "l", "name": "logout", "args": f"\[none]", "description": "return to login screen", "function": "commands.screenSaver"},

]

def getTime():
    with open("vars.json", 'r') as f: data = json.load(f)

    if data['verbose'] == 1 or data['verbose'] == 2:
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        return datetime.utcnow().strftime("%H:%M:%S")

def setVerbose(arg):
    with open("vars.json", 'r') as f: data = json.load(f)
    if arg not in [0, 1, 2]: InvalidVerboseMode(arg)
    else: data['verbose'] = arg
    f.close()

    with open("vars.json", 'w') as f: json.dump(data, f, indent=4)
    f.close()

def getVerbose():
    with open("vars.json", 'r') as f: data = json.load(f)
    return data['verbose']

def setTheme(arg):
    with open("vars.json", 'r') as f: data = json.load(f); settings_path = data['settings_path']
    with open(settings_path, 'r', encoding='utf-8') as file: settings = json.load(file)

    valid_themes = []

    for theme in settings['schemes']: valid_themes.append(theme['name'])
    if arg in valid_themes:
        for profile in settings['profiles']['list']: profile['colorScheme'] = arg
        data['theme'] = arg
        with open("vars.json", 'w') as f: json.dump(data, f, indent=4)
        with open(settings_path, 'w', encoding='utf-8') as file: json.dump(settings, file, indent=4)
    else: InvalidTheme(arg)

def getTheme():
    with open("vars.json", 'r') as f: data = json.load(f)
    return data['theme']

def setDir(arg):
    with open("vars.json", 'r') as f: data = json.load(f)
    if ":" in arg:
        if os.path.isdir(arg): data['dir'] = arg
        else: InvalidDirectory(arg)
    elif ".." in arg:
        if data['dir'].rfind("\\") != -1:
            data['dir'] = data['dir'][:data['dir'].rfind("\\")]
        else: pass
    else:
        dir = data['dir']
        arg = arg[:len(arg)-1] if arg[-1] == "\\" else arg

        if dir[-1] != "\\": dir = dir + "\\"

        if arg[0] == "\\": arg = arg[1:]

        if os.path.isdir(dir + arg): data['dir'] = dir + arg
        else: InvalidDirectory(arg)

    with open("vars.json", 'w') as f: json.dump(data, f, indent=4)

def getDir():
    with open("vars.json", 'r') as f: data = json.load(f)
    return data['dir']

def errorMsg(message):
    """Function to print themed error message
       Wrapper Function for print
        Attributes
            msg -- Error Message
            thm -- Error Theme
        """
    with open("vars.json", 'r') as f:
        data = json.load(f)
        print("\033[91m" + message + "\033[0m")
    f.close()

class Verbose:
    """Called if in Verbose mode 2
    prints verbose message
    Attributes
        message -- verbose message to be displayed
    """
    def __init__(self, message):
        self.message = message
        with open("vars.json", 'r') as f:
            data = json.load(f)
            if data['verbose'] == 2: print("\033[33m" + getTime() + " >> " + message + "\033[0m")
        f.close()

class InvalidPage:
    """Raised when invalid page name provided
    Attributes
        page -- page name provided
        deft -- default page
        message -- error message displayed
    """
    def __init__(self, page, deft, message="Invalid Page Name; "):
        self.page = str(page)
        self.deft = str(deft)
        self.message = getTime() + " >> " + message + "'"+self.page+"'" + ", redirecting to page - " + self.deft
        errorMsg(self.message)
class InvalidArgument:
    """Raised when invalid argument provided
        Attributes
            arg -- argument provided
            exp -- expected argument
            message -- error message displayed
        """
    def __init__(self, arg, exp, message="Invalid Argument; "):
        self.arg = str(arg)
        self.exp = exp
        self.message = getTime() + " >> " + message + "'"+self.arg+"'" + ", expected - " + self.exp
        errorMsg(self.message)
class InvalidArgumentCount:
    """Raised when invalid argument count provided
        Attributes
            args -- argument(s) provided
            exp -- expected argument(s)
            message -- error message displayed
        """
    def __init__(self, args, exp, message="Invalid Argument Count; "):
        self.args = str(args)
        self.exp = exp
        self.message = getTime() + " >> " + message + "got - " + self.args + ", expected - " + self.exp
        errorMsg(self.message)
class CommandNotFound:
    """Raised when invalid command name provided
            Attributes
                cmd -- command provided
                message -- error message displayed
            """
    def __init__(self, cmd, message="Command Not Found; "):
        self.cmd = cmd
        self.message = getTime() + " >> " + message + "'"+self.cmd+"'" + " - use [h] or [help] for Help Menu"
        errorMsg(self.message)
class InvalidPort:
    """Raised when invalid port is provided
    Attributes
        port -- port provided
        deft -- default port
        message -- error message displayed
    """
    def __init__(self, port, deft, message="Invalid Port; "):
        self.port = str(port)
        self.deft = str(deft)
        self.message = getTime() + " >> " + message + "'"+self.port+"'" + ", defaulting to port " + "'"+self.deft+"'"
        errorMsg(self.message)
class InvalidVerboseMode:
    """Raised when invalid verbose argument is provided
        Attributes
            mode -- verbose mode provided
            message -- error message displayed
    """
    def __init__(self, mode, message="Invalid Verbose Mode; "):
        self.mode = str(mode)
        self.message = getTime() + " >> " + message + "'"+self.mode+"'" + ", expected - None, -v, -vv"
        errorMsg(self.message)
class InvalidCredentials:
    """Raised during invalid login attempt
        Attributes
            message -- error message displayed
    """
    def __init__(self, message="Invalid Login Credentials; "):
        self.message = getTime() + " >> " + message + "Please try again"
        errorMsg(self.message)
class FileNotFound:
    """Raised when invalid file is provided when using Emu
        Attributes
            file -- file attempted to be opened
            message -- error message displayed
    """
    def __init__(self, file, message="File Not Found; "):
        self.file = str(file)
        self.message = getTime() + " >> " + message + "no such file '"+self.file
        errorMsg(self.message)
class FileReadError:
    """Raised when error occurs reading a file while using Emu
        Attributes
            file -- file attempted to be opened
            message -- error message displayed
    """

    def __init__(self, file, message="File Read Error; "):
        self.file = str(file)
        self.message = getTime() + " >> " + message + "could not read file '"+self.file
        errorMsg(self.message)
class InvalidTheme:
    """Raised when invalid theme name is provided
            Attributes
                theme -- theme attempt to be loaded
                message -- error message displayed
        """

    def __init__(self, theme, message="Invalid Theme; "):
        self.theme = str(theme)
        self.message = getTime() + " >> " + message + "could not find theme " + self.theme
        errorMsg(self.message)
class InvalidDirectory():
    """Raised when invalid directory path is provided
                Attributes
                    dir -- directory path
                    message -- error message displayed
            """

    def __init__(self, dir, message="Invalid Directory; "):
        self.dir = str(dir)
        self.message = getTime() + " >> " + message + "could not find path - " + self.dir
        errorMsg(self.message)
