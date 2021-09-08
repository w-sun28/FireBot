#!/usr/bin/python
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import socket
from time import sleep
import time
import board
import busio
import bme280

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)
ads.gain = 2/3
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
GPIO.setmode(GPIO.BCM)

FLIN1 = 6   # Input Pin
FLIN2 = 5   # Input Pin
FLEN = 11    # Enable Pin

FRIN1 = 26    # Input Pin
FRIN2 = 19    # Input Pin
FREN = 13    # Enable Pin

BLIN1 = 27    # Input Pin
BLIN2 = 17    # Input Pin
BLEN = 4    # Enable Pin

BRIN1 = 9    # Input Pin
BRIN2 = 10    # Input Pin
BREN = 22    # Enable Pin

S0 = 24	# Pins for CD74HC4067
S1 = 23
S2 = 18
S3 = 15

Flame = 21	# Pin for flame sensor

AIN1 = 20	# Actuator Motor Driver Pins
AIN2 = 16
AEN = 12

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
GPIO.setup(S0,GPIO.OUT)
GPIO.setup(S1,GPIO.OUT)
GPIO.setup(S2,GPIO.OUT)
GPIO.setup(S3,GPIO.OUT)
GPIO.setup(Flame, GPIO.IN)

pwmFR=GPIO.PWM(FREN,100)
pwmFL=GPIO.PWM(FLEN,100)
pwmBR=GPIO.PWM(BREN,100)
pwmBL=GPIO.PWM(BLEN,100)

pwmFR.start(0)
pwmFL.start(0)
pwmBR.start(0)
pwmBL.start(0)

def mux_read(x1,x2,x3,x4): 
	GPIO.output(S0, x1)
        GPIO.output(S1, x2)
        GPIO.output(S2, x3)
        GPIO.output(S3, x4)
	
(chip_id, chip_version) = bme280.readBME280ID()

#connecting to the sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("169.254.131.2")  #change ip whenever on new network
s.connect((host, 12345))

