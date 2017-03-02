#!/bin/python

import sys,os
import time
import hashlib
import urllib
import urllib2
import json
import socket
import uuid
import fcntl
import struct
import datetime
pf=74
#time_stamp
time_s=int(time.time())
time_stamp=str(time_s)

#sha1 viatest
test='viatest'
singnature=str(time_stamp)
singnature+=test
hash_sha1=hashlib.sha1(singnature)

#ip 
def get_ip(ethname):
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ethname[:15]))[20:24])

#http_get
def http_get():
	try:	
		url1="http://192.168.0.22/systemvalidation/autolog/synctime/?timestamp=1477484788&signature=34e881a3fd52a8871253c7100942b6a4008e51aa"
		response=urllib2.urlopen(url1)
		res=float(response.read())
		return res
	except:
		print 'Can not get server time.'

if __name__=='__main__':
	ip=get_ip('enp2s0')

#time_replace	
def time_replace():
	ret=http_get()
	timeArray=time.localtime(ret)
	timenow=time.strftime('%Y-%m-%d %H:%M:%S',timeArray)	
	return timenow

print time_stamp
timenow=time_replace()
os.system("date -s '%s'" %(timenow))  


#post heartbeat
def heartbeat():
	url="http://192.168.0.22/systemvalidation/autolog/heartbeat/?ip="+ip+"&timestamp="+time_stamp+"&signature="+hash_sha1.hexdigest()
	post={"item":"heartbeat","platform":{"location":"%i" %pf}}
	print url
	jdata=json.dumps(post)
	print jdata
	req=urllib2.Request(url,jdata)
	response=urllib2.urlopen(req)
	return response.read()

#ack
def ack():
	hb=heartbeat()
	url="http://192.168.0.22/systemvalidation/autolog/heartbeat/?ip="+ip+"&timestamp="+time_stamp+"&signature="+hash_sha1.hexdigest()
	post={"item":"heartbeat","ack":"ack","platform":{"location":"%i" %pf}}
	jdata=json.dumps(post)
	print jdata
	req=urllib2.Request(url,jdata)
	response=urllib2.urlopen(req)
	return response.read()

#store data
def store():
	f=open("/root/json","w")
	f.write(heartbeat())
	f.close()

def load():
	with open("/root/json" ) as json_file:
	udata=json.load(json_file)
	return udata
	print udata[0]["item"]

while True:
	print heartbeat()
	if heartbeat()=="0" or heartbeat()=="NULL":
		print "have no task"
	else: 	
		store()
		print heartbeat()
		ack()
		print "ack now"
		data=load()
		item=data[0]["item"]
		start_time=data[0]["startTime"]
		end_time=data[0]["endTime"]
		if item=="acpis3"		
	time.sleep(10)

