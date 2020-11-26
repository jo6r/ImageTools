"""
Remove EXIF metadata from image files.

CLI help
python exif_remover.py -h

Exif Remover

positional arguments:
  source       path to source folder

optional arguments:
  -h, --help   show this help message and exit
  --backup     enable backup images - enable as default
  --no-backup  disable backup images


Usage:
python exif_remover.py /albums/rivers --backup
python exif_remover.py /albums/rivers --no-backup
"""

import argparse
import datetime

from image.ImageTools import ImageTools
from utils.FileUtils import FileUtils

EXT_FILTER = [".jpg", ".png"]
VERSION = 1.0

def main():
    begin_time = datetime.datetime.now()
    parser = argparse.ArgumentParser(description='Exif Remover {}'.format(VERSION))
    parser.add_argument('source', help='path to source folder', type=str)
    parser.add_argument('--backup', dest='backup', action='store_true', help='enable backup images - enable as default')
    parser.add_argument('--no-backup', dest='backup', action='store_false', help='disable backup images')
    parser.set_defaults(backup=True)
    arguments = parser.parse_args()
    print(arguments)

    list_files = FileUtils.get_list_of_files_filter(arguments.source, EXT_FILTER)
    print("Processing folder {}".format(arguments.source))
    print("Input files: {}".format(len(list_files)))
    if arguments.backup:
        print("Backup images is enabled")
    else:
        print("Backup images is disabled")

    for image in list_files:
        if not FileUtils.file_exists(image):
            print("ERROR: File Not Found. {}".format(image))
            break  # end of loop

        if arguments.backup:
            FileUtils.backup_file(image)

        # processing image
        img_tools = ImageTools(image)
        img_tools.save_no_exif()

    print("Execution time: {}".format(datetime.datetime.now() - begin_time))


if __name__ == '__main__':
    main()
