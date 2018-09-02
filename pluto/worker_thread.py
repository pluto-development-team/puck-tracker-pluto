__author__ = "Dennis Claußner"

import threading

class WorkerThread(threading.Thread):
	"""This Thread performs the parallelization of the tracking process"""
	def __init__(self, puck, frame, frameCopy, posList, lock):
		threading.Thread.__init__(self)
		self.puck = puck
		self.frame = frame
		self.frameCopy = frameCopy
		self.posList = posList
		self.threadLock = lock
	
	def run(self):
		pos = self.puck.track(self.frame, self.frameCopy, self.threadLock)
		self.threadLock.acquire(1)
		self.posList.append(pos)
		self.threadLock.release()
