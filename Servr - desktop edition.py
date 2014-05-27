from wsgiref.simple_server import make_server
import os
import mimetypes
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
  resourceFileNaameList = os.listdir("Resources")
  for fileName in resourceFileNameList:
    dataFile = open("Resources/" + fileName, "r")
    mimeTypes.append(mimetypes.guess_type(fileName))
    data.append(dataFile.read())
    resourceList = resource.split("/")
    fileNames.append(resourceList[len(resourceList) - 1])
    dataFile.close()
    i += 1
  address = raw_input("Enter this device's private IP address:")
  port = raw_input("Enter an unused port:")
elif doAutoStart == "y":
  print "Getting data from Config.txt..."
  fileName = autoStartConfig[1]
  resources = os.listdir("Resources")
  for resource in resources:
    dataFile = open("Resources/" + resource, "r")
    mimeTypes.append(mimetypes.guess_type(resource))
    data.append(dataFile.read())
    resourceList = resource.split("/")
    fileNames.append(resourceList[len(resourceList) - 1])
    dataFile.close()
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
print "Serving at address " + str(address) + ":" + port
webServer.serve_forever()
