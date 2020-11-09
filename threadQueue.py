import threading

class ProdConsQueue(): 
    def __init__(self): #create an object with python lists, the semaphores will block the putFrame and getFrame if empty/full 
        self.queue = []
        self.lock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(24)

    def putFrame(self,frame): #enqueue in the lists
        self.empty.acquire()
        self.lock.acquire()
        self.queue.append(frame)
        self.lock.release()
        self.full.release()

    def getFrame(self):  #dequeue in the lists
        self.full.acquire()
        self.lock.acquire()
        frame = self.queue.pop(0)
        self.lock.release()
        self.empty.release()
        return frame

