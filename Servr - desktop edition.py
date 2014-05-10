from wsgiref.simple_server import make_server
import os
print "Welcome to Servr - desktop edition!"
##autoStartConfigFile = open(os.path.join(os.path.expanduser("~"), "/servrAutoStartConfig.txt"), "a+")
autoStartConfigFile = open("servrAutoStartConfig.txt", "r")
autoStartConfig = autoStartConfigFile.read().split("\n")
doAutoStart = autoStartConfig[0]
if doAutoStart == "n":
  pageNum = raw_input("Enter the number of pages you want to serve:")
  pageNumInt = int(pageNum)
  i = 1
  while i != pageNumInt:
    fileName = raw_input("Enter name of HTML file including extension (must use UTF-8 encoding and be in same folder as script):")
    dataFile = open(fileName, "r")
    exec 'htmlData' + i + ' = dataFile.read().split("\n")'
    dataFile.close()
    i += 1
  address = raw_input("Enter this device's private IP address:")
  port = raw_input("Enter an unused port:")
elif doAutoStart == "y":
  print "Getting data from servrAutoStartConfig.txt..."
  fileName = autoStartConfig[1]
  dataFile = open(fileName, "r")
  htmlData = dataFile.read().split("\n")
  address = autoStartConfig[2]
  port = autoStartConfig[3]
exec '''
def hostFunc''' + pageNum + '''(environ, start_response):
  status = "200 OK"
  headers = [("Content-type", "text/html")]
  start_response(status, headers)
  return [str("".join(htmlData''' + pageNum + '''))]
'''
webServer = make_server(address, int(port), hostFunc)
print "Serving at address " + address + ":" + port
webServer.serve_forever()
