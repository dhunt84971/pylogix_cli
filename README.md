# pylogix_cli

The pylogix_cli application is intended to encaspulate all of the pylogix commands into a single directly executable program.  Using pyinstaller, pylogix_cli can be packaged into an .exe file that can be run on any Windows computer without the need for installing Python.  This can be particularly
handy for systems where an end-user does not have the Rockwell software, but needs to update a value, set the time on the controller or read or write settings from or to the target PLC.

Execution of the application will take the form of a single command or a shell console application allowing multiple commands to be executed.

## Examples of Usage
Single command syntax:
```
pylogix_cli 192.168.1.10 Read CurrentScreen
```

Console app example:
```
pylogix_cli 192.168.1.10
> Read CurrentScreen
12
> .quit
```

- or -
```
pylogix_cli
> Read CurrentScreen
ERROR - No IPAdress specified.  Use IPAddress command.
> IPAddress 192.168.1.10
> Read CurrentScreen
12
> .quit
```

## The pylogix Project
This application is a command line wrapper to ease the use of the many functions of the pylogix library.  The pyinstaller program is used to create an executable package on Windows that does not require the installation of Python.

## Development Environment
In order to build the executable using pyinstaller clone this repository and install both pylogix and pyinstaller using pip.

```
pip install pylogix
pip install pyinstaller
```

### Building the Executable
In order to build the executable for a the Windows platform it is necessary to run pyinstaller on a Windows computer.  Keep in mind that Python 3.9+ cannot run on Windows 7.  For this reason it is recommended that a Windows 7 system with Python installed be used to create the executable in order to ensure compatability with Windows 7 and newer versions of Windows.
 
```
pyinstaller -F pylogix_cli.py
```

## License

This project is licensed under Apache 2.0 License - see the [LICENSE](LICENSE.txt) file for details.

