from yt_dlp import YoutubeDL
from _constants import Dir
from collections.abc import Generator
from random import randint
from pathlib import Path
from dotenv import dotenv_values

def create_dir():
    paths = (Dir.DL_DIR, Dir.FFMPEG_DIR)
    for path in paths:
        if not Path(path).exists():
            Path(path).mkdir()


def custom_format(ctx, res: int = 720) -> Generator[dict[str, str], None, None]:
    # sort from best to worst
    formats = ctx.get("formats")[::-1]

    # acodec='none' means there is no audio
    best_video_only = next(
        f
        for f in formats
        if all(
            (
                f.get("vcodec") != "none",
                f.get("acodec") == "none",
                f.get("height") <= res,
            )
        )
    )
    # find compatible audio extension
    allowed_audio_ext = {"mp4": "m4a", "webm": "webm"}
    audio_ext = allowed_audio_ext.get(best_video_only["ext"])
    # vcodec='none' means there is no video
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
    # These are the minimum required fields for a merged format
    final_format = {
        "format_id": f'{best_video_only["format_id"]}+{best_audio_only["format_id"]}',
        "ext": best_video_only["ext"],
        "requested_formats": [best_video_only, best_audio_only],
        # Must be + separated list of protocols
        "protocol": f'{best_video_only["protocol"]}+{best_audio_only["protocol"]}',
    }
    yield final_format


def main():
    create_dir()
    url = dotenv_values(Dir.PROJ_DIR.joinpath(".env")).get("SAMPLE_URL")
    dl_opts = {
        "format": custom_format,
        "paths": {"home": str(Dir.DL_DIR), "temp": str(Dir.TEMP_DL_DIR)},
        "outtmpl": {"default": f"{randint(0, 1000)}-%(title)s [%(id)s]"},
        "ffmpeg_location": Dir.FFMPEG_DIR,
    }
    with YoutubeDL(dl_opts) as ydl:
        ydl.download(url)


if __name__ == "__main__":
    main()
