# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

hostName = "myth58.stanford.edu"
serverPort = 6161
SECTION_SIZE = 10240 # 10 KB
filename = "book.txt"

class MyServer(BaseHTTPRequestHandler):        

    def do_GET(self):
        self.send_response(200)
        # if self.path.
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html>", "utf-8"))
        self.wfile.write(bytes("<p>Request path: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))

        number = int(self.path[1:])
        start = SECTION_SIZE * number

        # check to make sure start < length of file
        if start < os.path.getsize(filename):
            with open(filename) as f:
                f.seek(start) 
                readBytes = bytes(f.read(SECTION_SIZE), "utf-8")
                self.wfile.write(readBytes)
        else:
            self.wfile.write(bytes("Request invalid. Chunk out of range.", "utf-8"))
            

        self.wfile.write(bytes("</body></html>", "utf-8"))

        



if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")