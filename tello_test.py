from tello import Tello
import sys
from datetime import datetime
import time
from os.path import join, dirname, realpath

start_time = str(datetime.now())


#def getFileName(s):
#    global file_name
#    file_name = s

def runCommands(commands):

    tello = Tello()
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()

            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print ('delay %s' % sec)
                time.sleep(sec)
                pass
            else:
                print(command)
                tello.send_command(command)

    log = tello.get_log()

    name_dir = 'log'

    log_name = start_time.replace(':', '-')

    file_path = join(dirname(realpath(__file__)),'log\\', log_name + '.txt')

    out = open(file_path, 'w+')
    for stat in log:
        stat.print_stats()
        str = stat.return_stats()
        out.write(str)
    out.close()
