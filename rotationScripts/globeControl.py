import sys

def globeControl(command):

    with open('commands.txt', 'w') as f:
        f.write(command)