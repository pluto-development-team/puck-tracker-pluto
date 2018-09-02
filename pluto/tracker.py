__author__ = "Dennis Claußner"

from cv2 import VideoCapture
import cv2 as cv
import numpy as np
import multi_tracker
from puck_kcf import TrackablePuck
import cascade
import copy
import utils

DEBUG = False
THREADED = True

capture = None
writeVideo = False
writer = None
top = 0
bottom = 0
right = 0
left = 0
totalTimePassed = 0
firstRun = True

def main(args):
    #C:\Users\dc\Studium\Projektlabor Mathesis\Projekt\20 schwarze Pucks - Spiegel.mp4
    fileName = input("Dateipfad eingeben: ")
    setup(fileName, "C:\\Users\\dc\\Studium\\Projektlabor Mathesis\\Projekt\\GitRepo\\mathesis\\code\\final\\cascade.xml", None) #Current version for modified pucks
    running = True
    while running:
        running, frameCount, data, runTime = run()
    cleanupTracker()
    print("Total time:", utils.clockStringFromSecs(totalTimePassed / 1000))
    return 0

def setup(videoFile, cascadeFile, initialBoxes = None, writeToVideo = False, outputFile = "result.mp4"):
    """Reads in the video, requests cropping dimensions and
    runs the cascade to find the pucks"""
    global capture, writer, writeVideo, top, bottom, right, left
    
    #Open video file
    capture = VideoCapture(videoFile)
    
    #Read first frame
    success, frame = capture.read()
    if not success: return False, 0
    
    #Get video details
    cols = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
    rows = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
    framecount = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
    framerate = int(capture.get(cv.CAP_PROP_FPS))
    
    #Select table size and crop the frame
    cv.namedWindow("Tisch auswaehlen und mit Enter bestaetigen", cv.WINDOW_NORMAL | cv.WINDOW_KEEPRATIO)
    tableBox = cv.selectROI("Tisch auswaehlen und mit Enter bestaetigen", frame, True, True);
    if DEBUG: print(tableBox)
    x, y, w, h = tableBox
    x, y = max(x, 0), max(y, 0)
    if DEBUG: print(x, y, w, h)
    top, bottom, left, right = y, y + h, x, x + w
    frame = frame[top:bottom, left:right]
    cv.destroyWindow("Tisch auswaehlen und mit Enter bestaetigen")
    
    openAndConfigureWindow()
    cv.imshow("Tracker", frame)
    cv.waitKey(0)
    
    #Find objects or use the boxes passed from user input and filter oversized and undersized boxes out
    if initialBoxes == None or len(initialBoxes) == 0:
        initialBoxes = cascade.findPucksInitial(cascadeFile, frame)
        initialBoxes[:] = (box for box in initialBoxes if utils.checkSizeOK(box))
        if DEBUG: print(initialBoxes)
    
    frameCopy = frame[:, :, :]
    for box in initialBoxes:
        p1 = (int(box[0]), int(box[1]))
        p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
        cv.rectangle(frameCopy, p1, p2, (0,0,255), 2, 1)
    cv.imshow("Tracker", frameCopy)
    cv.waitKey(0)
    
    utils.filterDuplicates(initialBoxes)
    
    for box in initialBoxes:
        p1 = (int(box[0]), int(box[1]))
        p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
        cv.rectangle(frameCopy, p1, p2, (0,255,0), 2, 1)
    cv.imshow("Tracker", frameCopy)
    cv.waitKey(0)
    
    modifiedBoxes = []
    for box in initialBoxes:
        modifiedBoxes.append(utils.shrinkBox(box))
    
    #Create TrackablePuck objects
    initialObjects = []
    multi_tracker.puckCountStart = len(modifiedBoxes)
    for i in range(0, len(modifiedBoxes)):
        initialObjects.append(TrackablePuck(i, modifiedBoxes[i]))
    
    #Initialize trackers and draw initial boxes and their indizes onto the frame
    displayFrame, positions = multi_tracker.addInitialObjects(initialObjects, frame)
    cv.imshow("Tracker", displayFrame)
    cv.waitKey(0)
    cv.destroyWindow("Tracker")
    
    #Reset frame counter
    capture.set(cv.CAP_PROP_POS_FRAMES, 0)
    
    #Initialize a video writer to write the frames with tracker marks to a file
    writeVideo = writeToVideo
    if writeToVideo:
        writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc(*'DIVX'), 60, (w, h))
    
    #Returns True, the total number of frames of the video, the frame with the markers, the amount of pucks and the frame size when the setup was successful
    return True, capture.get(cv.CAP_PROP_FRAME_COUNT), displayFrame, multi_tracker.puckCountStart, w, h

def run():
    """Reads a frame from the video, tracks the pucks and
    returns the position data to the caller"""
    global writer, totalTimePassed, firstRun
    
    if firstRun:
        firstRun = False
        openAndConfigureWindow()
    
    startTime = utils.millis()
    
    #Read next frame
    success, frame = capture.read()
    if not success: return False, 0, None, 0
    
    #Crop frame
    frame = frame[top:bottom, left:right]
    
    #Track objects
    displayFrame, positions = multi_tracker.trackObjects(frame)
    
    if DEBUG:
        frameMax = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
        frameCount = int(capture.get(cv.CAP_PROP_POS_FRAMES))
        time = utils.millis() - startTime
        totalTimePassed += time
        secs = int((time * (frameMax - frameCount)) / 1000)
        countStr = "Frame: " + str(frameCount) + "/" + str(frameMax)
        ellapStr = "Ellapsed: " + utils.clockStringFromSecs(totalTimePassed / 1000)
        etaStr = "ETA: " + utils.clockStringFromSecs(secs)
        cv.putText(displayFrame, countStr, (0, 25), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
        cv.putText(displayFrame, ellapStr, (0, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
        cv.putText(displayFrame, etaStr, (0, 75), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
    
    #Display frame and write it to the video file
    cv.imshow("Tracker", displayFrame)
    if writeVideo:
        writer.write(displayFrame)
    cv.waitKey(1)
    
    timeElapsed = utils.millis() - startTime
    
    #Returns status, frame counter, current puck positions and the time taken for processing this frame
    return True, capture.get(cv.CAP_PROP_POS_FRAMES), positions, timeElapsed

def cleanupTracker():
    """Cleans up the video input and output and instructs
    the multi_tracker to do cleanup as well"""
    global capture, writer
    if not capture == None:
        capture.release()
        capture = None
    if not writer == None:
        writer.release()
        writer = None
    multi_tracker.cleanupMultiTracker()
    cv.destroyWindow("Tracker")

def openAndConfigureWindow():
    cv.namedWindow("Tracker", cv.WINDOW_NORMAL | cv.WINDOW_KEEPRATIO)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
