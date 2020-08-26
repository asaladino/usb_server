from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import io, os


hostName = "0.0.0.0"
serverPort = 8081

class UsbServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        gps_text = self.read_from_usb()
        self.wfile.write(bytes(gps_text, "utf-8"))
        
    def read_from_usb(self):
        tty = io.TextIOWrapper(io.FileIO(os.open("/dev/ttyUSB0", os.O_NOCTTY | os.O_RDWR), "r+"))

        count = 0
        lines = ""
        for line in iter(tty.readline, None):
            lines += line
            count += 1
            if count  > 20:
                break
	    	
        return lines

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), UsbServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
