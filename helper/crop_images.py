import os
from PIL import Image
import xml.etree.ElementTree as ET
import shutil

MAX_SIZE = 2048

import sys
IMAGE_DIR = None
if len(sys.argv) > 1:
    IMAGE_DIR = sys.argv[1]
else:
	print('Please, insert crop image folder')
	exit()
if len(sys.argv) > 2:
	MAX_SIZE = sys.argv[2]

def create_xml(folder, filename, path, width, height, objects):
	template = """<annotation>
  <folder>{0}</folder>
  <filename>{1}</filename>
  <path>{2}</path>
  <source>
    <database>Unknown</database>
  </source>
  <size>
    <width>{3}</width>
    <height>{4}</height>
    <depth>3</depth>
  </size>
  <segmented>0</segmented>
  {5}
</annotation>""".format(folder, filename, path, width, height, objects)

	return template



def crop_image_with_annotation(image):
	im = Image.open(image)
	filename = os.path.splitext(image)[0]
	file_format = os.path.splitext(image)[1]
	if im.width <= MAX_SIZE and im.height <= MAX_SIZE:
		pass
		# shutil.copy(image, RESULT_DIR)
		# shutil.copy(filename+'.xml', RESULT_DIR)
	else:
		print(image)
		### BRANDS
		tree = ET.parse(filename+'.xml')
		root = tree.getroot()

		crop_locations = []
		xml_objects = []

		for index, member in enumerate(root.findall('object')):
			x_min = int(member[4][0].text)
			y_min = int(member[4][1].text)
			x_max = int(member[4][2].text)
			y_max = int(member[4][3].text)
			
			middle_point_x = (x_min + x_max) / 2
			middle_point_y = (y_min + y_max) / 2

			crop_x_min = int(max(0, middle_point_x - (MAX_SIZE / 2)))
			crop_y_min = int(max(0, middle_point_y - (MAX_SIZE / 2)))
			crop_x_max = int(min(crop_x_min+MAX_SIZE, im.width))
			crop_y_max = int(min(crop_y_min+MAX_SIZE, im.height))
			crop_locations.append({'xmin': crop_x_min, 'ymin': crop_y_min, 'xmax': crop_x_max, 'ymax': crop_y_max, 'objects':[{'id': index, 'name': member[0].text, 'xmin': x_min - crop_x_min, 'ymin': y_min - crop_y_min, 'xmax': x_max - crop_x_min, 'ymax': y_max -  crop_y_min}]})
		

		for crop_location in crop_locations:
			for index, member in enumerate(root.findall('object')):
				x_min = int(member[4][0].text)
				y_min = int(member[4][1].text)
				x_max = int(member[4][2].text)
				y_max = int(member[4][3].text)
				if crop_location['xmin'] <= x_min and crop_location['ymin'] <= y_min and crop_location['xmax'] >= x_max and crop_location['ymax'] >= y_max and not {'id': index, 'name': member[0].text, 'xmin': x_min - crop_location['xmin'], 'ymin': y_min - crop_location['ymin'], 'xmax': x_max - crop_location['xmin'], 'ymax': y_max -  crop_location['ymin']} in crop_location['objects']:
					crop_location['objects'].append({'id': index, 'name': member[0].text, 'xmin': x_min - crop_location['xmin'], 'ymin': y_min - crop_location['ymin'], 'xmax': x_max - crop_location['xmin'], 'ymax': y_max -  crop_location['ymin']})
		# else:
		# 	crop_locations.append({'xmin': crop_x_min, 'ymin': crop_y_min, 'xmax': crop_x_max, 'ymax': crop_y_max, 'objects':[{'id': index, 'name': member[0].text, 'xmin': x_min - crop_x_min, 'ymin': y_min - crop_y_min, 'xmax': x_max - crop_x_min, 'ymax': y_max -  crop_y_min}]})
		template = """<object>
	<name>{0}</name>
	<pose>Unspecified</pose>
	<truncated>0</truncated>
	<difficult>0</difficult>
	<bndbox>
		<xmin>{1}</xmin>
		<ymin>{2}</ymin>
		<xmax>{3}</xmax>
		<ymax>{4}</ymax>
	</bndbox>
</object>"""
		# print(crop_locations)
		sorted_by_objects = sorted(crop_locations, key = lambda crop_location: len(crop_location['objects']), reverse=True)
		# print(sorted_by_objects)
		# for crop in sorted_by_objects:
		# 	print("####")
		# 	print(crop)
		object_already_in_image = []

		split_count = 1
		for crop_location in sorted_by_objects:
			objects = ''
			if any([False if obj['id'] in object_already_in_image else True for obj in crop_location['objects']]):
				for index, obj in enumerate(crop_location['objects']):
					object_already_in_image.append(obj['id'])
					objects += template.format(obj['name'], obj['xmin'], obj['ymin'], obj['xmax'], obj['ymax'])
					if index < len(crop_location['objects'])-1:
						objects+='\n'
				cropped_img = im.crop((crop_location['xmin'], crop_location['ymin'], crop_location['xmax'], crop_location['ymax']))
				xml_string = create_xml('images', os.path.basename(filename) + '_'+str(split_count)+file_format, os.path.join('images', os.path.basename(filename) + '_'+str(split_count)+file_format), im.width, im.height, objects)
				cropped_img.save(filename + '_'+str(split_count)+file_format)
				xml_file = open(filename + '_'+str(split_count)+'.xml', 'w')
				xml_file.write(xml_string)
				xml_file.close()
				split_count+=1
	os.remove(image)
	os.remove(filename+'.xml')



if __name__ == '__main__':
	if IMAGE_DIR:
		images = [os.path.join(IMAGE_DIR,image) for image in os.listdir(IMAGE_DIR) if not image.startswith('.') and image.endswith(('.jpg','.JPG','.png','.PNG','.jpeg'))]
		for image in images:
			crop_image_with_annotation(image)