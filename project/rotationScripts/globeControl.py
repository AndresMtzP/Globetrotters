import sys

def globeControl(command):

    with open('commands', 'w') as f:
        f.write(command)