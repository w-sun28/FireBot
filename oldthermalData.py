#work without numpy, bc we cannot download numpy
import time
import busio
import board
import adafruit_amg88xx
import pickle

 
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

#shared = {"arr":amg.pixels}
#fp = open("shared.pkl", 'wb') #pickle to share amg.pixels array

#f = open("data.txt", "w+") #opens file to write thermal data to


while True:
	f = open("/var/www/thermalData.txt", "w+") #opens file to write thermal data to
	#fp = open("shared.pkl", 'wb') #pickle to share amg.pixels array
	#pickle.dump(amg.pixels, fp, protocol=2)
	for row in amg.pixels:
		#print(['{0:.1f}'.format(temp) for temp in row])
		#print("")
		for temp in row:
			f.write('{0:.1f}'.format(temp))
			f.write(" ")
        	# Pad to 1 decimal place
        	#f.write(['{0:.1f}'.format(temp) for temp in row])
        	#f.write("")
		f.write("\n")
	f.write("\n")
	#print("\n")
	f.close()
	time.sleep(1)


