#!/usr/bin/env python3

import threading
import cv2

class ProdConsQueue():
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
        return frame

    def extract_frames(userFile, queue):
        count = 0
        video_file = cv2.VideoCapture(userFile)

        success,image = video_file.read()

        while success:
            queue.put(image)
            success,image = video_file.read()
            count += 1

        queue.put('$')

    def convert_gray(color. gray):
        count = 0

        colorFrame = color.get()

        while colorFrame is not '$':
            grayFrame = cv2.cvtColor(colorFrame,cv2.COLOR_BGR2GRAY)

            gray.put(grayFrame)
            count += 1

            colorFrame = color.get()

        grat.put('$')

    def display_frames(frames):
        count = 0
        currentFrame = frames.get()

        while currentFrame is not '$':
            cv2.imshow('Video',currentFrame)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break
            count += 1

            currentFrame = frames.get()

        cv2.destroyAllWindows()

    color_frames = ProdConsQueue()
    gray_frames = ProdConsQueue()

    extract = threading.Thread(target = extract_frames, args = ('clip.mp4',color_frames))
    convert = threading.Thread(target = convert_frames, args = (color_frames, gray_frames))
    display = threading.Thread(target = display_frames, args = (gray_frames))

    extract.start()
    convert.start()
    display.start()
