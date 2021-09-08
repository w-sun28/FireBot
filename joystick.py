#OLD OLD
# NOTE: This script requires the following Python modules:
#  pyserial - http://pyserial.sourceforge.net/ pygame - http://www.pygame.org/ Win32 users may also need: pywin32 - 
#  http://sourceforge.net/projects/pywin32/
#
import signal 
import sys 
import threading 
import signal 
import serial 
import pygame

# allow multiple joysticks
joy = []

# Arduino USB port address (try "COM5" on Win32) 
#usbport = "/dev/tty.usbmodem641" 

# define usb serial connection to Arduino ser = 
#serial.Serial(usbport, 9600)

# handle joystick event
def handleJoyEvent(e):
    if e.type == pygame.JOYAXISMOTION:
        axis = "unknown"
        if (e.dict['axis'] == 0):
            axis = "X"
        if (e.dict['axis'] == 1):
            axis = "Y"
        if (e.dict['axis'] == 2):
            axis = "Twist"
        if (e.dict['axis'] == 3):
            axis = "Throttle"
        if (e.dict['axis'] == 4):
            axis = "Camera 2"
        if (e.dict['axis'] == 5):
            axis = "Camera 1"
        if (e.dict['axis'] == 6):
            axis = "Slide"
        print(axis)
        if (axis != "unknown"):
            str = "Axis: %s; Value: %f" % (axis, e.dict['value'])
            # uncomment to debug
            output(str, e.dict['joy'])
    elif e.type == pygame.JOYBUTTONDOWN:
        str = "Button: %d" % (e.dict['button'])
        # uncomment to debug
        output(str, e.dict['joy'])
        # Button 0 (trigger) to quit
        if (e.dict['button'] == 11):
            print ("Bye!\n")
            exit()
    else:
        pass

# print the joystick position
def output(line, stick):
    print (stick, line)
    print(" ")
    print(" ")
# wait for joystick input
def joystickControl():
    while True:
        e = pygame.event.wait()
        print (e)
        if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN):
            handleJoyEvent(e)

# main method
def main():
    # initialize pygame
    pygame.joystick.init()
    pygame.display.init()
    if not pygame.joystick.get_count():
        print ("\nPlease connect a joystick and run again.\n")
        quit()
    print ("\n%d joystick(s) detected." % pygame.joystick.get_count())
    for i in range(pygame.joystick.get_count()):
        myjoy = pygame.joystick.Joystick(i)
        myjoy.init()
        joy.append(myjoy)
        #print ("Joystick %d: " % (i) + joy[i].get_name())
    print ("Depress trigger (button 0) to quit.\n")
    # run joystick listener loop
    joystickControl()

# allow use as a module or standalone script
if __name__ == "__main__":
    main()
