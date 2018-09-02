__author__ = "Dennis Claußner"

import cv2 as cv
import numpy as np
import multi_tracker
import utils
import copy
import tracker

class TrackablePuck:
	def __init__(self, identifier, track_window):
		self.identifier = identifier
		#track_window == (column, row, width, height)
		self.bbox = track_window
		self.failed = False
		self.lastValidBox = None
		self.framesMissing = 0
		self.failedHard = False
	
	def setupValues(self, frame):
		"""Set up the initial ROI from the first frame that was used
		to find and identify the objects"""
		self.tracker = cv.TrackerKCF_create()
		ok = self.tracker.init(frame, self.bbox)
	
	def track(self, frame, frameCopy, threadLock = None):
		"""Track objects on the frame and mark them on the frameCopy,
		uses the threadLock for thread sync if necessary"""
		ok, self.bbox = self.tracker.update(frame)
		
		if ok and not self.failed: # Tracking success
			# Draw bounding box
			if not threadLock is None: threadLock.acquire(1)
			self.drawMarkerOnFrame(frameCopy)
			if not threadLock is None: threadLock.release()
			self.lastValidBox = copy.deepcopy(self.bbox)
		elif not self.failedHard:
			self.failed = True
			
			#If a puck is can't be found within 5 frames after losing it, the last position reference
			#is considered useless and we stop trying to find that puck again
			self.framesMissing += 1
			if self.framesMissing > 5:
				self.failedHard = True
				if not threadLock is None: threadLock.acquire(1)
				multi_tracker.notifyPuckHardFail()
				if not threadLock is None: threadLock.release()
	
		#return the bounding box points
		return utils.getCoordsFromXYWH(self.bbox)
	
	def checkBoxRelation(self, box):
		"""Check if self.bbox is within the given box"""
		return utils.doesBox1ContainBox2(box, self.lastValidBox)
	
	def notifyRecovered(self, newBox, frame):
		"""Notifies the puck that it has been recovered by the cascade"""
		self.bbox = newBox
		self.lastValidBox = copy.deepcopy(newBox)
		self.failed = False
		self.framesMissing = 0
	
	def drawMarkerOnFrame(self, frameCopy):
		"""Draw the mark (box) onto the frameCopy"""
		p1 = (int(self.bbox[0]), int(self.bbox[1]))
		p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
		cv.rectangle(frameCopy, p1, p2, (255,0,0), 2, 1)
	
	def printIndizes(self, frameCopy):
		"""Prints the puck identifier on the puck"""
		coord = (int(self.bbox[0]), int(self.bbox[1] + 24))
		cv.putText(frameCopy, str(self.identifier), coord, cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
		
