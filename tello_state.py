from re import T
import socket
import re
from time import sleep
import math
#import curses
import heading_diff
from threading import Thread
import tello_test

INTERVAL = 0.1

thread_running = True    
x = 0
y = 0
z = 0
yaw = 0
start_yaw = 0
tmp_1 = 0
diff = 0
pitch = 0
tas_x = 0
tas_z = 0
vx = 0
vz = 0
test = 0
angle = 0
diff = 0

def numbers(s):
    return int(re.search(r"-?\d+", s).group(0))

def loop():
    tello_ip = '192.168.10.1'
    tello_port = 8889
    tello_adderss = (tello_ip, tello_port)

    socket.sendto('command'.encode('utf-8'), tello_adderss)
    
    try:
        index = 0
        global yaw
        global thread_running
        while thread_running:
            index += 1
            response, ip = socket.recvfrom(1024)
            if response == 'ok':
                continue
            response = response.decode('utf-8')
            out = response.replace(';', ';\n')
            out = 'Tello State:\n' + out
            telemetry_list = response.split(";")

            global start_yaw
            if index == 1:
                start_yaw = numbers(telemetry_list[2])
                if(start_yaw < 0):
                    start_yaw = 360 + start_yaw
                # for c in telemetry_list[2]:
                #     if c.isdigit():
                #         start_yaw = start_yaw + int(c)

            global pitch
            pitch = -1 * numbers(telemetry_list[0])
            ## With the code below, we only parse the last digit of numbers larger than 9 -> pitch:10 gets parsed into pitch:0
            ## Why do we keep adding to pitch? For each run through we'll get a pitch which just keeps on rising which we don't want (?)
            # for c in telemetry_list[0]:
            #     if c.isdigit():
            #         pitch = pitch + int(c)
                    
            global vx
            vx = numbers(telemetry_list[3])
            # vx = 0
            # for c in telemetry_list[3]:
            #     if c.isdigit():
            #         vx = vx + int(c)

            global vz
            vz = numbers(telemetry_list[5])
            # vz = 0
            # for c in telemetry_list[5]:
            #     if c.isdigit():
            #         vz = vz + int(c)

            global tas_x
            global tas_z
            tas_x = (vx * math.cos(math.radians(pitch)) - (vz * math.sin(math.radians(pitch))))
            tas_z = (vx * math.sin(math.radians(pitch)) + (vz * math.cos(math.radians(pitch))))

            global test
            if tas_x > 5:
                if test == 0:
                    # global yaw
                    yaw = numbers(telemetry_list[2])
                    if(yaw < 0 ):
                        yaw = 360 + yaw
                    # yaw = 0
                    # for c in telemetry_list[2]:
                    #   if c.isdigit():
                    #     yaw = yaw + int(c)
                    test += 1
            else:
                test = 0
                global tmp_1
                # tmp_1 = 0

                tmp_1 = numbers(telemetry_list[2])
                # for c in telemetry_list[2]:
                #     if c.isdigit():
                #         tmp_1 = tmp_1 + int(c)
                if(tmp_1 < 0):
                    tmp_1 = 360 + tmp_1
                global diff
                print("TEMP RIKTING", tmp_1)
                diff = heading_diff.getHeadingDiff(yaw, tmp_1)
                global angle
                angle = 180 - diff
                if angle < 0:
                    raise ArithmeticError
            
            global tmp_x
            global tmp_z
            global tmp_y

            tmp_x = (tas_x * INTERVAL) * math.sin(diff)
            tmp_y = (tas_x * INTERVAL) * math.cos(diff)
            tmp_z = tas_z * INTERVAL
            if diff < 0:
                tmp_x * -1
            if abs(diff) > 90:
                tmp_y * -1 

            global x
            global y
            global z

            x += tmp_x
            y += tmp_y
            z += tmp_z
 
                        

            #print(out)

            print(x)
            print(y)
            print(z)
            print("RIKTING", yaw)
          #  report(out)
            sleep(INTERVAL)
    except KeyboardInterrupt:
        print("interupted")

def input_abort():
    usr_input = input()
    print("Aborted")




#def report(str):
  #  stdscr.addstr(0, 0, str)
  #  stdscr.refresh()

if __name__ == "__main__":
  #  stdscr = curses.initscr()
  # curses.noecho()
  #  curses.cbreak()

    local_ip = ''
    local_port = 8890
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
    socket.bind((local_ip, local_port))

    t1 =  Thread(target=loop)
    t2 = Thread(target=input_abort)

    t1.start()
    t2.start()

    t2.join()
    thread_running = False

    f = open("command.txt", "w+")

   # global x
   # global y
   # global start_yaw, yaw
    print("TEST", x, y, start_yaw, yaw)
    distance = math.sqrt(int(math.pow(x, 2) + int(math.pow(y, 2)))) 

    final_diff = heading_diff.getHeadingDiff(start_yaw, yaw)

    if final_diff < 0:
        final_diff = abs(final_diff)
        rotate = f"ccw %s" %final_diff
    else:
        rotate = f"cw %s" %final_diff
    
    
    f.write(rotate + "\n" )

    str_forward = f"forward %s" %distance

    f.write(str_forward + "\n")

    f.write("land")

    f.close()

    commands = [rotate, str_forward, "land"]

    tello_test.runCommands(commands)
