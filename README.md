# broadcast_sender_receiver


A set of systems enabling communication and improving the work of teachers during remote classes with the use of virtual machines.

## Related work
This project is part of the VirtuaLab system, which enables conducting remote classes at technical universities with the use of virtual machines.
Link to VirtuaLab project:
https://github.com/NiNJAxFREEZu/virtualab

## How it works
All virtual machines created for laboratories should be in one internal network.
student_main.py and activity.py should start with system on every virtual machine and work in background.
communicator_main.py and professor_main.py are responsible for activating the communicator and the professor panel, respectively.


## Dependencies
- PyQt5
- xdotool
- libnotify-bin
- net-tools
