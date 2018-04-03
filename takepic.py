#!/usr/bin/python -u

import time
import picamera
import paho.mqtt.client as mqtt

def on_disconnect(client, userdata, rc):
	print "unexpected disconnect at ", time.asctime(time.localtime(time.time()))	
	while True:
		time.sleep(1)
		print "attempting to reconnect at ", time.asctime(time.localtime(time.time()))
		if client.connect(serveripcred):
			break

def on_message(mosq, obj, msg):
	print("hi")
	if msg.payload == "1":
		camera = picamera.PiCamera()
		camera.capture('image.jpg')
		camera.close()
		print("pic taken")
		f = open('image.jpg')
		imagestring = f.read()
		byteArray = bytes(imagestring)
		client.publish("takepic", "0")
		client.publish("photo", byteArray, 0)
		print("pic published")

print "takepic.py running at ", time.asctime(time.localtime(time.time()))
# get server ip:
with open("credentials.txt","r") as f:
	serveripcred = f.readline().rstrip()

client = mqtt.Client()
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(serveripcred) 	# paste in the IP of the MQTT server
client.subscribe("takepic")

client.loop_forever()
