#!/usr/bin/python
#eMonitor by Kranu
#modified by DarkTrick
#Version 2 (9-1-2011)

#Tested on Windows 7 x64, Python 2.7.2
#Tested on Ubuntu 19.04, Python 2.7.16
#For more information, see: http://goo.gl/rJoLp

#BEGIN SETUP

#HTTP Server
port=8080 #port of http server (http://127.0.0.1:8000/)

#capture region
#l,t=(1680,1050-800)
l,t=(10,120) #left and right offset from primary monitor
#rootWindow,h=(595,701) #width and height of capture region
rootWindow,h=(701,595) #width and height of capture region

# "ss" = screenshot
ssX = l
ssY = t
ssWidth = rootWindow
ssHeight = h

#fn ='shot.jpg' #file name of screenshot
fn ='shot.png' #file name of screenshot

#//END SETUP

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time


# import GTK
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk as gdk
from gi.repository import GObject as gobject

# Windows only?
# import gtk.gdk as gdk

class GdkPixbufAdapterLinux:
  """
  I'm not sure if the code here is same on win and linux;
  thereore I created this adapter already - just in case.
  """
  def __init__(self, rootWindow, ssX,ssY,ssWidth,ssHeight):
    self.buffer = gdk.pixbuf_get_from_window(rootWindow, ssX,ssY,ssWidth,ssHeight)

  def save(self, filename, encoding = "png"):
    if (not self.hasBuffer()):
      return False

    return self.buffer.savev (filename, encoding)

  def hasBuffer(self):
    return (self.buffer != None)

  def rotate_simple(self, degrees):
    self.buffer = self.buffer.rotate_simple(degrees)




def gtkScreenshot():
  rootWindow = gdk.get_default_root_window()
  #ssWidth,ssHeight = rootWindow.get_size()
  #print "The size of the window is %d x %d" % sz

  image = GdkPixbufAdapterLinux (rootWindow, ssX,ssY,ssWidth,ssHeight)
  image.rotate_simple(90)

  ts = time.time()
  filename = fn

  if (not image.save(filename,"png")):
    print("Unable to get the screenshot.")

class serv(BaseHTTPRequestHandler):

  def deliverSite(self):
    #print("deliverSite()")

    self.send_header('Content-type','text/html')
    self.end_headers()

    reloadFunction = 'function() {'\
    ' document.getElementById("pic").src="'+fn+'?"+(new Date()).getTime();'\
    '}'

    website = """
    <!doctype html>
    <html lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>eMonitor by Kranu</title>
    </head>
    <body id="bod" style="margin:0px;">
    <img id="pic" src='shot.png' >
    <script type="text/javascript">
    document.getElementById("pic").onclick="""+reloadFunction+"""
    </script>

    </body>
    </html>"""



    with open("debug_website.html","w") as file:
      file.write(website)

    websiteBytes = bytes(website,"utf-8")
    self.wfile.write(websiteBytes)

  def do_GET(self):
    self.send_response(200)
    if self.path.startswith('/'+fn): #check, if the request was about the image
      print("deliverImage()")


      self.send_header('Content-type','image/jpeg')
      self.end_headers()

      gtkScreenshot()

      with open(fn,'rb') as f:
        self.wfile.write(f.read())

    else:
      self.deliverSite()

def main():
  try:
    print( 'eMonitor by Kranu')

    #Amazon's website is used here for its reliablity. Feel free to change it.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("amazon.com",80))

    print ('Starting.. '),
    server=HTTPServer(('',port),serv)
    print ('Press Ctrl+C to stop')
    print ("")

    print ('On your Kindle, visit http://'+s.getsockname()[0]+':'+str(port)+'/')

    # take initial screenshot
    gtkScreenshot()


    server.serve_forever()
  except KeyboardInterrupt:
    print ('Stopping.. '),
    server.socket.close()

if (__name__ == "__main__"):
  main()
