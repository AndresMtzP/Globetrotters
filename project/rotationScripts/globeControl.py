import sys

def globeControl(command):

    with open('/home/pi/globe/Rotation/commands', 'w') as f:
        f.write(command)