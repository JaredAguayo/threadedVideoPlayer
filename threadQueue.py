import threading

class ProdConsQueue():
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(24)

    def putFrame(self,frame):
        self.empty.acquire()
        self.lock.acquire()
        self.queue.append(frame)
        self.lock.release()
        self.full.release()

    def getFrame(self):
        self.full.acquire()
        self.lock.acquire()
        frame = self.queue.pop(0)
        self.lock.release()
        self.empty.release()
        return frame

