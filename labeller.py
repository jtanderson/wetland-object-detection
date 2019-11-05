import os, sys
import glob
from multiprocessing import Process
import numpy as np
from skimage.filters import scharr, sobel, roberts, prewitt
from skimage.feature import canny
from skimage.color import rgb2gray
from scipy import ndimage as ndi

import matplotlib.pyplot as plt
import imageio

import PyQt5.QtCore as qtc
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QFileDialog, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QColor
#from PyQt5.QtGui.QColor


class App(QMainWindow):
	def __init__(self):
		super(App, self).__init__()
		self.title = 'PyQt5 image - pythonspot.com'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.label = QLabel(self)
		self.label.mousePressEvent = self.label_object

		self.central_widget = QWidget()
		self.setCentralWidget(self.central_widget)
		self.layout = QVBoxLayout(self.central_widget)
		self.layout.addWidget(self.label)
		self.label.move(0, 500)

		self.edge_type = "scharr"
		self.edge_folders = {}
		self.qim = 0
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		numImages = 10
		firstNonPanelImg = 13
		# Create folder selector widget
		dlg = QFileDialog()
		dlg.setFileMode(QFileDialog.Directory)
		#filenames = QStringList()
		dir_names = []
		if dlg.exec_():
			dir_names = dlg.selectedFiles()
		print(dir_names)

		button = QPushButton('Next Image', self)
		#button.move(100,70)
		button.clicked.connect(self.next_image_clicker)
		self.load_images(dir_names)
		self.show()

	def load_images(self, dir_names):
		for dir in dir_names:
			self.current_edges_folder = dir + "-" + self.edge_type + "edges"
			self.edge_folders[self.current_edges_folder] = []

			if self.current_edges_folder not in self.edge_folders:
				self.edge_folders.append(self.current_edges_folder)
			directory = os.fsencode(dir)
			for file in os.listdir(directory):
				file_name = os.fsdecode(file)
				im_type = file_name.split('.')[-1]
				img_path = f"{dir}/{file_name}"
				# print("name", file_name)
				# print("dir", dir)
				out_file_name = file_name.split('.')[0] + "-edges." + im_type
				out_image_path = os.path.join(dir+"-" + self.edge_type + "edges", out_file_name)
				if not os.path.isdir(dir+"-" + self.edge_type + "edges"):
					os.mkdir(dir+"-" + self.edge_type + "edges")
				if not os.path.isfile(out_image_path):
					im_edges = self.edges(img_path)
					imageio.imwrite(out_image_path, im_edges)
				if out_image_path not in self.edge_folders[self.current_edges_folder]:
					self.edge_folders[self.current_edges_folder].append(out_image_path)
		# for key in self.edge_folders.keys():
		# 	print(f"{key}: {self.edge_folders[key]}\n")

	def edges(self, image_path):
		#edges = sobel(gray)*256
		img = imageio.imread(image_path)
		gray = rgb2gray(img)
		# * 255 so that it's not scaled between 0-1 for when it converts to uint8
		if self.edge_type == "canny":
			edges = canny(gray, sigma=6)
		if self.edge_type == "sobel":
			edges = sobel(gray)*256
		if self.edge_type == "scharr":
			edges = scharr(gray)*256
		if self.edge_type == "roberts":
			edges = roberts(gray)*256
		if self.edge_type == "prewitt":
			edges = prewitt(gray)*256
		#fill_objects = ndi.binary_fill_holes(edges)
		return edges.astype('uint8')

	@qtc.pyqtSlot()
	def next_image_clicker(self):
		self.show_next_img()

	def show_next_img(self):
		# print(f"current folder: {self.current_edges_folder}\nfiles: {self.edge_folders[self.current_edges_folder]}\n")
		open_image_path = self.edge_folders[self.current_edges_folder].pop()
		print(f"current folder: {self.current_edges_folder}\nfile: {open_image_path}")
		self.qim = QImage(open_image_path)
		self.update_qpix()

	def label_object(self , event):
		self.clicked = True
		x = event.pos().x()
		y = event.pos().y()
		print(f"{x}, {y}")
		self.floodfill_queue(x, y)

	def floodfill_queue(self, x, y):
		qim_max = self.qim.size().width()
		while_tol = 15
		q = [(x, y)]
		touched = []
		while q and len(touched) < 10000:
			n = q.pop(0)
			x = n[0]
			y = n[1]
			for new_point in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
				if x > 0 and y > 0 and x <qim_max and y < qim_max and new_point not in touched:
					c = self.get_pix_color(new_point[0], new_point[1])
					if c[0] <= while_tol and c[1] <= while_tol and c[2] <= while_tol:
						#print(f"color at {x} {y} is {c}")
						self.set_pix_color(new_point[0], new_point[1], [255, 255, 255])
						touched.append((x, y))
						q.append(new_point)
		# if not q:
		# 	for point in touched:
		# 		self.set_pix_color(point[0], point[1], [255, 255, 255])
		# else:
		# 	print("the point you clicked on isn't inside a closed box")
		self.update_qpix()

	def write_Qimage(self, img, name):
		#img should be a pyqt5 qimage, name is the filename
		imtype = 'jpg' # or 'jpg'
		out_folder_path = os.path.join('.', self.out_folder_name)
		if not os.path.isdir(out_folder_path):
			os.mkdir(out_folder_path)
		out_file_name = name.split('.')[0] + "edges." + imtype
		out_file_path = os.path.join('.', self.out_folder_name, out_file_name)
		img.save(out_file_path, quality = -1)

	def write_image(self, img, name):
		#img should be a pyqt5 qimage, name is the filename
		imtype = 'jpg' # or 'jpg'
		out_folder_path = os.path.join('.', self.out_folder_name)
		if not os.path.isdir(out_folder_path):
			os.mkdir(out_folder_path)
		out_file_name = name.split('.')[0] + "masks." + imtype
		out_file_path = os.path.join('.', self.out_folder_name, out_file_name)
		imageio.imwrite(out_file_path, img)

	def display_image(self, img):
		plt.imshow(img)

	def get_pix_color(self, x, y):
		c = self.qim.pixel(x,y)
		colors = QColor(c).getRgb()[:-1]
		#print (f"({x},{y}) = {colors}")
		return colors

	def set_pix_color(self, x, y, c):
		color = QColor(c[0], c[1], c[2])
		self.qim.setPixel(x, y, color.rgb())

	def update_qpix(self):
		self.pixmap = QPixmap(self.qim)
		self.label.setPixmap(self.pixmap)
		self.resize(self.pixmap.width(), self.pixmap.height())
		self.show()

		#fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(32, 32), sharex=True, sharey=True)
		# ax1.imshow(scharr_edges, cmap=plt.cm.gray)
		# ax1.axis('off')
		# ax1.set_title('scharr', fontsize=20)
		#
		# ax2.imshow(img, cmap=plt.cm.gray)
		# ax2.axis('off')
		# ax2.set_title('image', fontsize=20)
		#
		# fig.tight_layout()
		# plt.show()
		# print("test")
		# print(dir(fill_objects))
		# print(type(fill_objects))
		#return fill_objects

if __name__ == '__main__':
	app = QApplication(sys.argv)

	ex = App()

	sys.exit(app.exec_())
