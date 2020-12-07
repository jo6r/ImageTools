"""
Export EXIF metadata from image to json files.

CLI help
python exif_exporter.py -h

Exif Exporter

positional arguments:
  source       path to source folder

optional arguments:
  -h, --help   show this help message and exit

Usage:
python exif_exporter.py /albums/rivers
python exif_exporter.py /albums/rivers
"""

import argparse
import concurrent.futures
import datetime
import json

from exif.ExifTools import ExifTools, NoExifError
from image.ImageTools import ImageTools
from utils.FileUtils import FileUtils

EXT_FILTER = [".jpg", ".png"]
VERSION = 1.1


def main():
    begin_time = datetime.datetime.now()
    parser = argparse.ArgumentParser(description='Exif Exporter {}'.format(VERSION))
    parser.add_argument('source', help='path to source folder', type=str)
    arguments = parser.parse_args()
    # print(arguments)

    list_files = FileUtils.get_list_of_files_filter(arguments.source, EXT_FILTER)
    print("Processing folder {}".format(arguments.source))
    print("Input file: {}".format(len(list_files)))

    # Default value of max_workers is changed to min(32, os.cpu_count() + 4).
    # This default value preserves at least 5 workers for I/O bound tasks
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        futures = []
        for file in list_files:
            futures.append(executor.submit(json_export, file))

        for future in concurrent.futures.as_completed(futures):
            # print("{} Task complete {}".format(file, future.result()))
            pass

    print("Execution time: {}".format(datetime.datetime.now() - begin_time))


def json_export(image) -> bool:
    try:
        exif: ExifTools = ExifTools.from_exif(ImageTools(image).get_exif())

        if exif:
            filename = image + ".exif.json"
            with open(filename, "w") as f:
                f.write(json.dumps(exif.__dict__))
        return True
    except NoExifError as e:
        print("{} {}".format(image, str(e)))
        return False


if __name__ == '__main__':
    main()
