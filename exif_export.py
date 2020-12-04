"""
Export EXIF metadata from image to json files.

CLI help
python exif_export.py -h

Exif Export

positional arguments:
  source       path to source folder

optional arguments:
  -h, --help   show this help message and exit

Usage:
python exif_export.py /albums/rivers
python exif_export.py /albums/rivers
"""

import argparse
import datetime
import json

from exif.ExifTools import ExifTools, NoExifError
from image.ImageTools import ImageTools
from utils.FileUtils import FileUtils

EXT_FILTER = [".jpg", ".png"]
VERSION = 1.0


def main():
    begin_time = datetime.datetime.now()
    parser = argparse.ArgumentParser(description='Exif Export {}'.format(VERSION))
    parser.add_argument('source', help='path to source folder', type=str)
    arguments = parser.parse_args()
    print(arguments)

    list_files = FileUtils.get_list_of_files_filter(arguments.source, EXT_FILTER)
    print("Processing folder {}".format(arguments.source))
    print("Input files: {}".format(len(list_files)))

    for image in list_files:
        if not FileUtils.file_exists(image):
            print("ERROR: File Not Found. {}".format(image))
            break  # end of loop
        print(image)
        try:
            exif: ExifTools = ExifTools.from_exif(ImageTools(image).get_exif())

            if exif:
                filename = image + ".exif.json"
                with open(filename, "w") as f:
                    f.write(json.dumps(exif.__dict__))
        except NoExifError as e:
            print(str(e))

    print("Execution time: {}".format(datetime.datetime.now() - begin_time))


if __name__ == '__main__':
    main()


