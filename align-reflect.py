import micasense
import micasense.utils
import micasense.plotutils as plotutils
import micasense.metadata as metadata
import os, glob
import matplotlib.pyplot as plt
import micasense.capture as capture
import multiprocessing
import micasense.image as image
import micasense.imageutils as imageutils

exiftoolPath = None
if os.name == 'nt':
    exiftoolPath = 'C:/exiftool/exiftool.exe'

imagesPath = os.path.join('.', 'MicasenseImagesPanels')
#allImages = os.listdir(imagesPath)
PanelNames = glob.glob( os.path.join('.', 'MicasenseImagesPanels', 'IMG_0009_*.tif') )

for panelName in PanelNames:
	meta = metadata.Metadata(panelName, exiftoolPath)
	img = image.Image(panelName)
	#print(dir(meta))
	print("Panel: {}".format(panelName))
	print('Band: {} / {}nm'.format(img.meta.band_name(), img.meta.bandwidth()))
#%%
# get image metadata
# for imageName in allImages:
# 	meta = metadata.Metadata(imageName, exiftoolPath)
# 	imageRaw=plt.imread(imageName)
# 	radianceimage, _, _, _ = micasense.utils.raw_image_to_radiance(meta, imageRaw)
# 	#plotutils.plotwithcolorbar(radianceimage)
# 	print(dir(meta))
# 	print('{0} {1} firmware version: {2}'.format(meta.camera_make(), meta.camera_model(), meta.firmware_version()))
#
# 	#TODO update the rest
# 	print('Exposure Time: {0} seconds'.format(meta.get_item('EXIF:ExposureTime')))
# 	print('Imager Gain: {0}'.format(meta.get_item('EXIF:ISOSpeed')/100.0))
# 	print('Size: {0}x{1} pixels'.format(meta.get_item('EXIF:ImageWidth'),meta.get_item('EXIF:ImageHeight')))
# 	print('Band Name: {0}'.format(meta.band_namebandName()))
# 	print('Center Wavelength: {0} nm'.format(meta.get_item('XMP:CentralWavelength')))
# 	print('Bandwidth: {0} nm'.format(meta.get_item('XMP:WavelengthFWHM')))
# 	print('Capture ID: {0}'.format(meta.get_item('XMP:CaptureId')))
# 	print('Flight ID: {0}'.format(meta.get_item('XMP:FlightId')))
# 	print('Focal Length: {0}'.format(meta.get_item('XMP:FocalLength')))

#%%
##########################################################
#				Alignment	WIP
######################################################
imagePath = os.path.join('.','Micasenseimages')
imageNames = glob.glob(os.path.join(imagePath,'IMG_0013_*.tif'))
capture = capture.Capture.from_filelist(imageNames)
panel_reflectance_by_band = [0.67, 0.69, 0.68, 0.61, 0.67] #RedEdge band_index order
panel_irradiance = panelCap.panel_irradiance(panel_reflectance_by_band)
capture.plot_undistorted_reflectance(panel_irradiance)
#
print("Alinging images. Depending on settings this can take from a few seconds to many minutes")
# Increase max_iterations to 1000+ for better results, but much longer runtimes
warp_matrices, alignment_pairs = imageutils.align_capture(capture, max_iterations=100)

print("Finished Aligning, warp matrices:")
for i,mat in enumerate(warp_matrices):
    print("Band {}:\n{}".format(i,mat))
# ## Crop Aligned Images
# After finding image alignments we may need to remove pixels around the edges which aren't present in every image in the capture.  To do this we use the affine transforms found above and the image distortions from the image metadata.  OpenCV provides a couple of handy helpers for this task in the  `cv2.undistortPoints()` and `cv2.transform()` methods.  These methods takes a set of pixel coordinates and apply our undistortion matrix and our affine transform, respectively.  So, just as we did when registering the images, we first apply the undistortion process the coordinates of the image borders, then we apply the affine transformation to that result. The resulting pixel coordinates tell us where the image borders end up after this pair of transformations, and we can then crop the resultant image to these coordinates.
# %%
dist_coeffs = []
cam_mats = []
# create lists of the distortion coefficients and camera matricies
for i,img in enumerate(capture.images):
    dist_coeffs.append(img.cv2_distortion_coeff())
    cam_mats.append(img.cv2_camera_matrix())
# cropped_dimensions is of the form:
# (first column with overlapping pixels present in all images,
#  first row with overlapping pixels present in all images,
#  number of columns with overlapping pixels in all images,
#  number of rows with overlapping pixels in all images   )
cropped_dimensions = imageutils.find_crop_bounds(capture.images[0].size(),
                                                 warp_matrices,
                                                 dist_coeffs,
                                                 cam_mats)
# %% markdown
# ## Visualize Aligned Images
#
# Once the transformation has been found, it can be verified by composting the aligned images to check alignment. The image 'stack' containing all bands can also be exported to a multi-band TIFF file for viewing in extrernal software such as QGIS.  Useful componsites are a naturally colored RGB as well as color infrared, or CIR.
# %%
im_aligned = imageutils.aligned_capture(warp_matrices, alignment_pairs, cropped_dimensions)
# Create a normalized stack for viewing
im_display = np.zeros((im_aligned.shape[0],im_aligned.shape[1],5), dtype=np.float32 )

for i in range(0,im_aligned.shape[2]):
    im_display[:,:,i] =  imageutils.normalize(im_aligned[:,:,i])

rgb = im_display[:,:,[2,1,0]]
cir = im_display[:,:,[3,2,1]]
fig, axes = plt.subplots(1, 2, figsize=(16,16))
plt.title("Red-Green-Blue Composite")
axes[0].imshow(rgb)
plt.title("Color Infrared (CIR) Composite")
axes[1].imshow(cir)
plt.show()
