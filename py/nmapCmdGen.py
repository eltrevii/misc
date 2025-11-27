'''
DESCRIPTION
    this script generates a command line to scan for open ports,
    depending on the ip address and port to scan

REQUIREMENTS
    rich
'''

##################################################
# GETCH IMPLEMENTATION
##################################################
class _Getch:
    """Gets a single character from standard input.
    Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
##################################################

from rich import print as rprint
from rich.prompt import Prompt

import os

debug = True

def clear(): os.system("cls") if os.name == "nt" else os.system("clear")

def dbgPrint(*args, **kwargs):
    if debug == True:
        print("[dim]", *args, **kwargs)

noEndPrint = lambda msg: rprint(msg, end='', flush=True)

def yesNo(msg):
    noEndPrint("[yellow]msg (y/n) [dim]\\[y]: ")
    while True:
        ynAns = getch().decode("UTF-8")
        match ynAns:
            case 'y':
                rprint("y")
                return True
            case 'n':
                rprint("n")
                return False
            case _:
                dbgPrint("pressed key " + ynAns)

def main():
    clear()
    rprint("[blue]ENTER RANGE (like 192.168.1.0/24 or 192.168.1.*)")
    ipRange = Prompt.ask("[yellow]RANGE")
    ipRangeSplit = ipRange.split(":")
    if len(ipRangeSplit) < 2:
        ipPort  = Prompt.ask("[yellow]PORT ")
    else:
        ipRange = ipRangeSplit[0]
        ipPort  = ipRangeSplit[1]
    scanCommand = f"nmap -oG - -p {ipPort} --open {ipRange}"
    rprint(f"[green]COMMAND: {scanCommand}")
    doExecute = Prompt.ask("\n[yellow]EXECUTE?", choices=['y', 'n'], default='y', case_sensitive=False)
    if doExecute == 'y':
        clear()
        rprint("[yellow]RUNNING COMMAND\nCTRL-C TO STOP\n")
        os.system(scanCommand)

if __name__=="__main__":
    main()