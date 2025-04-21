from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())

        elif self.path == '/updates':
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')  # Critical for SSE
            self.end_headers()

            if not os.path.exists('output.txt'):
                with open('output.txt', 'w'): pass

            last_modified = os.path.getmtime('output.txt')
            try:
                while True:
                    # Check if client disconnected (for non-Linux systems)
                    if hasattr(self, 'wfile') and self.wfile.closed:
                        break

                    current_modified = os.path.getmtime('output.txt')
                    if current_modified != last_modified:
                        last_modified = current_modified
                        with open('output.txt', 'r') as file:
                            data = file.read()
                            formatted_data = data.replace('\n', '\\n')
                            self.wfile.write(f"data: {formatted_data}\n\n".encode())
                    else:
                        # Send heartbeat every 15 seconds
                        self.wfile.write(": heartbeat\n\n".encode())
                    
                    self.wfile.flush()
                    time.sleep(2)

            except (ConnectionResetError, BrokenPipeError):
                print("Client disconnected gracefully")

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    server = HTTPServer((host, port), Server)
    print(f'Server running at http://{host}:{port}')
    server.serve_forever()