x_pos = 0
y_pos = 0
throttle = 1  #controls sensitivity of speed
battery = 60 #power multiplier based on max current delivery of battery, 100 = max, 50 = 1/2 power
try:
        while True:
		
		#start_millis = int(round(time.time() * 1000))	#start time of loop - used to delay readings between each dht11/other sensors
		# to control sensor data on index.html
		#index = open("/var/www/index.html").read().format(ExtTemp = '100', humidity = '50', smokeLevel = '1', soundLevel = '12')
		
		t = open("/var/www/top.txt", "w+") #opens file to write thermal data to
	 	b = open("/var/www/bottom.txt", "w+")

		#to control motors with joystick
		msg = s.recv(32)  # recieve up to 32 bytes of data
    		msg = msg.decode("utf-8")  # decode the message
    		if msg[0:5] != "Axis:":  # checking if string is messed up
        		continue
		flag = 0
    		if (msg = firemen presses up on the small joystick button)
			flag = 1
		else if(msg = firemen pressed down on the small joystick button)
			flag = -1
		data = msg.split(" ")
    		axis = data[1]  # axis
    		value = data[3]  # value
    		axis = axis[0:len(axis)-1]  # removing semicolon at end of axis
    		value = value[0:8]  # removing any extraneous text at end of value

		print(value)
		float_value = float(value)

		if(axis == "X"):
			x_pos = round(float_value * battery,-1) 
		elif( axis == "Y"):
			y_pos = round(float_value * battery * round(throttle,2) * -1,-1) 
		elif( axis == "Twist"):  #twist and throttle are oppositely named in pygame library
			throttle = round(((float_value * -1.0) + 1.0) / 2.0, 2) 
		
		print('X == ')
		print(x_pos)
		print('Y == ')
                print(y_pos)
		print('throttle == ')
                print(throttle)

		right_motors = 100
		left_motors = 100

		if(y_pos == 0):
			right_motors = -1 * x_pos
			left_motors = x_pos
		elif(x_pos == 0):
			right_motors = y_pos
			left_motors = y_pos
		elif(x_pos > 0 and y_pos > 0):
			right_motors = y_pos - x_pos / 2
		        left_motors = y_pos
		elif(x_pos < 0 and y_pos > 0):
		        right_motors = y_pos;
		        left_motors = y_pos + x_pos / 2
		elif(x_pos > 0 and y_pos < 0):
		        right_motors = y_pos
		        left_motors = y_pos + x_pos / 2
		elif(x_pos < 0 and y_pos < 0):
		        right_motors = y_pos - x_pos / 2
 		        left_motors = y_pos
			
		#control motors here:
		print('right_motors')
		print(right_motors)
		print('left_motors')
		print(left_motors)
		if(right_motors == 0 and left_motors == 0):
			pwmFR.ChangeDutyCycle(0);
			pwmFL.ChangeDutyCycle(0);
    			pwmBR.ChangeDutyCycle(0);
			pwmBL.ChangeDutyCycle(0);
		
		if(right_motors > 0 and left_motors > 0):
			GPIO.output(FRIN1,0)
			GPIO.output(FRIN2,1)
			pwmFR.ChangeDutyCycle(right_motors)
			GPIO.output(FLIN1,0)
		        GPIO.output(FLIN2,1)
			pwmFL.ChangeDutyCycle(left_motors)
                        GPIO.output(BRIN1,0)
                        GPIO.output(BRIN2,1)
                        pwmBR.ChangeDutyCycle(right_motors)
			GPIO.output(BLIN1,0)
                        GPIO.output(BLIN2,1)
       		        pwmBL.ChangeDutyCycle(left_motors)
		
		if(right_motors < 0 and left_motors > 0):
		        GPIO.output(FRIN1,0)
                        GPIO.output(FRIN2,1)
                        pwmFR.ChangeDutyCycle(-1 * right_motors)
                        GPIO.output(FLIN1,1)
                        GPIO.output(FLIN2,0)
                        pwmFL.ChangeDutyCycle(left_motors)
                        GPIO.output(BRIN1,1)
                        GPIO.output(BRIN2,0)
                        pwmBR.ChangeDutyCycle(-1 * right_motors)
                        GPIO.output(BLIN1,0)
                        GPIO.output(BLIN2,1)
                        pwmBL.ChangeDutyCycle(left_motors)

		if(right_motors < 0 and left_motors < 0):
                        GPIO.output(FRIN1,1)
                        GPIO.output(FRIN2,0)
                        pwmFR.ChangeDutyCycle(-1 * right_motors)
                        GPIO.output(FLIN1,1)
                        GPIO.output(FLIN2,0)
                        pwmFL.ChangeDutyCycle(-1 * left_motors)
                        GPIO.output(BRIN1,1)
                        GPIO.output(BRIN2,0)
                        pwmBR.ChangeDutyCycle(-1 * right_motors)
                        GPIO.output(BLIN1,1)
                        GPIO.output(BLIN2,0)
                        pwmBL.ChangeDutyCycle(-1 * left_motors)
		
		if(right_motors > 0 and left_motors < 0):
                        GPIO.output(FRIN1,1)
                        GPIO.output(FRIN2,0)
                        pwmFR.ChangeDutyCycle(right_motors)
                        GPIO.output(FLIN1,0)
                        GPIO.output(FLIN2,1)
                        pwmFL.ChangeDutyCycle(-1 * left_motors)
                        GPIO.output(BRIN1,0)
                        GPIO.output(BRIN2,1)
                        pwmBR.ChangeDutyCycle(right_motors)
                        GPIO.output(BLIN1,1)
                        GPIO.output(BLIN2,0)
                        pwmBL.ChangeDutyCycle(-1 * left_motors)
		
		if(flag = 0)
                        GPIO.output(AEN, 0)
                        GPIO.output(AIN1, 0)
                        GPIO.output(AIN2, 0)
		        
		if(flag = 1)
			GPIO.output(AEN, 1)
			GPIO.output(AIN1, 1)
			GPIO.output(AIN2, 0)

		if(flag = -1)
                        GPIO.output(AEN, 1)
                        GPIO.output(AIN1, 0)
                        GPIO.output(AIN2, 1)

		if((int(round(time.time() * 1000)) - start_millis) > 500):
			mux_read(0,0,0,0)
			CO = str(chan1.voltage)
                        mux_read(1,0,0,0)
			CO2 = str(chan1.voltage)
                        mux_read(0,1,0,0)
			LPG = str(chan1.voltage)
                        mux_read(1,1,0,0)
			AM = str(chan1.voltage)
                        mux_read(0,0,1,0)
			H2 = str(chan1.voltage)
                        mux_read(1,0,1,0)
			MTH = str(chan1.voltage)
                        mux_read(0,1,1,0)
			SMK = str(chan1.voltage)
			mux_read(0,0,0,0)
			ext_temp = str(1/((1/298.15) + (1/3380) * math.log(32767/chan2.value)-1))								
			temperature,pressure,humidity = bme280.readBME280All()
			int_temp = str(temperature)
			humidity2 = str(humidity) 
			if(GPIO.input(Flame) == 1)
				flame = 'Fire is Present'
			else if(GPIO.input(Flame) == 0)
				flame = 'No Fire Present'
			Latitude = '32.730535'
			Longitude = '97.108131'
			top_string = "CO Level = " + CO + " CO Level = " + CO + " CO2 Level = " + CO2 + " Ammonium Sulfide Level = " + AM + " Hydrogen Gas Level = " + H2 + " Methane Level = " + MTH + " Smoke Level = " + SMK 
			bottom_string = "Internal Temperature = " + int_temp + " Humidity = " + humidity2 + " External Temperature = " + ext_temp + " " + flame + " Latitude = " +  Latitude + " Longitude = " + Longitude
			t.write(top_string)
			b.write(bottom_string)

		start_millis = int(round(time.time() * 1000))

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
        print "STOP"
        pwmFR.stop()
	pwmFL.stop()
	pwmBR.stop()
	pwmBL.stop()
  	t.close()
	b.close()
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

