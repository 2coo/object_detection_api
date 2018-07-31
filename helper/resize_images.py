import os
from PIL import Image
import shutil
import xml.etree.ElementTree as ET
import sys

IMAGE_DIR = None
MAX_SIZE = 2048

if len(sys.argv) > 1:
	IMAGE_DIR = sys.argv[1]
else:
	print('please, insert resize images directory')
	exit()

if len(sys.argv) > 2:
	MAX_SIZE = sys.argv[2]

def resize_img(image_path):
	img = Image.open(image_path)
	if img.width > MAX_SIZE or img.height > MAX_SIZE:		
		print(image)
		# image_name = os.path.basename(image_path)
		filename = os.path.splitext(image_path)[0]
		exten = os.path.splitext(image_path)[1]
		if img.width >  img.height:
			dwidth = MAX_SIZE
			proportion =  dwidth / int(img.width)
			dheight = int(int(img.height) * proportion)
		else:
			dheight = MAX_SIZE
			proportion =  dheight / int(img.height)
			dwidth = int(int(img.width) * proportion)

		img = img.resize((dwidth, dheight))
		img.save(image_path)

		tree = ET.parse(filename+'.xml')
		root = tree.getroot()

		root.find('size')[0].text = str(int(dwidth))
		root.find('size')[1].text = str(int(dheight))
		for member in enumerate(root.findall('object')):
			member[4][0].text = str(int(int(member[4][0].text) * proportion))
			member[4][1].text = str(int(int(member[4][1].text) * proportion))
			member[4][2].text = str(int(int(member[4][2].text) * proportion))
			member[4][3].text = str(int(int(member[4][3].text) * proportion))

		tree.write(filename+'.xml')

if __name__ == '__main__':
	images = [os.path.join(IMAGE_DIR, image) for image in os.listdir(IMAGE_DIR) if not image.startswith('.') and image.endswith(('.jpg','.JPG','.png','.jpeg','.JPEG','.PNG'))]
	for image in images:
		resize_img(image)

	

