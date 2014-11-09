from wsgiref.simple_server import make_server
import os
import mimetypes
import subprocess
import php
import re
print "Welcome to Servr - desktop edition!"
autoStartConfigFile = open("Config.txt", "a+")
autoStartConfigFile.close()
autoStartConfigFile = open("Config.txt", "r")
autoStartConfig = autoStartConfigFile.read().split("\n")
doAutoStart = autoStartConfig[0]
data = []
mimeTypes = []
fileNames = []
if doAutoStart == "n":
	fileName = raw_input("Enter homepage HTML file name including extension:")
	dataFile = open("Resources/" + fileName, "r")
	htmlData = dataFile.read().split("\n")
	dataFile.close()
	resourceFileNameList = os.listdir("Resources")
	os.chdir("Resources")
	for fileName1 in resourceFileNameList:
		if os.path.isdir(fileName1):
			resourceFileNameList2 = os.listdir(fileName1)
			os.chdir(fileName1)
			for fileName2 in resourceFileNameList2:
				if os.path.isdir(fileName2):
					resourceFileNameList3 = os.listdir(fileName2)
					os.chdir(fileName2)
					for fileName3 in resourceFileNameList3:
						if not os.path.isdir(fileName3) and fileName3 != ".DS_Store":
							dataFile = open(fileName3, "r")
							mimeTypes.append(mimetypes.guess_type(fileName3))
							data.append(dataFile.read())
							resourceList = fileName3.split("/")
							del resourceList[0]
							fileNames.append(fileName1 + "/" + fileName2 + "/" + fileName3)
							dataFile.close()
					os.chdir("..")
				else:
					if fileName2 != ".DS_Store":
						dataFile = open(fileName2, "r")
						mimeTypes.append(mimetypes.guess_type(fileName2))
						data.append(dataFile.read())
						resourceList = fileName2.split("/")
						del resourceList[0]
						fileNames.append(fileName1 + "/" + fileName2)
						dataFile.close()
			os.chdir("..")
		else:
			if fileName1 != ".DS_Store":
				dataFile = open(fileName1, "r")
				mimeTypes.append(mimetypes.guess_type(fileName))
				data.append(dataFile.read())
				resourceList = fileName1.split("/")
				fileNames.append(resourceList[len(resourceList) - 1])
				dataFile.close()
	os.chdir("..")
	address = raw_input("Enter this device's private IP address:")
	port = raw_input("Enter an unused port:")
elif doAutoStart == "y":
	print "Getting data from Config.txt..."
	fileName = autoStartConfig[1]
	resourceFileNameList = os.listdir("Resources")
	os.chdir("Resources")
	for fileName1 in resourceFileNameList:
		if os.path.isdir(fileName1):
			resourceFileNameList2 = os.listdir(fileName1)
			os.chdir(fileName1)
			for fileName2 in resourceFileNameList2:
				if os.path.isdir(fileName2):
					resourceFileNameList3 = os.listdir(fileName2)
					os.chdir(fileName2)
					for fileName3 in resourceFileNameList3:
						if not os.path.isdir(fileName3) and fileName3 != ".DS_Store":
							dataFile = open(fileName3, "r")
							mimeTypes.append(mimetypes.guess_type(fileName3))
							data.append(dataFile.read())
							resourceList = fileName3.split("/")
							del resourceList[0]
							fileNames.append(fileName1 + "/" + fileName2 + "/" + fileName3)
							dataFile.close()
					os.chdir("..")
				else:
					if fileName2 != ".DS_Store":
						dataFile = open(fileName2, "r")
						mimeTypes.append(mimetypes.guess_type(fileName2))
						data.append(dataFile.read())
						resourceList = fileName2.split("/")
						del resourceList[0]
						fileNames.append(fileName1 + "/" + fileName2)
						dataFile.close()
			os.chdir("..")
		else:
			if fileName1 != ".DS_Store":
				dataFile = open(fileName1, "r")
				mimeTypes.append(mimetypes.guess_type(fileName))
				data.append(dataFile.read())
				resourceList = fileName1.split("/")
				fileNames.append(resourceList[len(resourceList) - 1])
				dataFile.close()
	os.chdir("..")
	dataFile = open("Resources/" + fileName, "r")
	htmlData = dataFile.read().split("\n")
	address = autoStartConfig[2]
	port = autoStartConfig[3]
def host(environ, start_response):
	i = 0
	if environ["PATH_INFO"] == None or environ["PATH_INFO"] == "/home" or environ["PATH_INFO"] == "/index.html" or environ["PATH_INFO"] == "/":
		dataToReturn = str("".join(htmlData))
		mimeType = "text/html"
	else:
		for resource in data:
			if environ["PATH_INFO"] == "/" + str(fileNames[i]):
				if ".php" in str(fileNames[i]):
					dataToReturn = ""
					resource = resource.split("</body>")[0]
					n = 0
					phpStartList = [m.start() for m in re.finditer(r"\<\?php", resource)]
					phpEndList = [m.start() for m in re.finditer(r"\?\>", resource)]
					for inst in phpStartList:
						phpStart = resource.find("<?php") + 5
						phpEnd = resource.find("?>")
						phpCode = resource[phpStart:phpEnd]
						resource2 = resource[:resource.find("<?php")] + resource[resource.find("?>") + 2:]
						phpResponse = php.PHP().get_raw(phpCode)
						resource = resource2 + phpResponse
						n += 1
						dataToReturn = resource + "</body></html>"
						mimeType = "text/html"
					else:
						mimeType = str(mimeTypes[i][0])
						dataToReturn = resource
			i += 1
	status = "200 OK"
	try:
		headers = [("Content-type", mimeType)]
	except:
		headers = []
	start_response(status, headers)
	return [dataToReturn]
webServer = make_server(address, int(port), host)
i = 0
servers = []
print "Serving at address " + str(address) + ":" + port
webServer.serve_forever()
