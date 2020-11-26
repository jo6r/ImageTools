from PIL import Image, ExifTags

from utils.FileUtils import FileUtils


class ImageTools:
    def __init__(self, path: str) -> None:
        self._path = path
        self._open()

    def _open(self):
        try:
            self._img: Image = Image.open(self._path)
        except Exception as e:
            print("Error during opening image {}".format(str(e)))

    def get_path_to_image(self) -> str:
        return self._path

    def get_exif_metadata(self):
        for key, value in self._img.getexif().items():
            print(self._get_labeled_tag(key))

            if isinstance(value, bytes):
                # print(value.decode("utf-8"))
                print(value.decode("latin-1"))
            else:
                print(value)
            print(" ")

    def _get_labeled_tag(self, tag: int):
        try:
            return ExifTags.TAGS[tag]
        except KeyError:
            return tag

    def save_no_exif(self):
        try:
            # TODO save with threading (concurrent.futures.ThreadPoolExecutor)
            new = Image.new(self._img.mode, self._img.size)
            new.putdata(list(self._img.getdata()))
            new.save(self.get_path_to_image())  # without exif metadata
            print("Done: {}".format(self.get_path_to_image()))
        except Exception as e:
            print("ERROR during saving image. {}".format(str(e)))
