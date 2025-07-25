import threading
import time

class URLStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = {}  # short_code: {url, clicks, created_at}

    def add(self, short_code, url):
        with self.lock:
            self.data[short_code] = {
                'url': url,
                'clicks': 0,
                'created_at': time.strftime('%Y-%m-%dT%H:%M:%S')
            }

    def get(self, short_code):
        with self.lock:
            return self.data.get(short_code)

    def increment_click(self, short_code):
        with self.lock:
            if short_code in self.data:
                self.data[short_code]['clicks'] += 1
                return True
            return False

    def exists(self, short_code):
        with self.lock:
            return short_code in self.data