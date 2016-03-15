#!/usr/bin/python
from http.server import HTTPServer

from restful.endpoint import IRefuseHTTPRESTEndPoint


def main():
    ip = "127.0.0.1"
    port = 8000
    server_address = (ip, 8000)
    httpd = HTTPServer(server_address, IRefuseHTTPRESTEndPoint)
    print("Running server on {}:{}".format(ip, port))
    httpd.serve_forever()

if __name__ == "__main__":
    main()
