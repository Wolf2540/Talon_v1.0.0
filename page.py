from rich.console import Console
from rich.table import Table
from settings import *

index = 0

def setPage(args):
    Verbose("VERBOSE: Inside Process Block: page/setPage")
    global index
    index = next((i for i, p in enumerate(pages) if p["name"] == args[0]), None)

    if index is None:
        index = 0
        Verbose("VERBOSE: [ERROR] Bad Page Name Provided: page/setPage")
        InvalidPage(args, getPageName())
    else:
        Verbose("VERBOSE: End Process Block: page/setPage")

def getPageName():
    return pages[index]["name"]

def getPage():
    return "@" + pages[index]["name"] + ": "

def getSym():
    return pages[index]["symbol"]

def listPages():
    Verbose("VERBOSE: Inside Process Block: page/listPages")
    p = Table(title="Pages", box=None, title_style="")
    console = Console()
    p.add_column("", width=2)
    p.add_column("")
    p.add_column("")
    for i in range(0, len(pages)):
        p.add_row(pages[i]["symbol"]+",", pages[i]["name"], pages[i]["desc"])
    console.print(p)
    Verbose("VERBOSE: End Process Block: page/listPages")
