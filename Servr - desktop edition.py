from wsgiref.simple_server import make_server
import os
print "Welcome to Servr - desktop edition!"
##autoStartConfigFile = open(os.path.join(os.path.expanduser("~"), "/servrAutoStartConfig.txt"), "a+")
autoStartConfigFile = open("/servrAutoStartConfig.txt", "a+")
autoStartConfig = autoStartConfigFile.read().split("\n")
doAutoStart = autoStartConfig[0]
if doAutoStart == "n":
  fileName = raw_input("Enter full HTML file path including extension (must use UTF-8 encoding):")
  dataFile = open(fileName, "r")
  htmlData = dataFile.read().split("\n")
  dataFile.close()
  address = raw_input("Enter this device's private IP address:")
  port = raw_input("Enter an unused port:")
elif doAutoStart == "y":
  print "Getting data from servrAutoStartConfig.txt..."
  fileName = autoStartConfig[1]
  dataFile = open(fileName, "r")
  htmlData = dataFile.read().split("\n")
  address = autoStartConfig[2]
  port = autoStartConfig[3]
def host(environ, start_response):
  status = "200 OK"
  headers = [("CContent-type", "text/html")]
  start_response(status, headers)
  return [str("".join(htmlData))]
webServer = make_server(address, int(port), host)
print "Serving at address " + address + ":" + port
webServer.serve_forever()
  
