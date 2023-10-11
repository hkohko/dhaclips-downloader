from dataclasses import dataclass
from pathlib import PurePath


@dataclass
class Dir:
    PROJ_DIR = PurePath(__file__).parents[2]
    SRC_DIR = PROJ_DIR.joinpath("src")
    TEMP_DL_DIR = PROJ_DIR.joinpath(".tempfile")
    DL_DIR = PROJ_DIR.joinpath("downloads")
    FFMPEG_DIR = SRC_DIR.joinpath("core", "ffmpeg")
