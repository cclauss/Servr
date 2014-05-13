from wsgiref.simple_server import make_server
import os
import mimetypes
print "Welcome to Servr - desktop edition!"
autoStartConfigFile = open("servrAutoStartConfig.txt", "a+")
autoStartConfigFile.close()
autoStartConfigFile = open("servrAutoStartConfig.txt", "r")
autoStartConfig = autoStartConfigFile.read().split("\n")
doAutoStart = autoStartConfig[0]
data = []
mimeTypes = []
fileNames = []
if doAutoStart == "n":
  fileName = raw_input("Enter full homepage HTML file path including extension:")
  dataFile = open(fileName, "r")
  htmlData = dataFile.read().split("\n")
  dataFile.close()
  resourceNum = int(raw_input("Enter number of resources other than the homepage to be used:"))
  i = 0
  while i < resourceNum:
    fileName = raw_input("Enter full resource file path including extension:")
    dataFile = open(fileName, "r")
    mimeTypes.append(mimetypes.guess_type(fileName))
    data.append(dataFile.read())
    resourceList = resource.split("/")
    fileNames.append(resourceList[len(resourceList) - 1])
    dataFile.close()
    i += 1
  address = raw_input("Enter this device's private IP address:")
  port = raw_input("Enter an unused port:")
elif doAutoStart == "y":
  print "Getting data from servrAutoStartConfig.txt..." 
  fileName = autoStartConfig[1]
  resources = autoStartConfig[2].split(",")
  for resource in resources:
    dataFile = open(resource, "r")
    mimeTypes.append(mimetypes.guess_type(resource))
    data.append(dataFile.read())
    resourceList = resource.split("/")
    fileNames.append(resourceList[len(resourceList) - 1])
    dataFile.close()
  dataFile = open(fileName, "r")
  htmlData = dataFile.read().split("\n")
  address = autoStartConfig[3]
  port = autoStartConfig[4]
def host(environ, start_response):
  i = 0
  if environ["PATH_INFO"] == None or environ["PATH_INFO"] == "/home" or environ["PATH_INFO"] == "/index.html" or environ["PATH_INFO"] == "/":
    dataToReturn = str("".join(htmlData))
    mimeType = "text/html"
  else:
    for resource in data:
      if environ["PATH_INFO"] == "/" + str(fileNames[i]):
        mimeType = str(mimeTypes[i][0])
        dataToReturn = resource
      i += 1
  status = "200 OK"
  headers = [("Content-type", mimeType)]
  start_response(status, headers)
  return [dataToReturn]
webServer = make_server(address, int(port), host)
i = 0
servers = []
print "Serving at address " + str(address)+ ":" + port
webServer.serve_forever()
