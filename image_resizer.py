"""
Resize image files to max width/height resolution

CLI help
python image_resizer.py -h

Image Resizer

positional arguments:
  source       path to source folder
  max          max resolution (pixels)

optional arguments:
  -h, --help   show this help message and exit
  --backup     enable backup images - enable as default
  --no-backup  disable backup images

Usage:
python image_resizer.py /albums/flowers 2560 --backup
python image_resizer.py /albums/flowers 2560 --no-backup
"""

import argparse
import datetime
import sys

from image.ImageTools import ImageTools
from utils.FileUtils import FileUtils

EXT_FILTER = [".jpg", ".png"]
VERSION = 1.0
LIMITS = (10, 10000)


def main():
    begin_time = datetime.datetime.now()
    parser = argparse.ArgumentParser(description='Image Resizer {}'.format(VERSION))
    parser.add_argument('source', help='path to source folder', type=str)
    parser.add_argument('max', help='max resolution (pixels)', type=int)
    parser.add_argument('--backup', dest='backup', action='store_true', help='enable backup images - enable as default')
    parser.add_argument('--no-backup', dest='backup', action='store_false', help='disable backup images')
    parser.set_defaults(backup=True)
    arguments = parser.parse_args()
    # print(arguments)

    if arguments.max < LIMITS[0] or arguments.max > LIMITS[1]:
        sys.exit("Argument 'max' is out of limits")

    list_images = FileUtils.get_list_of_files_filter(arguments.source, EXT_FILTER)
    print("Processing folder {}".format(arguments.source))
    print("Input files: {}".format(len(list_images)))
    if arguments.backup:
        print("Backup images is enabled")
    else:
        print("Backup images is disabled")

    # counter
    processed_img = 0
    for image in list_images:
        if not FileUtils.file_exists(image):
            print("ERROR: File Not Found. {}".format(image))
            break  # end of loop

        if arguments.backup:
            FileUtils.backup_file(image)

        # TODO process images with threading (concurrent.futures.ThreadPoolExecutor)
        img_tools = ImageTools(image)
        if img_tools.get_width() > img_tools.get_height():
            if img_tools.get_width() > arguments.max:
                print("Processing image: {}".format(img_tools.filepath))
                img_tools.resize_width_keep_aspect_ratio(arguments.max)
                img_tools.save()
                processed_img += 1
        elif img_tools.get_width() < img_tools.get_height():
            if img_tools.get_height() > arguments.max:
                print("Processing image: {}".format(img_tools.filepath))
                img_tools.resize_height_keep_aspect_ratio(arguments.max)
                img_tools.save()
                processed_img += 1

    print("Changed files: {}".format(processed_img))
    print("Execution time: {}".format(datetime.datetime.now() - begin_time))


if __name__ == '__main__':
    main()
