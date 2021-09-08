import RPi.GPIO as GPIO
from time import sleep
import time
import curses

GPIO.setmode(GPIO.BCM)

FLIN1 = 24   # Input Pin
FLIN2 = 23   # Input Pin
FLEN = 18    # Enable Pin

FRIN1 = 25    # Input Pin
FRIN2 = 8    # Input Pin
FREN = 7    # Enable Pin

BLIN1 = 16    # Input Pin
BLIN2 = 20    # Input Pin
BLEN = 12    # Enable Pin

BRIN1 = 19    # Input Pin
BRIN2 = 21    # Input Pin
BREN = 26    # Enable Pin

i = 5
GPIO.setup(FLIN1,GPIO.OUT)
GPIO.setup(FLIN2,GPIO.OUT)
GPIO.setup(FLEN,GPIO.OUT)
GPIO.setup(FRIN1,GPIO.OUT)
GPIO.setup(FRIN2,GPIO.OUT)
GPIO.setup(FREN,GPIO.OUT)
GPIO.setup(BLIN1,GPIO.OUT)
GPIO.setup(BLIN2,GPIO.OUT)
GPIO.setup(BLEN,GPIO.OUT)
GPIO.setup(BRIN1,GPIO.OUT)
GPIO.setup(BRIN2,GPIO.OUT)
GPIO.setup(BREN,GPIO.OUT)

pwmFR=GPIO.PWM(FREN,100)
pwmFL=GPIO.PWM(FLEN,100)
pwmBR=GPIO.PWM(BREN,100)
pwmBL=GPIO.PWM(BLEN,100)

pwmFR.start(0)
pwmFL.start(0)
pwmBR.start(0)
pwmBL.start(0)

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
speed=0
def motorspeed(num1,num2,num3,num4):
        global i
        global speed
        pwmFR.ChangeDutyCycle(speed)
        pwmFL.ChangeDutyCycle(speed)
	pwmBR.ChangeDutyCycle(speed)
	pwmBL.ChangeDutyCycle(speed)
        GPIO.output(FRIN1,num1)
        GPIO.output(FRIN2,abs(num1 - 1))
	GPIO.output(FLIN1,num2)
        GPIO.output(FLIN2,abs(num2-1))
	GPIO.output(BRIN1,num3)
        GPIO.output(BRIN2,abs(num3 - 1))
	GPIO.output(BLIN1,num4)
        GPIO.output(BLIN2,abs(num4 - 1))

try:
        while True:
                char = screen.getch()
                if char == ord('q'):
                        break
                elif char == curses.KEY_UP:
                        motorspeed(0, 0, 0, 0)
			print('Forward')
                elif char == curses.KEY_DOWN:
                        motorspeed(1, 1, 1, 1)
			print('Back')
                elif char == curses.KEY_RIGHT:
                        motorspeed(1, 0, 1, 0)
			print('Right')
                elif char == curses.KEY_LEFT:
                        motorspeed(1, 0, 0, 1)
			print('Left')
                elif char == ord('x'):
                        GPIO.output(FRIN1,False)
        		GPIO.output(FRIN2,False)
        		GPIO.output(FREN,False)
        		GPIO.output(FLIN1,False)
       		 	GPIO.output(FLIN2,False)
        		GPIO.output(FLEN,False)
        		GPIO.output(BRIN1,False)
        		GPIO.output(BRIN2,False)
        		GPIO.output(BREN,False)
       		 	GPIO.output(BLIN1,False)
        		GPIO.output(BLIN2,False)
        		GPIO.output(BLEN,False)
                elif char == ord('w'):
                        speed+=10
                        if speed>100:
                                speed=100
			print(speed)
                elif char == ord('s'):
                        speed-=10
                        if speed<0:
                                speed=0
			print(speed)
except KeyboardInterrupt:
        pass
finally:
        GPIO.output(FRIN1,False)
        GPIO.output(FRIN2,False)
        GPIO.output(FREN,False)
        GPIO.output(FLIN1,False)
        GPIO.output(FLIN2,False)
        GPIO.output(FLEN,False)
	GPIO.output(BRIN1,False)
        GPIO.output(BRIN2,False)
        GPIO.output(BREN,False)
	GPIO.output(BLIN1,False)
        GPIO.output(BLIN2,False)
        GPIO.output(BLEN,False)
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()
        print "STOP"
        pwmFR.stop()
	pwmFL.stop()
	pwmBR.stop()
	pwmBL.stop()
        GPIO.cleanup()























#link = "http://169.254.131.2/firebot/" #link of webserver hosted on will's laptop 
#f = urllib.request.urlopen(link) #opens link to webserver
#myfile = f.read(); #myfile contains the contents of webserver

#g = open("/var/www/index.html", 'w'); #opens index.html file

#message = """<script>
#intTemp = 1000;
#</script>"""

# g.write(message) #writes message to index.html
#g.close()

