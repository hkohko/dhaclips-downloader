from threading import Thread

import PySimpleGUI as sG
from yt_dlp.utils._utils import YoutubeDLError

from src.core._time_handler import get_seconds
from src.core.main import Download


def download_handler(
    url: str, res: str, time_from: int, time_end: int, dlbutton: tuple[str, int], window
):
    _, group = dlbutton
    window[dlbutton].update(disabled=True)
    try:
        window[("-VALIDURL-", group)].update("")
        dl = Download(int(res.replace("p", "")))
        dl.main(url, time_from, time_end)
    except YoutubeDLError:
        window[("-VALIDURL-", group)].update("!!Invalid URL!!")
    finally:
        window[dlbutton].update(disabled=False)
        return None


def sanitize_input(url, start, end):
    placeholder = (None, None)

    if url == "":
        sG.popup("Please input a URL.", title="Warning")
        return False, placeholder

    try:
        time_from = get_seconds(start)
        time_end = get_seconds(end)
    except (TypeError, ValueError):
        sG.popup(
            "Invalid time format. Must be hh:mm:ss, mm:ss, or ss\nhh<24\nmm<60\nss<60",
            title="Error",
        )
        return False, placeholder

    if all((time_from is not None, time_end is not None)):
        if time_from > time_end:
            sG.popup("'From' must be earlier in time than 'To'.")
            return False, placeholder

    return True, (time_from, time_end)


def dl_videos(event: tuple[str, int], values, window):
    dlbutton, group = event
    url: str = values.get(("-URL-", group))
    res: str = values.get(("-RES-", group))
    start = values.get(("-FROM-", group))
    end = values.get(("-TO-", group))
    sanitized, ranges = sanitize_input(url, start, end)

    if sanitized:
        time_from = ranges[0]
        time_to = ranges[1]
        task = Thread(
            group=None,
            target=download_handler,
            args=(url, res, time_from, time_to, event, window),
        )
        task.start()
