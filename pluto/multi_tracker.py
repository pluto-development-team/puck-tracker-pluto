__author__ = "Dennis Claußner"

import copy
import cv2 as cv
import numpy as np
import tracker
import cascade
import utils
import threading
from worker_thread import WorkerThread
from puck_kcf import TrackablePuck

pucks = []
puckCountStart = 0

def addInitialObjects(data, frame):
	"""Handles first setup of the trackers"""
	global pucks
	pucks = copy.deepcopy(data)
	frameCopy = frame[:, :]
	positions = []
	
	for p in pucks:
		p.setupValues(frame)
		positions.append(p.track(frame, frameCopy))
		p.printIndizes(frameCopy)
	
	return frameCopy, positions

def trackObjects(frame):
	"""Tracks the pucks, checks for missing pucks and
	handles associated actions"""
	global counter, puckCountStart
	
	frameCopy = frame[:, :, :]
	positions = []
	
	if tracker.THREADED:
		trackObjectsThreaded(frame, frameCopy, positions)
	else:
		for p in pucks:
			positions.append(p.track(frame, frameCopy))
	
	#Count pucks and check if we lost one
	puckCount = 0
	for p in pucks:
		if not p.failed: puckCount += 1
	#If we lost one, try to find it and, if found again, correct the position in the positions list
	if puckCount < puckCountStart:
		if tracker.DEBUG:
			print("puckCountStart:", puckCountStart)
			print("puckCount:", puckCount)
		updatedPucks = updateBoxesWithCascade(frame, positions, frameCopy)
		for p in updatedPucks:
			positions[p.identifier] = utils.getCoordsFromXYWH(p.bbox)
			p.drawMarkerOnFrame(frameCopy)
	
	return frameCopy, positions

def trackObjectsThreaded(frame, frameCopy, positions):	
	"""Creates thread and lock objects to reliably
	track the pucks parallelized"""
	threadList = []
	threadLock = threading.Lock()
	
	for p in pucks:
		thread = WorkerThread(p, frame, frameCopy, positions, threadLock)
		thread.start()
		threadList.append(thread)
	
	for t in threadList:
		t.join()

def updateBoxesWithCascade(frame, positions, frameCopy):
	"""Tries to recover lost pucks by running the cascade again
	over the current frame"""
	boxes = cascade.findPucks(frame)
	count = len(boxes)
	
	for pos in positions:
		boxes[:] = (box for box in boxes if not utils.doesBoxContainCoords(box, pos))
	utils.filterDuplicates(boxes)
	for i in range(len(boxes)):
		boxes[i] = utils.enlargeBox(boxes[i], 80)
	
	"""
	frameCopyCopy = copy.deepcopy(frameCopy)
	
	if tracker.DEBUG:
		print("boxes found:", count)
		print("boxes left:", len(boxes))
		
	for box in boxes:
		p1 = (int(box[0]), int(box[1]))
		p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
		cv.rectangle(frameCopyCopy, p1, p2, ((0,255,0) if utils.checkSizeOK(box) else (0,0,255)), 2, 1)		
	
	for p in pucks:
		if p.failed and not p.failedHard:
			p1 = (int(p.lastValidBox[0]), int(p.lastValidBox[1]))
			p2 = (int(p.lastValidBox[0] + p.lastValidBox[2]), int(p.lastValidBox[1] + p.lastValidBox[3]))
			cv.rectangle(frameCopyCopy, p1, p2, (0,255,255), 2, 1)
	
	cv.imshow("Reclaiming", frameCopyCopy)
	cv.waitKey(0)
	"""
	
	updatedPucks = []
	
	for p in pucks:
		if p.failed and not p.failedHard:
			for box in boxes:
				if p.checkBoxRelation(box):
					p.notifyRecovered(utils.shrinkBox(box), frame)
					updatedPucks.append(p)
					break
	
	return updatedPucks

def notifyPuckHardFail():
	"""Used to decrement the amount of pucks that are known to be
	trackable when a puck goes missing and can not be recovered"""
	global puckCountStart
	puckCountStart -= 1 #Decrement this so we don't try to find a puck without a useable position reference

def cleanupMultiTracker():
	"""Cleans up the multi_tracker data"""
	pucks.clear()
	puckCountStart = 0
