#!/usr/bin/python

import json
import sys
import urllib2
import time
import os

if len(sys.argv) != 2:
	print "This script takes in one argument, the url path to the Jenkins Job."
	sys.exit(2)

jenkinsUrl = sys.argv[1]

try:
	jenkinsStream = urllib2.urlopen(jenkinsUrl + "/lastBuild/api/json")
except urllib2.HTTPError, e:
	print "URL Error: " + str(e.code)
	sys.exit(2)

try:
	buildStatusJson = json.load(jenkinsStream)
except:
	print "Failed to parse jenkins status JSON"
	sys.exit(3)

if buildStatusJson.has_key("number"):
	print "Build number: " + str(buildStatusJson["number"])
	buildNumber = buildStatusJson["number"]

building=True
while (building):
	try:
		jenkinsStream = urllib2.urlopen(jenkinsUrl + "/" + str(buildNumber) + "/api/json")
	except urllib2.HTTPError, e:
		print "URL Error: " + str(e.code)
		sys.exit(2)
	try:
		buildStatusJson = json.load(jenkinsStream)
	except:
		print "Failed to parse jenkins status JSON"
		sys.exit(3)

	if buildStatusJson.has_key("result"):
		if buildStatusJson["result"] is not None:
			building = False
			print "build status: " + buildStatusJson["result"]
			if buildStatusJson["result"] != "SUCCESS" :
				print "not successful"
				os.system("osascript -e 'tell app \"System Events\" to display dialog \"Build Unsuccessful\"'")
				exit(4)
			else:
				os.system("osascript -e 'tell app \"System Events\" to display dialog \"Build Complete\"'")
				exit(5)
	
	time.sleep(10)
