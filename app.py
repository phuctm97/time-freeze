import cv2
from image_processing import process_images
from utils import absolute_path

# samples data
sample_boat = ['samples/stitching/boat{}.jpg'.format(i) for i in range(1, 7)]
sample_newspaper = ['samples/stitching/newspaper{}.jpg'.format(i) for i in range(1, 5)]
sample_building_1 = ['samples/stitching/a{}.png'.format(i) for i in range(1, 4)]
sample_building_2 = ['samples/stitching/building{}.jpg'.format(i) for i in range(1, 3)]
sample_landscape = ['samples/stitching/b{}.png'.format(i) for i in range(1, 3)]
sample_people = ['samples/stitching/people{}.jpg'.format(i) for i in range(1, 4)]
sample_letter = ['samples/stitching/letter{}.jpg'.format(i) for i in range(1, 4)]

# load/capture images
images = [cv2.imread(src) for src in sample_letter]

# process images
succeeded, result_filename = process_images(images, 130)
if succeeded:
    print('Generated panorama "{}" and uploaded to facebook successfully'.format(absolute_path(result_filename)))
