import paho.mqtt.client as mqtt
import time

broker_address="10.0.0.179" #broker address (your pis ip address)

# booleans to keep track of whether the button has been pressed and whether the LED is currently on
buttonstate = False
ledOn = False

client = mqtt.Client() #create new mqtt client instance

client.connect(broker_address) #connect to broker

client.loop_start() #start client

while True:
	buttonstate = GPIO.input(17)

	# turn LED on if the button is pressed and the LED is off
	if buttonstate == 1 and ledOn == 0:
		client.publish("/led","on") #send message
		time.sleep(.2)
		ledOn = True
	
	# keep LED if it is already on and the button isn't being pressed
	elif buttonstate == 0 and ledOn == 1:
		client.publish("/led","on") #send message
		time.sleep(.2)
	
	# turn LED off otherwise
	else:
		client.publish("/led","off") #send message
		time.sleep(.2)
		ledOn = False

client.loop_stop() #stop client