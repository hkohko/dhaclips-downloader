from dotenv import dotenv_values

from src.core._constants import Dir
from src.core.main import Download


def test1():
    url = dotenv_values(Dir.PROJ_DIR.joinpath(".env")).get("SAMPLE_URL")
    dl = Download(1080)
    info_dict = dl.main(url, info_only=True)
    title = info_dict.get("title")
    print(title)
