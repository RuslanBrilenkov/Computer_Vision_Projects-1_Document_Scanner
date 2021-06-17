import numpy as np
import cv2
from skimage.filters import threshold_local
import math
from scipy import ndimage
print("Imports are Done!")


class Scanner():
	def Scan_View(self, imname):
		print("Part 1: Scanned View")
		# read the image, find out the ratio of old/new height,
		# copy original image
		image = cv2.imread(imname)
		orig = image.copy()
		height_ratio = 50 / image.shape[0]
		#calculate the ratio of original dimensions
		height, width = int(image.shape[0] * height_ratio), int(image.shape[1] * height_ratio)
		# resizing our image
		# image = cv2.resize(image, (width, height))

		# convert our image to grayscale, apply threshold
		# to Crete scanned paper effect
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		thr = threshold_local(image, 11, offset = 10, method = "gaussian")
		image = (image > thr).astype("uint8") * 255

		# show the original image and the edge detected image
		cv2.imshow("orig", orig)
		cv2.imshow("Scanned", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return image

if __name__=="__main__":
	# Calling the scanner class
	scan = Scanner()
	im = "21_Lesson_21th_Century.jpeg"
	
	scanned_im = scan.Scan_View(im)
	#scan.Rotation(scanned_im)
