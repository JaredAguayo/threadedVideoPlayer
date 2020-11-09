#!/usr/bin/env python3

import cv2
import threading
from threadQueue import ProdConsQueue

def extract_frames(userFile, queue):
    count = 0
    video_file = cv2.VideoCapture(userFile)

    success,image = video_file.read()

    print(f'Reading frame {count} {success}')
    while success:
        queue.putFrame(image)
        success,image = video_file.read()
        print(f'Reading frame {count} {success}')
        count += 1

        print('Finished extracting frames')
        queue.putFrame('$')

def convert_gray(colorFrames, grayFrames):
    count = 0

    colorFrame = colorFrames.getFrame()

    while colorFrame is not '$':
        print(f'Converting frame {count}')
        grayFrame = cv2.cvtColor(colorFrame,cv2.COLOR_BGR2GRAY)

        grayFrames.putFrame(grayFrame)
        count += 1

        colorFrame = colorFrames.getFrame()

    print('Conversion to grayscale complete')
    grayFrames.putFrame('$')

def display_frames(frames):
    count = 0
    frame = frames.getFrame()

    while frame is not '$':
        print(f'Displaying frame {count}')
        cv2.imshow('Video',frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        count += 1

        frame = frames.getFrame()

    print('Finished displaying all the frames')
    cv2.destroyAllWindows()

if __name__ == "__main__":
    color_frames = ProdConsQueue()
    gray_frames = ProdConsQueue()

    extract = threading.Thread(target = extract_frames, args = ('clip.mp4',color_frames))
    convert = threading.Thread(target = convert_gray, args = (color_frames, gray_frames))
    display = threading.Thread(target = display_frames, args = (gray_frames,))

    extract.start()
    convert.start()
    display.start()
