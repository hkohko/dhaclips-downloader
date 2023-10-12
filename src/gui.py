from threading import Thread

import PySimpleGUI as sG
from yt_dlp.utils._utils import YoutubeDLError

from core._time_handler import get_seconds
from core.main import Download


def download_handler(
    url: str, res: str, time_from: int, time_end: int, event: tuple[str, int], window
):
    _, group = event
    window[event].update(disabled=True)
    try:
        window[("-VALIDURL-", group)].update("")
        dl = Download(int(res.replace("p", "")))
        dl.main(url, time_from, time_end)
    except YoutubeDLError:
        window[("-VALIDURL-", group)].update("!!Invalid URL!!")
    finally:
        window[event].update(disabled=False)
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


def main_frame(i):
    valid_url = [sG.Text("URL status:"), sG.Text("", key=("-VALIDURL-", i))]
    url_input = [
        sG.InputText(
            "",
            size=(42, 10),
            key=("-URL-", i),
        ),
        sG.Combo(
            values=("1080p", "720p", "480p", "360p"),
            default_value=["1080p"],
            readonly=True,
            background_color="White",
            key=("-RES-", i),
        ),
    ]
    time_from_to = [
        sG.T("From:"),
        sG.InputText("", size=(8, 10), key=("-FROM-", i)),
        sG.T("To:"),
        sG.InputText("", size=(8, 10), key=("-TO-", i)),
        sG.Button(button_text="download", key=("-DLBUTTON-", i)),
    ]

    return valid_url, url_input, time_from_to


def main():
    sG.theme("SystemDefaultForReal")
    valid_url, url_input, time_from_to = main_frame(0)
    dl_frame = [
        sG.Frame(title="", layout=[valid_url, url_input, time_from_to], key="-FRAME-")
    ]
    layout = [dl_frame, [sG.Button("+", size=(2, 1), key="-ADDROW-")]]

    window = sG.Window("dhaclips", layout)
    i = 1
    while True:
        event, values = window.read()

        if event == sG.WIN_CLOSED:
            break
        if event == "-ADDROW-":
            window.extend_layout(window["-FRAME-"], rows=main_frame(i))
            i += 1
        if isinstance(event, tuple):
            if event[0] == "-DLBUTTON-":
                dl_videos(event, values, window)
    window.close()


if __name__ == "__main__":
    main()
