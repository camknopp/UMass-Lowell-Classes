"""
receive light sensor values from esp through mqtt and store in influxdb

"""

from flask import Flask, request, json
from flask_restful import Resource, Api
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from influxdb import InfluxDBClient
import datetime


broker_address = "10.0.0.179"  # broker address (your pis ip address)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)
dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')
client = mqtt.Client()  # create new client instance
client.connect(broker_address)  # connect to broker


client.subscribe("/led")  # subscribe to topic
client.subscribe("/pilight")


def on_message(client, userdata, message):  # what to do when get message from mqtt
    if client == "/pilight" and message == "on":
        GPIO.output(21, GPIO.HIGH)  # turn on pi LED
        return
    elif client == "/pilight" and message == "off":
        GPIO.output(21, GPIO.LOW)  # turn off pi LED
        return
    
    if client == "/led" and (message == "on" or message == "off"):  # check for messages that are intended for the esp
        return

    global lightstate

    # convert bytes -> string -> int
    lightstate = int((message.payload).decode("utf-8"))

    # get current time
    receiveTime = datetime.datetime.utcnow()

   # create json to insert into db
    json_body = [{
        "measurement": 'test',
        "time": receiveTime,
        "fields": {
            "lightstate": lightstate}}]

    dbclient.write_points(json_body)
    
client.on_message = on_message  # set the on message function


client.loop_start()  # start client
try:
    while True:
        pass

except KeyboardInterrupt:
    pass

client.loop_stop()  # stop clientß


# write to db

print("Finished writing to InfluxDB")
 