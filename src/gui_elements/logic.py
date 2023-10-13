from concurrent.futures import ThreadPoolExecutor

import PySimpleGUI as sG
from yt_dlp.utils._utils import YoutubeDLError

from src.core._time_handler import get_seconds
from src.core.main import Download


class Logic:
    def __init__(self):
        self._tasks = []

    def _download_handler(
        self,
        url: str,
        res: str,
        time_from: int,
        time_end: int,
        dlbutton: tuple[str, int],
        window,
    ):
        _, group = dlbutton
        text_validurl = ("-VALIDURL-", group)
        window[dlbutton].update(disabled=True)
        try:
            window[text_validurl].update("")
            dl = Download(int(res.replace("p", "")))
            window[text_validurl].update("Downloading...")
            dl.main(url, time_from, time_end)
            window[text_validurl].update("Done!")
        except YoutubeDLError:
            window[text_validurl].update("!!Invalid URL!!")
        finally:
            window[dlbutton].update(disabled=False)
            return None

    def _sanitize_input(self, url, start, end):
        placeholder = (None, None)

        if url == "":
            sG.popup("Please input a URL.", title="Warning")
            return False, placeholder

        try:
            time_from = get_seconds(start)
            time_end = get_seconds(end)
        except (TypeError, ValueError):
            sG.popup(
                "Invalid time format. Must be hh:mm:ss, mm:ss, or ss\n"
                "hh<24\nmm<60\nss<60",
                title="Error",
            )
            return False, placeholder

        if all((time_from is not None, time_end is not None)):
            if time_from > time_end:
                sG.popup("'From' must be earlier in time than 'To'.")
                return False, placeholder

        return True, (time_from, time_end)

    def dl_videos(self, event: tuple[str, int], values, window):
        dlbutton, group = event
        url: str = values.get(("-URL-", group))
        res: str = values.get(("-RES-", group))
        start = values.get(("-FROM-", group))
        end = values.get(("-TO-", group))
        sanitized, ranges = self._sanitize_input(url, start, end)

        if sanitized:
            self._spawn_threads(ranges, url, res, event, window)

    def _spawn_threads(self, ranges, url, res, event, window):
        time_from = ranges[0]
        time_to = ranges[1]
        executor = ThreadPoolExecutor()
        task = executor.submit(
            self._download_handler, url, res, time_from, time_to, event, window
        )
        self._tasks.append(task)
