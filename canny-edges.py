import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import feature
from scipy import ndimage as ndi

numImages = 10
firstNonPanelImg = 13
for i in range(numImages):
	imagePath = os.path.join('.', 'Aligned-iter250')
	imageStr = "img" + str(i + firstNonPanelImg) + "-rgb.jpg"
	# imagePath = os.path.join('.', 'MicasenseImagesPanels')
	# imageStr = "IMG_" + ("0" if i >= 100 else "00") + str(i + firstNonPanelImg) + "_1.tif"
	imageName = os.path.join(imagePath, imageStr)
	print(imageName)
	img = io.imread(imageName)
	gray = np.sqrt((img*img).sum(-1))

	edges = feature.canny(gray, sigma=7)

	fill_objects = ndi.binary_fill_holes(edges)

	fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(32, 32), sharex=True, sharey=True)
	ax1.imshow(img, cmap=plt.cm.gray)
	ax1.axis('off')
	ax1.set_title('image', fontsize=20)

	ax2.imshow(fill_objects, cmap=plt.cm.gray)
	ax2.axis('off')
	ax2.set_title('Canny filter, $\sigma=2$', fontsize=20)

	fig.tight_layout()

	plt.show()

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
