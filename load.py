#!/bin/python
import json
import time

#def load():
#	with open("/root/json.bak") as json_file:
#		data=json.load(json_file)
data=[json.loads(line) for line in open('/root/json.bak')]
#data=[json.read(line) for line in open('/root/json.bak')]
#print data[0]
#		return data
#print data[0]['item']


#print data
#odata=data.keys()
#print odata
#print data['item']

with open("/root/json.bak" ) as json_file:
	udata=json.load(json_file)
	print udata
	print udata[0]["item"]
