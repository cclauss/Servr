from wsgiref.simple_server import make_server
import os
import mimetypes
print "Welcome to Servr - desktop edition!"
with open("Config.txt", "a+") as autoStartConfigFile:
  pass
with open("Config.txt", "r") as autoStartConfigFile:
  autoStartConfig = autoStartConfigFile.read().split("\n")
doAutoStart = autoStartConfig[0].lower()
if doAutoStart == "y":
  print "Getting data from Config.txt..."
  fileName, address, port = autoStartConfig[1:3]
else:
  fileName = raw_input("Enter homepage HTML file name including extension:").strip()
  address = raw_input("Enter this device's private IP address:").strip()
  port = raw_input("Enter an unused port:").strip()
with open("Resources/" + fileName, "r") as dataFile:
  htmlData = dataFile.read().split("\n")

def fileNames_mimeTypes_and_data(directory="Resources"):
  data = []
  mimeTypes = []
  fileNames = []
  for fileName in os.listdir(directory):
    with open(directory + "/" + fileName, "r") as dataFile:
      mimeTypes.append(mimetypes.guess_type(fileName))
      data.append(dataFile.read())
      resourceList = fileName.split("/")
      fileNames.append(resourceList[-1])
  return fileNames, mimeTypes, data

fileNames, mimeTypes, data = fileNames_mimeTypes_and_data()

def host(environ, start_response):
  i = 0
  if environ["PATH_INFO"] in (None, "/", "/home", "/index.html"):
    dataToReturn = "".join(htmlData)
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
