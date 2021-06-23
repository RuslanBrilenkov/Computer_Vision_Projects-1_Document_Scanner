import numpy as np
import cv2
from skimage.filters import threshold_local
import math
from scipy import ndimage
print("Imports are Done!")


class Scanner:
	"""
	A class to scan (and perform related operations on) a document.

	...

	Attributes
	----------
	img : str
		image name of the document/photo.

	Methods
	-------
	Resize_Image(final_height, img):
		Resizes the image by preserving its axis ratio.

	Scan_View():
		Transforms the image/document view into B&W (proper scanned colour scheme).

	Rotation():
		Automatically rotates the image/document to a straight (top-down, face-on) view.

	"""

	def __init__(self, img):
		"""
		Constructs all the necessary attributes for the person object.

		Parameters
		----------
		img : str
			image name of the document/photo

		Returns
		-------
		None
		"""
		
		self.img = img
		
	def Resize_Image(self, final_height, img):
		"""
		Resizes the image by preserving its axis ratio. 

		An argument 'img' can be either a string or an image array itself.

		Parameters
		----------
		img : str/array
			image name (image array) of the document/photo
		final_height : int 
			final height to resize an image to (in pixels)

		Returns
		-------
		Resized image (array)
		"""

		if isinstance(img, str):
			print("This is string!")
			img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
		else:
			print("This is not string!")
			print(type(img))
			img = img
		# Optional - resizing an image by preserving its aspect ratio
		# percentage by which we resize our image (based on the hight)
		height_ratio = final_height / img.shape[0]
		#calculate the ratio of original dimensions
		height, width = int(img.shape[0] * height_ratio), int(img.shape[1] * height_ratio)
		# resizing our image to the desired size
		im_res = cv2.resize(img, (width, height))
		cv2.imshow("Resized", im_res)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return im_res
	
	def Scan_View(self, save_collage=False, resize_collage=True, resize_height=500):
		"""
		Transforms an image/document view into B&W view (proper scanned colour scheme).

		Optionally, saves and resizes a collage with the original and scanned images.

		Parameters
		----------
		save_collage : bool
			flag to save the collage
		resize_collage : bool
			flag to resize the collage
		resize_height : int (default = 500)
			final height to resize an image to (in pixels)

		Returns
		-------
		Resized image (array)
		"""

		print("Scanned View")
		# read the original image, copy it,
		# apply threshold to "scannify" it
		image = cv2.imread(self.img)
		orig = image.copy()
		
		# convert our image to grayscale, apply threshold
		# to create scanned paper effect
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		thr = threshold_local(image, 11, offset = 10, method = "gaussian")
		image = (image > thr).astype("uint8") * 255

		# show the original image and the edge detected image
		#cv2.imshow("orig", orig)
		#cv2.imshow("Scanned", image)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		print(np.shape(orig), np.shape(image))
		if save_collage:
			# Saving a nice horizontal collage
			horiz_conc = np.concatenate((orig[:,:,1], image), axis=1)
			if resize_collage:
				# Optional - resizing this collage to take less space
				horiz_conc = self.Resize_Image(resize_height, horiz_conc)
			# Saving the horizontal collage
			cv2.imwrite('Part_scan_view.png', horiz_conc)
		else:
			# Saving an image itself
			cv2.imwrite('Part_scan_view.png', image)
		return image

	def Rotation(self, save_rotated=False, resize_height=500):
		"""
		Rotate an image/document view for a face-on view (view from the top).

		Optionally, saves and resizes a collage with the original and scanned images.

		Parameters
		----------
		save_rotated : bool
			flag to save the rotated image
		resize_height : int (optional, default = 500)
			final height to resize an image to (in pixels)

		Returns
		-------
		Rotated image (array)
		"""

		print("Rotation")
		# read the original image, copy it,
		# rotate it
		image = cv2.imread(self.img)
		orig = image.copy()
		
		image = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
		img_edges = cv2.Canny(image, 100, 100, apertureSize=3)
		lines = cv2.HoughLinesP(img_edges, rho=1, theta=np.pi / 180.0, threshold=160, minLineLength=100, maxLineGap=10)
		
		# calculate all the angles:
		angles = []
		for [[x1, y1, x2, y2]] in lines:
			# Drawing Hough lines
			#cv2.line(image, (x1, y1), (x2, y2), (128,0,0), 30)
			angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
			angles.append(angle)
			
		# average angles
		median_angle = np.median(angles)
		# actual rotation
		image = ndimage.rotate(image, median_angle)

		# Resize the rotated image to the old height
		#image = self.Resize_Image(resize_height , image)
		#print(np.shape(image))
		# show the original and rotated image
		#cv2.imshow("orig", orig)
		cv2.imshow("Rotated", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		print(np.shape(orig), np.shape(image))
		if save_rotated:
			# Saving an image itself
			cv2.imwrite('Part_rotation.png', image)
		return image
	
	
if __name__=="__main__":
	# Defining the image name
	img = "21_Lesson_21th_Century.jpeg"
	
	# Calling the scanner class
	scan = Scanner(img)
	
	# Optional - resizing image
	#scan.Resize_Image(512, img)
	
	# Scanning the image -> B&W scheme
	scanned_im = scan.Scan_View(save_collage=False, resize_collage=False, resize_height =500)

	# Testing my docstrings:
	#help(Scanner)
	
	scanned_im = "Part_scan_view.png"
	scan = Scanner(scanned_im)
	rotated_im = scan.Rotation(save_rotated=True, resize_height=500)
	
