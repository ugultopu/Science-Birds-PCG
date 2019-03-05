#@title Imports
from sys import argv
import math
import os
from os import listdir
from os.path import isfile, join
from io import BytesIO
import tarfile
import tempfile
from six.moves import urllib

import numpy as np
from PIL import Image

import tensorflow as tf
from structure import OBJmatrix


class DeepLabModel(object):
	"""Class to load deeplab model and run inference."""

	INPUT_TENSOR_NAME = 'ImageTensor:0'
	OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
	INPUT_SIZE = 513
	FROZEN_GRAPH_NAME = 'frozen_inference_graph'

	def __init__(self, tarball_path):
		"""Creates and loads pretrained deeplab model."""
		self.graph = tf.Graph()

		graph_def = None
		# Extract frozen graph from tar archive.
		tar_file = tarfile.open(tarball_path)
		for tar_info in tar_file.getmembers():
			if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
				file_handle = tar_file.extractfile(tar_info)
				graph_def = tf.GraphDef.FromString(file_handle.read())
				break
		tar_file.close()

		if graph_def is None:
			raise RuntimeError('Cannot find inference graph in tar archive.')

		with self.graph.as_default():
			tf.import_graph_def(graph_def, name='')

		self.sess = tf.Session(graph=self.graph)

	def run(self, image):
		"""Runs inference on a single image.

		Args:
			image: A PIL.Image object, raw input image.

		Returns:
			resized_image: RGB image resized from original input image.
			seg_map: Segmentation map of `resized_image`.
		"""
		width, height = image.size
		resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
		target_size = (int(resize_ratio * width), int(resize_ratio * height))
		resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
		batch_seg_map = self.sess.run(
			self.OUTPUT_TENSOR_NAME,
			feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
		seg_map = batch_seg_map[0]
		return resized_image, seg_map

if __name__ == "__main__":
	if len(argv) < 3:
		print("insufficent inputs")
		print("format: [deeplab|gimp] [difficulty:1-4] [file-path]")
	else:
		file_path = argv[3]
		if file_path[-1] != '/':
			file_path += '/'
		difficulty = int(argv[2]) * 20
		model = argv[1]
   
		if model == 'deeplab':
			#@title Select and download models {display-mode: "form"}

			MODEL_NAME = 'xception_coco_voctrainaug'  # @param ['mobilenetv2_coco_voctrainaug', 'mobilenetv2_coco_voctrainval', 'xception_coco_voctrainaug', 'xception_coco_voctrainval']

			_DOWNLOAD_URL_PREFIX = 'http://download.tensorflow.org/models/'
			_MODEL_URLS = {
				'mobilenetv2_coco_voctrainaug':
					'deeplabv3_mnv2_pascal_train_aug_2018_01_29.tar.gz',
				'mobilenetv2_coco_voctrainval':
					'deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz',
				'xception_coco_voctrainaug':
					'deeplabv3_pascal_train_aug_2018_01_04.tar.gz',
				'xception_coco_voctrainval':
					'deeplabv3_pascal_trainval_2018_01_04.tar.gz',
			}
			_TARBALL_NAME = MODEL_NAME+'.tar.gz'

			model_dir = '../training_model/'

			download_path = os.path.join(model_dir, _TARBALL_NAME)

			if not isfile(download_path):

				print('downloading model, this might take a while...')
				urllib.request.urlretrieve(_DOWNLOAD_URL_PREFIX + _MODEL_URLS[MODEL_NAME],
							   download_path)
				print('download completed! loading DeepLab model...')

			MODEL = DeepLabModel(download_path)
			print('model loaded successfully!')


			for pic in pictures:
				jpg = Image.open(file_path+pic)
				resized_im, seg_map = MODEL.run(jpg)
				#setting width and length of matrix
				width = len(seg_map[0])
				height = len(seg_map)
				
				if width > 100:
					interval = math.ceil(width/difficulty)
				if height > 100:
					interval = max(math.ceil(height/difficulty), interval)

				mat = []
				for index,i in enumerate(seg_map):
					tam = []
					if index % interval == 0:
						for index,j in enumerate(i):
							if index % interval == 0:
								tam.append(1 if j != 0 else 0)
						if tam.count(1)>3:
							mat.append(tam)

				for i in range(4 if len(mat)%2 == 0 else 3):
					mat.insert(0,[0 for i in range(len(mat[0]))])
				for i in mat:
					for count in range(3):
						i.append(0)
						i.insert(0,0)

				#generate structures
				OBJmatrix(matrix=mat,name=pic.split('.')[0]+'.xml')
		elif model == "gimp":
			os.system('../shell/main.sh ../shell/ '+file_path)
			svgs = [f 
					for f in listdir(file_path) 
					if f.find('polygon')!= -1 and isfile(join(file_path, f))]
			for svg in svgs:
				OBJmatrix(
					svg_file_path=file_path+svg,
					perimeter=difficulty,
					name = svg.split('-')[0]+'.xml'
				)


