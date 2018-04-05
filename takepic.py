#!/usr/bin/python -u

import time
import picamera
import paho.mqtt.client as mqtt

def on_disconnect(client, userdata, rc):
	print "unexpected disconnect at ", time.asctime(time.localtime(time.time()))	
	while not client.connected_flag:
		time.sleep(1)
		print "attempting to reconnect at ", time.asctime(time.localtime(time.time()))
		client.connect(serveripcred)

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		client.connected_flag = True # set flag
		print("connected OK")
		client.subscribe("takepic")
	else:
		print("Bad connection Returned code=",rc)
		mqtt.Client.connected_flag = False # create flag in class

def on_message(mosq, obj, msg):
	if msg.payload == "1":
		print "image requested by server at ", time.asctime(time.localtime(time.time()))
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
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(serveripcred)

client.loop_forever()
