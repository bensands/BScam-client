#!/usr/bin/python

import time
import picamera
import paho.mqtt.client as mqtt

def on_message(mosq, obj, msg):
	print("hi")
	if msg.payload == "1":
		camera.capture('image.jpg')
		f = open('image.jpg')
		imagestring = f.read()
		byteArray = bytes(imagestring)
		client.publish("takepic", "0")
		client.publish("photo", byteArray, 0)

camera = picamera.PiCamera()

client = mqtt.Client()
client.on_message = on_message
client.connect("server.ip.goes.here") 	# paste in the IP of the MQTT server
client.subscribe("takepic")

client.loop_forever()
