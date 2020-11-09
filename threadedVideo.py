#!/usr/bin/env python3

import cv2
import threading
from threadQueue import ProdConsQueue

#based on the demo for extract frames
def extract_frames(userFile, queue):
    count = 0  #initialize frame count 
    video_file = cv2.VideoCapture(userFile)

    success,image = video_file.read() #returns whether the frame is read correctly, and a frame

    print(f'Reading frame {count} {success}')
    while success: 
        queue.putFrame(image) #adding a frame to the queue
        success,image = video_file.read() #get another frame
        print(f'Reading frame {count} {success}')
        count += 1 #increment the fram count

    print('Finished extracting frames')
    queue.putFrame('$') #putting a $ to show an empty queue

def convert_gray(colorFrames, grayFrames):
    count = 0 #frame count
    colorFrame = colorFrames.getFrame() #get a frame from queue of extracted color frames

    while colorFrame is not '$': #as long as the extracted frames queue isnt empty 
        print(f'Converting frame {count}')
        grayFrame = cv2.cvtColor(colorFrame,cv2.COLOR_BGR2GRAY) #convert frame to gray and save it

        grayFrames.putFrame(grayFrame) #put the gray frame into a queue of gray frames
        count += 1 #increment frame count

        colorFrame = colorFrames.getFrame() #dequeue next color frame

    print('Conversion to grayscale complete')
    grayFrames.putFrame('$') #if the gray queue is empty

def display_frames(frames):
    count = 0 #frame count
    frame = frames.getFrame() #get a frame from the gray queue

    while frame is not '$': #if the gray queue is not empty
        print(f'Displaying frame {count}')
        cv2.imshow('Video',frame) #display the frame in a window
        if cv2.waitKey(42) and 0xFF == ord("q"): #wait 42ms and check if the user wants to quit
            break
        count += 1 #increment frame count

        frame = frames.getFrame() #dequeue next gray frame

    print('Finished displaying all the frames')
    cv2.destroyAllWindows() #cleanup all the windows that were displaying

if __name__ == "__main__":
    color_frames = ProdConsQueue() #initialize the queue for color frames
    gray_frames = ProdConsQueue()  #initialize the queue for the gray frames

    #extract frames, convert frames, and display frames fuctions 
    extract = threading.Thread(target = extract_frames, args = ('clip.mp4',color_frames))
    convert = threading.Thread(target = convert_gray, args = (color_frames, gray_frames))
    display = threading.Thread(target = display_frames, args = (gray_frames,))

    #starts the threads
    extract.start()
    convert.start()
    display.start()
