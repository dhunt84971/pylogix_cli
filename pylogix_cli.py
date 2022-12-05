
'''
The pylogix_cli application is intended to encaspulate all of the pylogix 
commands into a single directly executable program.  Using pyinstaller,
pylogix_cli can be packaged into an .exe file that can be run on any Windows
computer without the need for installing Python.  This can be particularly
handy for systems where an end-user does not have the Rockwell software, but
needs to update a value, set the time on the controller or read or write
settings from or to the target PLC.

Execution of the application will take the form of a single command or a shell
console application allowing multiple commands to be executed.

Single command syntax:
pylogix_cli 192.168.1.10 Read CurrentScreen

Console app example:
pylogix_cli 192.168.1.10
> Read CurrentScreen
12
> quit

- or -

pylogix_cli
> Read CurrentScreen
ERROR - No IPAdress specified.  Use IPAddress command.
> IPAddress 192.168.1.10
> Read CurrentScreen
12
> quit

'''

'''
the following import is only necessary because eip.py is not in this directory
'''
import sys
import pylogix

#sys.path.append('..')

from pylogix import PLC
version = "0.1.1"
comm = PLC()

#region CONSOLE COMMAND DEFINITIONS
def ipAddress(args):
    comm.Close()
    comm.IPAddress = args

def getPLCTime(args):
    ret = comm.GetPLCTime()
    print(ret)

def setPLCTime(args):
    ret = comm.SetPLCTime()
    print(ret)

def getDeviceProperties(args):
    ret = comm.GetDeviceProperties()
    print(ret)

def getModuleProperties(args):
    ret = comm.GetModuleProperties(args)
    print(ret)

def read(args):
    ret = comm.Read(args)
    print(ret)

def write(args):
    words = args.split()
    comm.Read(words[0])  # Always read the tag first since this will initiate the connection.
    ret = comm.Write(words[0], words[1])
    print(ret)

def getVersion(args):
    print("pylogix_cli v" + version + ", pylogix v" + pylogix.__version__)

def getTagList(args):
    tags = comm.GetTagList()
    for tag in tags.Value:
        print(tag.TagName, tag.DataType)

def validateTags(args):
    fileName = args
    with open(fileName, encoding="utf-8") as f:
        for line in f:
            ret = comm.Read(line)
            print(ret)

def getHelp(args):
    print('''
    Commands: (Not case sensitive.)
        Help                        - Displays this list of commands.
        IPAddress <ip address>      - Sets the IP address for the target PLC.
        Quit                        - Leave console application.
        GetPLCTime                  - Returns the PLC time.
        SetPLCTime                  - Sets the PLC time to the current time.
        GetModuleProperties <slot>code  - Gets the properties of the module in the specified slot.
        GetDeviceProperties         - Gets the properties of the connected device.
        Read <tag>                  - Returns the specified tag's value from the target PLC.
        Write <tag> <value>         - Sets the specified tag's value in the target PLC.
        Version                     - Returns the version of pylogix_cli and pylogix.
        GetTagList                  - Returns the list of tags in the target PLC.
    ''')

#endregion CONSOLE COMMAND DEFINITIONS

#region COMMAND LOOP
def parseCommand(command):
    words = command.casefold().split()
    if (len(words) > 0):
        if (words[0] == "help"):
            getHelp(command)
        elif (words[0] == "ipaddress"):
            ipAddress(words[1])
        elif (words[0] == "getplctime"):
            getPLCTime(getAdditionalArgs(command))
        elif (words[0] == "setplctime"):
            setPLCTime(getAdditionalArgs(command))
        elif (words[0] == "getdeviceproperties"):
            getDeviceProperties(getAdditionalArgs(command))
        elif (words[0] == "getmoduleproperties"):
            getModuleProperties(getAdditionalArgs(command))
        elif (words[0] == "read"):
            read(getAdditionalArgs(command))
        elif (words[0] == "write"):
            write(getAdditionalArgs(command))
        elif (words[0] == "version"):
            getVersion(getAdditionalArgs(command))
        elif (words[0] == "gettaglist"):
            getTagList(getAdditionalArgs(command))
        else:
            print("ERROR - Unrecognized command.  Enter Help for a list of commands.")

def commandLoop():
    command = input("pylogix_cli> ").casefold()
    while (command != "quit"):
        parseCommand(command)
        command = input("pylogix_cli> ").casefold()

#endregion COMMAND LOOP

#region HELPER FUNCTIONS
def isIPAddress(value):
    return len(value.split(".")) == 4

def getAdditionalArgs(command):
    words = command.casefold().split()
    if (len(words) > 1):
        return " ".join(words[1:])
    else:
        return ""
#endregion HELPER FUNCTIONS

#region MAIN
def main():
    arguments = sys.argv
    if (len(arguments) > 1):
        if (isIPAddress(arguments[1])):
            comm.IPAddress = arguments[1]
            if (len(arguments) > 2):
                parseCommand(" ".join(arguments[2:]))
            else:
                commandLoop()
    else:
        commandLoop()
    comm.Close()

#endregion MAIN

main()
