"""Local build helper: fetch Maven Central through Python's verified HTTPS client."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import hashlib
import threading
import time
import requests

cache = Path(__file__).resolve().parent / 'maven-download-cache'
cache.mkdir(exist_ok=True)
gate = threading.Semaphore(8)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith('/central/') or '..' in self.path:
            self.send_error(404)
            return
        relative = self.path[len('/central/'):].split('?',1)[0]
        target = cache / hashlib.sha256(relative.encode()).hexdigest()
        with gate:
            if target.exists():
                body = target.read_bytes()
            else:
                response = None
                for attempt in range(4):
                    try:
                        response = requests.get('https://repo.maven.apache.org/maven2/'+relative, timeout=60)
                        body = response.content
                        break
                    except requests.RequestException as error:
                        print(type(error).__name__, str(error)[:160], flush=True)
                        if attempt == 3:
                            self.send_error(502, 'Upstream HTTPS download failed')
                            return
                        time.sleep(0.5)
                if response.status_code != 200:
                    self.send_error(response.status_code)
                    return
                target.write_bytes(body)
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


if __name__ == '__main__':
    print('Maven download bridge listening on 127.0.0.1:18765', flush=True)
    HTTPServer(('127.0.0.1',18765),Handler).serve_forever()
