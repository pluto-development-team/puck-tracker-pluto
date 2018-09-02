__author__ = "Dennis Claußner"

import time

dotSize = 40
boxSizeMax = 200

def getCoordsFromXYWH(data):
	"""Converts the given box from top left corner coordinate and size
	to 4 corner coordinates"""
	return [(data[0], data[1]), (data[0] + data[2], data[1]), (data[0] + data[2], data[1] + data[3]), (data[0], data[1] + data[3])]

def doesBox1ContainBox2(box1, box2):
	"""Checks if the given box2 is within the given box1"""
	containsX = box2[0] >= box1[0] and (box2[0] + box2[2]) <= (box1[0] + box1[2])
	containsY = box2[1] >= box1[1] and (box2[1] + box2[3]) <= (box1[1] + box1[3])
	return containsX and containsY

def doesBoxContainCoords(box, coords2):
	"""Checks if the given coords2 lie in the given box"""
	coords1 = getCoordsFromXYWH(box)
	topLeftContained = coords1[0][0] <= coords2[0][0] and coords1[0][1] <= coords2[0][1]
	bottomRightContained = coords1[2][0] >= coords2[2][0] and coords1[2][1] >= coords2[2][1]
	return topLeftContained and bottomRightContained

def checkSizeOK(box):
	"""Checks if the given box is atleast the size of the ROI passed to
	the tracker and smaller than the maximum box size"""
	coords = getCoordsFromXYWH(box)
	sizeX = coords[1][0] - coords[0][0]
	sizeY = coords[3][1] - coords[0][1]
	return sizeX >= dotSize and sizeX <= boxSizeMax and sizeY >= dotSize and sizeY <= boxSizeMax

def filterDuplicates(boxes):
	"""Filters duplicated boxes out by checking if any box in the list
	lies within another box in the list"""
	toRemove = []
	for box in boxes:
		for b in boxes:
			if not box is b and doesBox1ContainBox2(box, b):
				toRemove.append(b)
				break
	
	for box in toRemove:
		boxes.remove(box)

def shrinkBox(box):
	"""Shrinks the given box to the size set for passing to the tracker"""
	width = box[2]
	height = box[3]
	diffX = dotSize - width
	diffY = dotSize - height
	
	copy = []
	
	copy.append(box[0] - (diffX / 2))
	copy.append(box[1] - (diffY / 2))
	copy.append(box[2] + diffX)
	copy.append(box[3] + diffY)
	
	return tuple(copy)

def enlargeBox(box, size):
	"""Resizes the given box to the given size"""
	width = box[2]
	height = box[3]
	diffX = size - width
	diffY = size - height
	
	copy = []
	
	copy.append(box[0] - (diffX / 2))
	copy.append(box[1] - (diffY / 2))
	copy.append(box[2] + diffX)
	copy.append(box[3] + diffY)
	
	return tuple(copy)

def millis():
	"""Returns the current system time in milliseconds"""
	return int(round(time.time() * 1000))

def clockStringFromSecs(secs):
	"""Formats a time in seconds as a digital clock string"""
	secs = int(secs)
	mins = int(secs / 60)
	secs -= mins * 60
	hours = int(mins / 60)
	mins -= hours * 60
	timeStr = ("0" if hours < 10 else "") + str(hours) + ":" + ("0" if mins < 10 else "") + str(mins) + ":" + ("0" if secs < 10 else "") + str(secs)
	return timeStr
