__author__ = "Dennis Claußner"

import numpy as np
import cv2 as cv

cascade = None

def findPucksInitial(cascadeFile, frame):
	"""Initializes the HAAR cascade"""
	global cascade
	
	cascade = cv.CascadeClassifier(cascadeFile)
	return findPucks(frame)
	
def findPucks(frame):
	"""Uses the HAAR cascade to find pucks on the given frame"""
	global cascade
	
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	pucks = cascade.detectMultiScale(gray, 1.3, 5)
	result = []
	for (x, y, w, h) in pucks:
		result.append((x, y, w, h)) 
	return result
