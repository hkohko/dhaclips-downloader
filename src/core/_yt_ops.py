from random import randint
from sys import platform

from ._constants import Dir


def get_ops(custom_format, download_range_func, my_hook, ranges):
    ffmpeg_dir = Dir.FFMPEG_DIR if platform == "win32" else Dir.FFMPEG_LINUX
    if all((ranges[0] is None, ranges[1] is None)):
        dl_opts = {
            "format": custom_format,
            "paths": {"home": str(Dir.DL_DIR), "temp": str(Dir.TEMP_DL_DIR)},
            "outtmpl": {"default": f"{randint(0, 1000)}-%(title)s [%(id)s]"},
            "ffmpeg_location": ffmpeg_dir,
            "progress_hooks": [my_hook],
        }
        return dl_opts

    dl_opts = {
        "format": custom_format,
        "paths": {"home": str(Dir.DL_DIR), "temp": str(Dir.TEMP_DL_DIR)},
        "outtmpl": {"default": f"{randint(0, 1000)}-%(title)s [%(id)s]"},
        "ffmpeg_location": ffmpeg_dir,
        "download_ranges": download_range_func(chapters=[], ranges=[ranges]),
        "progress_hooks": [my_hook],
    }
    return dl_opts
