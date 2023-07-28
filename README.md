# pylogix_cli

The pylogix_cli application is intended to encaspulate all of the pylogix commands into a single directly executable program.  Using pyinstaller, pylogix_cli can be packaged into an .exe file that can be run on any Windows computer without the need for installing Python.  This can be particularly
handy for systems where an end-user does not have the Rockwell software, but needs to update a value, set the time on the controller or read or write settings from or to the target PLC.

Warning!  PLCs control industrial equipment and writing values to a PLC that is actively operating equipment should be done with great care and is at your own risk.

Click below to download the current standalone executable for Windows 7/10:<br/>
https://github.com/dhunt84971/pylogix_cli/releases/download/v0.1.3/pylogix_cli.exe 


Execution of the application will take the form of a single command or a shell console application allowing multiple commands to be executed.

## Examples of Usage
Single command syntax example:
```
pylogix_cli 192.168.1.10 Read CurrentScreen
None 12 Success
```
![Peek 2022-04-18 15-17](https://user-images.githubusercontent.com/674065/163863258-3edac336-dc3b-4469-b1a2-660256805834.gif)


Console app example:
```
pylogix_cli 192.168.1.10
pylogix_cli> Read CurrentScreen
None 12 Success
pylogix_cli> quit
```

OR
```
pylogix_cli
pylogix_cli> Read CurrentScreen
ERROR - No IPAddress specified.  Use IPAddress command.
pylogix_cli> IPAddress 192.168.1.10
pylogix_cli> Read CurrentScreen
None 12 Success
pylogix_cli> quit
```
![Peek 2022-04-18 15-13](https://user-images.githubusercontent.com/674065/163862795-0810d192-76c8-40b5-a798-819640d2ef5f.gif)



## The pylogix Project
This application is a command line wrapper to ease the use of the many functions of the pylogix library.  The pyinstaller program is used to create an executable package on Windows that does not require the installation of Python.

For more information and documentation:
https://github.com/dmroeder/pylogix

**Special thanks to dmroeder and all the contributors that make pylogix possible.**

## Currently Implemented Functions
```
        Help                        - Displays this list of commands.
        IPAddress <ip address>      - Sets the IP address for the target PLC.
        Quit                        - Leave console application.
        GetPLCTime                  - Returns the PLC time.
        SetPLCTime                  - Sets the PLC time to the current time.
        GetModuleProperties <slot>  - Gets the properties of the module in the specified slot.
        GetDeviceProperties         - Gets the properties of the connected device.
        * GetFaultCodes             - Gets the Type and Code of the current controller fault.
        Read <tag>                  - Returns the specified tag's value from the target PLC.
        Write <tag> <value>         - Sets the specified tag's value in the target PLC.
        Version                     - Returns the version of pylogix_cli and pylogix.
        GetTagList                  - Returns the list of tags in the target PLC.
        Output (Raw | Readable)     - Sets the output format.  Raw is the default.     

* - Is not a standard pylogix command.
```
(Commands are not case sensitive.)



## Development Environment
In order to build the executable using pyinstaller, first clone this repository and then install both pylogix and pyinstaller using pip.

```
git clone https://github.com/dhunt84971/pylogix_cli.git
cd pylogix_cli
pip install pylogix
pip install pyinstaller
```

### Building the Executable
In order to build the executable for the Windows platform it is necessary to run pyinstaller on a Windows computer.  Keep in mind that Python 3.9+ cannot run on Windows 7.  For this reason it is recommended that a Windows 7 system with Python installed be used to create the executable in order to ensure compatability with Windows 7 and newer versions of Windows.
 
```
pyinstaller -F pylogix_cli.py
```

## License

This project is licensed under Apache 2.0 License - see the [LICENSE](LICENSE.txt) file for details.

