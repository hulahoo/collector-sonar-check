import http.server
import socketserver

PORT = 8002

Handler = http.server.BaseHTTPRequestHandler


class CustomHandler(http.server.BaseHTTPRequestHandler):
    def handle(self) -> None:
        data = str(self.request.recv(1024), 'ascii')
        # data = self.request[0].strip()
        print("{} wrote:".format(self.client_address[0]))
        print('HANDLED', data, self)

        print(data)
        return super(CustomHandler, self).handle()

    def do_GET(self) -> None:
        print(self)
        return super(CustomHandler, self).do_GET()


with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
