#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):

        self.data = self.request.recv(1024).decode("utf-8")
        self.split = self.data.strip().split(' ')
        method = self.split[0]
        path = self.split[1]
        requestedPath = self.split[0:3]
        str1 = " "
        fullRequest = str1.join(requestedPath)
        if ( method != "GET"):
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", "utf-8"))
            return

        if "../../" in fullRequest:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", "utf-8"))
            return
            
        self.validate(path)

    def validate(self,requested):
        if os.path.isdir("www" + requested):
            if requested[-1] == "/":
                path = "www" + requested + "index.html"
                file = ""
                data = open(path, 'r')
                for line in data:
                    file += line
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/%s; charset=utf-8\r\n\r\n"%(path.split(".")[1])+file, 'utf-8'))
            else:
                self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\n", "utf-8"))
        elif not os.path.isfile("www" + requested):
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", "utf-8"))
            return
        else:
            path = "www" + requested
            file = ""
            data = open(path, 'r')
            for line in data:
                file += line
            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/%s; charset=utf-8\r\n\r\n"%(path.split(".")[1])+file, 'utf-8'))



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()