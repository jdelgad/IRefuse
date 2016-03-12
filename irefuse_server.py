#!/usr/bin/python

from http.server import BaseHTTPRequestHandler, HTTPServer


class IRefuseHTTPRESTEndPoint(BaseHTTPRequestHandler):

    def do_POST(self):
        print(self.headers)
        length = int(self.headers['Content-Length'])
        post_type = self.headers['Content-Type']

        if post_type == "application/json":
            post_data = self.rfile.read(length).decode()
            # You now have a dictionary of the post data
            print(post_data)

            self.wfile.write("received json {}".format(post_data).encode(
                "utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Invalid request".encode("utf-8"))


def main():
    ip = "127.0.0.1"
    port = 8000
    server_address = (ip, 8000)
    httpd = HTTPServer(server_address, IRefuseHTTPRESTEndPoint)
    print("Running server on {}:{}".format(ip, port))
    httpd.serve_forever()

if __name__ == "__main__":
    main()
