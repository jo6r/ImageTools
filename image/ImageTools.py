from PIL import Image

from utils.FileUtils import FileUtils


class ImageTools:
    def __init__(self, path: str) -> None:
        self.filepath = path
        self.path = FileUtils.get_file_path(path)
        self.name = FileUtils.get_file_name(path)
        self.ext = FileUtils.get_file_ext(path)
        self._open()

    def _open(self):
        try:
            self._img: Image = Image.open(self.filepath)
        except Exception as e:
            print("Error during opening image {}".format(str(e)))

    def save_remove_exif(self):
        try:
            new = Image.new(self._img.mode, self._img.size)
            new.putdata(list(self._img.getdata()))
            new.save(self.filepath)  # without exif metadata
            print("Done: {}".format(self.filepath))
        except Exception as e:
            print("ERROR during saving image. {}".format(str(e)))

    def save(self):
        try:
            self._img.save(self.filepath)
            print("Done: {}".format(self.filepath))
        except Exception as e:
            print("ERROR during saving image. {}".format(str(e)))

    def get_height(self) -> int:
        w, h = self._img.size
        return h

    def get_width(self) -> int:
        w, h = self._img.size
        return w

    def resize_width_keep_aspect_ratio(self, width):
        width_percent = (width / float(self.get_width()))
        height_size = int((float(self.get_height()) * float(width_percent)))
        new_size = (width, height_size)
        self._img = self._img.resize(new_size, Image.ANTIALIAS)  # replace original image

    def resize_height_keep_aspect_ratio(self, height):
        height_percent = (height / float(self.get_height()))
        width_size = int((float(self.get_width()) * float(height_percent)))
        new_size = (width_size, height)
        self._img = self._img.resize(new_size, Image.ANTIALIAS)  # replace original image
