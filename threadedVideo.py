#!/usr/bin/env python3

import threading
import cv2

class ProConsQueue():
    def __init__(self,queueCapacity):
        self.queue = []
        self.full = Semaphore(0)
        self.empty = Semaphore(24)

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
        return frame)
