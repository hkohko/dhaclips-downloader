import json
from collections.abc import Generator
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import download_range_func

from ._constants import Dir
from ._yt_ops import get_ops


class Download:
    def __init__(self, res: int, ext: str = None):
        self.res = res
        self.ext = ext

    def create_dir(self):
        paths = (Dir.DL_DIR, Dir.FFMPEG_DIR, Dir.TEMP_DL_DIR)
        for path in paths:
            if not Path(path).exists():
                Path(path).mkdir()

    def get_video(self, formats: list[dict[str | int]]):
        best_video_only = next(
            f
            for f in formats
            if all(
                (
                    f.get("vcodec") != "none",
                    f.get("acodec") == "none",
                    f.get("height") <= self.res,
                    f.get("ext") == self.ext if self.ext is not None else f.get("ext"),
                )
            )
        )
        return best_video_only

    def get_audio(self, formats: list[dict[str | int]], audio_ext: str):
        best_audio_only = next(
            f
            for f in formats
            if all(
                (
                    f.get("acodec") != "none",
                    f.get("vcodec") == "none",
                    f.get("ext") == audio_ext,
                )
            )
        )
        return best_audio_only

    def custom_format(self, ctx) -> Generator[dict[str, str], None, None]:
        # sort from best to worst
        formats = ctx.get("formats")[::-1]

        # acodec='none' means there is no audio]
        best_video_only = self.get_video(formats)
        # find compatible audio extension
        allowed_audio_ext = {"mp4": "m4a", "webm": "webm"}
        audio_ext = allowed_audio_ext.get(best_video_only["ext"])
        # vcodec='none' means there is no video
        best_audio_only = self.get_audio(formats, audio_ext)
        # These are the minimum required fields for a merged format
        final_format = {
            "format_id": f'{best_video_only["format_id"]}+'
            f'{best_audio_only["format_id"]}',
            "ext": best_video_only["ext"],
            "requested_formats": [best_video_only, best_audio_only],
            # Must be + separated list of protocols
            "protocol": f'{best_video_only["protocol"]}+{best_audio_only["protocol"]}',
        }
        yield final_format

    def my_hook(self, data):
        with open("hook.txt", "w") as file:
            json.dump(data, file)

    def start_download(self, dl_opts, url, info_only=False):
        if info_only:
            with YoutubeDL(dl_opts) as ydl:
                data = ydl.extract_info(url, download=False)
                return data
        with YoutubeDL(dl_opts) as ydl:
            ydl.download(url)

    def main(
        self,
        url,
        start: int | None = None,
        end: int | None = None,
        info_only: bool = False,
    ):
        self.create_dir()
        if start is None:
            start = 0
        if end is None:
            dl_opts = get_ops(
                self.custom_format, download_range_func, self.my_hook, (None, None)
            )
            dur = self.start_download(dl_opts, url, info_only=True)
            formats = dur.get("formats")
            end = formats[0].get("fragments")[0].get("duration")
        ranges = (start, end)
        dl_opts = get_ops(self.custom_format, download_range_func, self.my_hook, ranges)
        _ = self.start_download(dl_opts, url, info_only=info_only)
        if info_only:
            return _
        return None
