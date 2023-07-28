
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
from pylogix.lgx_response import Response
from struct import pack, unpack_from

#sys.path.append('..')

from pylogix import PLC
version = "0.1.3"
comm = PLC()
output_format = "raw"
output_formats = ["raw", "readable", "minimal"]

#region CUSTOM COMMAND CODE
"""
Credit to dmroeder. https://github.com/dmroeder
"""
def get_controller_fault(plc):
    """
    User configurable CIP command.  It is up to you to understand the
    data that will be returned
    
    returns Response class (.TagName, .Value, .Status
    """
    conn = plc.conn.connect(True)
    if not conn[0]:
        return Response(None, None, conn[1])

    cip_service = 0x01
    cip_service_size = 0x02
    cip_class_type = 0x20
    cip_class = 0x73
    cip_instance_type = 0x24
    cip_instance = 0x01

    request = pack('<BBBBBB',
                    cip_service,
                    cip_service_size,
                    cip_class_type,
                    cip_class,
                    cip_instance_type,
                    cip_instance)

    status, ret_data = plc.conn.send(request, False)

    if status == 0:
        data = ret_data[44:]
        major = unpack_from("<H", data, 20)[0]
        minor = unpack_from("<H", data, 22)[0]
    else:
        major = None
        minor = None

    return Response(None, (major, minor), status)


#endregion CUSTOM COMMAND CODE

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
    if not args.isnumeric():
        print("ERROR - Invalid argument.  Please specify a slot number.")
        return
    ret = comm.GetModuleProperties(int(args))
    print(ret)

def getFaultCodes(args):
    ret = get_controller_fault(comm)
    if (output_format == "raw"):
        print(ret)
    elif (output_format == "readable"):
        print("Fault Type({}), Code({})".format(ret.Value[0], ret.Value[1]))
    else:
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

def output(args):
    global output_format
    if (args in output_formats):
        output_format = args
        print("Output format set to {}".format(args))
    else:
        print("Invalid output format")
    return

def getHelp(args):
    print('''
    Commands: (Not case sensitive.)
        Help                        - Displays this list of commands.
        IPAddress <ip address>      - Sets the IP address for the target PLC.
        Quit                        - Leave console application.
        GetPLCTime                  - Returns the PLC time.
        SetPLCTime                  - Sets the PLC time to the current time.
        GetModuleProperties <slot>  - Gets the properties of the module in the specified slot.
        GetDeviceProperties         - Gets the properties of the connected device.
        GetFaultCodes               - Gets the Type and Code of the current controller fault.
        Read <tag>                  - Returns the specified tag's value from the target PLC.
        Write <tag> <value>         - Sets the specified tag's value in the target PLC.
        Version                     - Returns the version of pylogix_cli and pylogix.
        GetTagList                  - Returns the list of tags in the target PLC.
        Output (Raw | Readable)     - Sets the output format.  Raw is the default.        
          
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
        elif (words[0] == "getfaultcodes"):
            getFaultCodes(getAdditionalArgs(command))
        elif (words[0] == "read"):
            read(getAdditionalArgs(command))
        elif (words[0] == "write"):
            write(getAdditionalArgs(command))
        elif (words[0] == "version"):
            getVersion(getAdditionalArgs(command))
        elif (words[0] == "gettaglist"):
            getTagList(getAdditionalArgs(command))
        elif (words[0] == "output"):
            output(getAdditionalArgs(command))
        else:
            print("ERROR - Unrecognized command.  Enter Help for a list of commands.")

def commandLoop():
    command = input("pylogix_cli> ").casefold()
    while (command != "quit" and command != "exit"):
        parseCommand(command)
        command = input("pylogix_cli> ").casefold()
    if command == "exit":
        print("I'll assume you meant quit.")

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
