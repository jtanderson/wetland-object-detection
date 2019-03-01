import micasense
import micasense.utils
import micasense.plotutils as plotut
ils
import micasense.metadata as metadata
import os, glob
import matplotlib.pyplot as plt

exiftoolPath = None
if os.name == 'nt':
    exiftoolPath = 'C:/exiftool/exiftool.exe'

imageName = os.path.join('.', 'MicasenseImages', 'IMG_0013_1.tif')

# get image metadata
meta = metadata.Metadata(imageName, exiftoolPath=exiftoolPath)
imageRaw=plt.imread(imageName)
radianceimage, _, _, _ = micasense.utils.raw_image_to_radiance(meta, imageRaw)
plotutils.plotwithcolorbar(radianceimage)
#print(dir(meta))
#print('{0} {1} firmware version: {2}'.format(meta.camera_make(), meta.camera_model(), meta.firmware_version()))

#TODO update the rest
# print('Exposure Time: {0} seconds'.format(meta.get_item('EXIF:ExposureTime')))
# print('Imager Gain: {0}'.format(meta.get_item('EXIF:ISOSpeed')/100.0))
# print('Size: {0}x{1} pixels'.format(meta.get_item('EXIF:ImageWidth'),meta.get_item('EXIF:ImageHeight')))
#print('Band Name: {0}'.format(bandName))
# print('Center Wavelength: {0} nm'.format(meta.get_item('XMP:CentralWavelength')))
# print('Bandwidth: {0} nm'.format(meta.get_item('XMP:WavelengthFWHM')))
# print('Capture ID: {0}'.format(meta.get_item('XMP:CaptureId')))
# print('Flight ID: {0}'.format(meta.get_item('XMP:FlightId')))
# print('Focal Length: {0}'.format(meta.get_item('XMP:FocalLength')))
