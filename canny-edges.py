import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import feature
from skimage.filters import roberts, sobel, scharr, prewitt
from skimage.color import rgb2gray
from scipy import ndimage as ndi
from pynput.mouse import Listener

listener = 0
def on_move(x, y):
	x = 1
	#print("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
	if pressed:
		print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
		if listener:
			listener.stop()
			plt.close()

def on_scroll(x, y, dx, dy):
	x = 1 #print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

numImages = 10
firstNonPanelImg = 13
for i in range(numImages):
	imagePath = os.path.join('.', 'Aligned-iter500')
	imageStr = "img" + str(i + firstNonPanelImg) + "-rgb.jpg"
	# imagePath = os.path.join('.', 'MicasenseImagesPanels')
	# imageStr = "IMG_" + ("0" if i >= 100 else "00") + str(i + firstNonPanelImg) + "_1.tif"
	imageName = os.path.join(imagePath, imageStr)
	print(imageName)
	img = io.imread(imageName)
	gray = rgb2gray(img)

	#edges = feature.canny(gray, sigma=4)
	roberts_edges = roberts(gray)
	sobel_edges = sobel(gray)
	scharr_edges = scharr(gray)
	prewitt_edges = prewitt(gray)
	fill_objects = ndi.binary_fill_holes(roberts_edges)

	fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(32, 32), sharex=True, sharey=True)
	ax1.imshow(scharr_edges, cmap=plt.cm.gray)
	ax1.axis('off')
	ax1.set_title('image', fontsize=20)

	ax2.imshow(roberts_edges, cmap=plt.cm.gray)
	ax2.axis('off')
	ax2.set_title('Canny filter, $\sigma=2$', fontsize=20)

	fig.tight_layout()



	with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
		plt.show()
		listener.join()
	# imtype = 'png' # or 'jpg'
	# outFolderName = "filledEdges" + str(numIterations)
	# outFolderPath = os.path.join('.', outFolderName)
	#
	# if not os.path.isdir(outFolderPath):
	# 	os.mkdir(outFolderPath)
	#
	# outFileName = 'img' + str(i + firstNonPanelImg) + '-edgeFill.'+imtype
	# outFilePath = os.path.join(outFolderPath, outFileNameRGB)
	#
	# print("Writing Images")
	# imageio.imwrite(outFilePath, (255*gamma_corr_rgb).astype('uint8'))
