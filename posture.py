# encoding=utf-8

__author__  = 'cty'
__version__ = '0.1'
__contact__ = 'chentianyu@outlook.com'

import sys, time
from naoqi import ALProxy
import vision_definitions

class Motion:

	# constructor
	def __init__(self, ip='127.0.0.1', port=9559):
		self.motionProxy = ALProxy('ALMotion', ip, port)
		self.postureProxy = ALProxy('ALRobotPosture', ip, port)
		self.camProxy = ALProxy('ALVideoDevice', ip, port)
		resolution = vision_definitions.kQVGA
		colorSpace = vision_definitions.kRGBColorSpace
		self.fps = 15
		self.videoClient = self.camProxy.subscribeCamera('python_client', 0, resolution, colorSpace, self.fps)
		print self.videoClient
		# wake up nao
		self.motionProxy.wakeUp()
		# stand init
		self.postureProxy.goToPosture("StandInit", 0.5)
		# init motion proxy
		self.motionProxy.moveInit()

	# destructor
	def __del__(self):
		self.camProxy.unsubscribe(self.videoClient)
		self.camProxy.setAllParametersToDefault(0)
		# rest, set all stiffness to 0
		self.motionProxy.rest()


	# move head toward a direction
	def swingHead(self, direction, rad):
		# for debug
		print 'head moves %s to angle: %f. ' %(direction, rad)

		if direction == 'vertical':
			self.motionProxy.setAngles('HeadPitch', rad, 0.1)
			# for debug, the angle should be the same
			print 'head vertical angle is: %f. ' %(self.motionProxy.getAngles('HeadPitch', False))
		elif direction == 'horizontal':
			self.motionProxy.setAngles('HeadYaw', rad, 0.1)
			print 'head horizontal angle is: %f. ' %(self.motionProxy.getAngles('HeadYaw', False))

	# take a picture
	def takePicture(self):
		# for debug
		print "takePicture"

		naoImage = self.camProxy.getImageRemote(self.videoClient)

		width = naoImage[0]; height = naoImage[1]
		nchanels = naoImage[2]; array = naoImage[6]

		return array, (height, width, nchanels)

	# turn left or turn right
	def turn(self, rad):
		# for debug
		print 'turning radius %f. ' %(direction, rad)
		self.motionProxy.walkTo(0.0, 0.0, rad)

	def walk(self):
		pass
