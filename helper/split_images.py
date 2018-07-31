import os
import random
import shutil
import sys

IMAGE_DIR = None

TRAIN_DATA_PROPORTION = 80

if len(sys.argv) > 1:
    IMAGE_DIR = sys.argv[1]
elif not len(sys.argv) > 1:
	print('Please, insert directory which contains images and labels of classes.')
	exit()
if len(sys.argv) > 2:
	TRAIN_DATA_PROPORTION = int(sys.argv[2])
	if TRAIN_DATA_PROPORTION > 100 or TRAIN_DATA_PROPORTION < 1:
		print('TRAIN_DATA_PROPORTION value must be between 0.01 and 1')
		exit()
	TRAIN_DATA_PROPORTION = float(TRAIN_DATA_PROPORTION / 100)
elif not len(sys.argv) > 2:
	print('Please, insert training data proportion')
	exit()


if __name__ == '__main__':
	if not os.path.exists(os.path.join(IMAGE_DIR, 'total_images')):
		os.makedirs(os.path.join(IMAGE_DIR, 'total_images'))
	else:
		shutil.rmtree(os.path.join(IMAGE_DIR, 'total_images'))	
	if IMAGE_DIR:
		IMAGE_DIR = os.path.realpath(IMAGE_DIR)
		sub_dirs = [directory for directory in os.listdir(IMAGE_DIR) if os.path.isdir(os.path.join(IMAGE_DIR,directory))]
		for sub_dir in sub_dirs:
			print(sub_dir)
			image_list = [image for image in os.listdir(os.path.join(IMAGE_DIR,sub_dir)) if image.endswith(('.jpeg','.jpg','.png','.PNG','.JPG','JPEG')) and not image.startswith('.')]
			print(len(image_list))
			print(TRAIN_DATA_PROPORTION)
			train_data = random.sample(image_list,int(len(image_list)*TRAIN_DATA_PROPORTION))
			test_data = list(set(image_list)-set(train_data))
			
			if not os.path.exists(os.path.join(IMAGE_DIR, sub_dir,'train')):
				os.makedirs(os.path.join(IMAGE_DIR, sub_dir,'train'))
			if not os.path.exists(os.path.join(os.path.split(IMAGE_DIR)[0], 'final_data','train')):
				os.makedirs(os.path.join(os.path.split(IMAGE_DIR)[0], 'final_data','train'))




			if not os.path.exists(os.path.join(IMAGE_DIR, sub_dir,'test')):
				os.makedirs(os.path.join(IMAGE_DIR, sub_dir,'test'))
			if not os.path.exists(os.path.join(os.path.split(IMAGE_DIR)[0], 'final_data','test')):
				os.makedirs(os.path.join(os.path.split(IMAGE_DIR)[0], 'final_data','test'))

			### COPYING
			for train_image in train_data:
				shutil.copy(os.path.join(IMAGE_DIR, sub_dir, train_image), os.path.join(IMAGE_DIR, sub_dir, 'train', train_image))
				shutil.copy(os.path.join(IMAGE_DIR, sub_dir, os.path.splitext(train_image)[0]+'.xml'), os.path.join(IMAGE_DIR, sub_dir, 'train', os.path.splitext(train_image)[0]+'.xml'))
				shutil.copy(os.path.join(IMAGE_DIR, sub_dir, train_image), os.path.join(os.path.split(IMAGE_DIR)[0], 'final_data', 'train', train_image))
				shutil.copy(os.path.join(IMAGE_DIR, sub_dir, os.path.splitext(train_image)[0]+'.xml'), os.path.join(os.path.split(IMAGE_DIR)[0], 'final_data', 'train', os.path.splitext(train_image)[0]+'.xml'))

			for test_image in test_data:
				shutil.copy(os.path.join(IMAGE_DIR, sub_dir, test_image), os.path.join(IMAGE_DIR, sub_dir, 'test', test_image))
				shutil.copy(os.path.join(IMAGE_DIR, sub_dir, os.path.splitext(test_image)[0]+'.xml'), os.path.join(IMAGE_DIR, sub_dir, 'test', os.path.splitext(test_image)[0]+'.xml'))
				shutil.copy(os.path.join(IMAGE_DIR, sub_dir, test_image), os.path.join(os.path.split(IMAGE_DIR)[0], 'final_data', 'test', test_image))
				shutil.copy(os.path.join(IMAGE_DIR, sub_dir, os.path.splitext(test_image)[0]+'.xml'), os.path.join(os.path.split(IMAGE_DIR)[0], 'final_data', 'test', os.path.splitext(test_image)[0]+'.xml'))


	# for index, image in enumerate(all_data):
	# 	if not image.startswith('.'):
	# 		filename = os.path.splitext(image)[0]
	# 		# print(filename)
	# 		extension = os.path.splitext(image)[1]
	# 		shutil.copy('images/'+xclass+'/'+image, 'images/'+xclass+'/train')
	# 		shutil.copy('images/'+xclass+'/'+filename+'.xml', 'images/'+xclass+'/train')