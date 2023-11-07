import http.server
import socketserver
import signal
from helium import *


def open_shadow_user(userid, password):
    try:
        if not userid or not password:
            return

        # When username and password are submitted continue to do the shadow login
        start_chrome("my url")

        # Helium steps

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        kill_browser()


# Define a custom request handler to parse query parameters
class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters from the request
        query_params = {}
        if "?" in self.path:
            query_string = self.path.split("?")[1]
            query_params = dict(param.split("=") for param in query_string.split("&"))

        if query_params.get("username") and query_params.get("password"):
            open_shadow_user(query_params.get("username"), query_params.get("password"))

        # Send a response with the parsed query parameters
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"Query Parameters: {query_params}", "utf-8"))


# Create a simple HTTP server
PORT = 8000
server = None


def shutdown_server(signum, frame):
    global server
    if server:
        server.server_close()
        print("Server has been shut down")
        exit(0)


server = socketserver.TCPServer(("", PORT), CustomRequestHandler)
print(f"Serving at port {PORT}")

# Register a signal handler to gracefully shut down the server
signal.signal(signal.SIGINT, shutdown_server)

try:
    # Start the server and keep it running until Ctrl+C is pressed
    server.serve_forever()
except KeyboardInterrupt:
    pass
