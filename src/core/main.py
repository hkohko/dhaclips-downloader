import json
from collections.abc import Generator
from pathlib import Path

from _constants import Dir
from _yt_ops import get_ops
from dotenv import dotenv_values
from yt_dlp import YoutubeDL
from yt_dlp.utils import download_range_func


class Download:
    def __init__(self, res: int, ext: str = "mp4"):
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
                    f.get("ext") == self.ext,
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

    def custom_format(
        self, ctx, res: int = 1080
    ) -> Generator[dict[str, str], None, None]:
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
        with open("hook.txt", "a") as file:
            json.dump(data, file)

    def main(self, url, start: int | None = None, end: int | None = None):
        ranges = (start, end)
        self.create_dir()
        dl_opts = get_ops(self.custom_format, download_range_func, self.my_hook, ranges)
        with YoutubeDL(dl_opts) as ydl:
            ydl.download(url)


if __name__ == "__main__":
    url = dotenv_values(Dir.PROJ_DIR.joinpath(".env")).get("SAMPLE_URL")
    dl = Download(1080, "mp4")
    dl.main(url, 0, 100)
