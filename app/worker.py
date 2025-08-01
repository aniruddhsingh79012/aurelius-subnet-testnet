import requests

class Worker:
    def __init__(self, worker_url, worker_port):
        self.worker_url = worker_url
        self.worker_port = worker_port

    def process_request(self):
        return requests.post(url=f"{self.worker_url}:{self.worker_port}/send_message/")