from commands import Clear, Home
from page import *   # grants access to errors, settings, and pages
import parser


def getInput(time):
    with open('vars.json', 'r') as f: data = json.load(f)
    prefix = "\033[33m" + time + " >> " + "\033[91m" + str(data['username']) + getPage() + "\033[32m" + getDir() + "\033[0m:-" + getSym() + " "
    return input(prefix)


def run():
    Clear(); Home()
    while True:
        parser.Parse(getSym() + getInput(getTime()))
