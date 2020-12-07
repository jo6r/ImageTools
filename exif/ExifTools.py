import string

from PIL.ExifTags import TAGS, GPSTAGS
from PIL.Image import Exif
from PIL.TiffImagePlugin import IFDRational


class ExifTools:

    @classmethod
    def from_exif(cls, exif: Exif):
        if not exif:  # Check if dictionary is empty
            raise NoExifError("Image has no exif data.")
        else:
            return cls(exif)

    def __init__(self, exif: Exif) -> None:
        self._exif = dict()
        self._label_tags(exif)
        self._label_gps_tags()

    def _label_tags(self, exif):
        for k, v in exif.items():
            try:
                self._exif[TAGS[k]] = self._decode(v)
            except KeyError as e:
                # print("Skip labeling, {}".format(str(e)))
                pass

    def _label_gps_tags(self):
        try:
            out = dict()
            gps = self._exif["GPSInfo"]
            for k, v in gps.items():
                try:
                    out[GPSTAGS[k]] = self._decode(v)
                except KeyError as e:
                    # print("Skip GPS labeling, {}".format(str(e)))
                    pass

            self._exif["GPSInfo"] = out
        except KeyError as e:
            # print("Image doesn't gave GPSInfo metadata. {}".format(str(e)))
            self._exif["GPSInfo"] = None

    def get_gps_info(self):
        return self._exif["GPSInfo"]

    def _decode(self, data):
        if isinstance(data, bytes):
            data = self._byte2str(data)
            data = self._remove_non_printable_chars(data)
            return data
        elif isinstance(data, IFDRational):
            return float(data.__repr__())
        elif isinstance(data, tuple):
            ilist = []
            for item in data:
                ilist.append(self._decode(item))
            return tuple(ilist)
        else:
            return data

    def _byte2str(self, data) -> str:
        out = data.decode("utf-8", "ignore")
        return out

    def _remove_non_printable_chars(self, data):
        res = filter(lambda x: x in string.printable, data)
        return "".join(list(res))

    def __str__(self) -> str:
        return self._exif.__str__()

    def __repr__(self) -> str:
        return self._exif.__repr__()


class NoExifError(Exception):
    """Raised when the image has not exif data"""
    pass
