import queue
import threading

class JobQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.in_progress = {}

    def add_job(self, job_id, job, client_conn):
        with self.lock:
            self.queue.put((job_id, job, client_conn))
            print(f"[QUEUE] Job added {job_id}: {job}")

    def get_job(self):
        with self.lock:
            if not self.queue.empty():
                job_id, job, client_conn = self.queue.get()
                self.in_progress[job_id] = (job, client_conn)
                print(f"[ASSIGN] {job_id}")
                return job_id, job, client_conn
            return None

    def complete_job(self, job_id):
        with self.lock:
            if job_id in self.in_progress:
                del self.in_progress[job_id]