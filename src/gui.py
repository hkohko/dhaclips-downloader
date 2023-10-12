import PySimpleGUI as sG

from core.main import Download


def dl_videos(event: tuple[str, int], values):
    _, group = event
    url: str = values.get(("-URL-", group))
    res: str = values.get(("-RES-", group))

    start = values.get(("-FROM-", group))
    end = values.get(("-TO-", group))

    if start == "":
        start = None
    if end == "":
        end = None

    dl = Download(int(res.replace("p", "")))
    dl.main(url, int(start), int(end))


def main_frame(i):
    url_input = [
        sG.InputText(
            "https://www.youtube.com/watch?v=zr5coQfT9IM",
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

    return url_input, time_from_to


def sanitize_input(event: tuple[str, int], values: dict[tuple[str, int], str]):
    pass


def main():
    sG.theme("SystemDefaultForReal")
    url_input, time_from_to = main_frame(0)
    dl_frame = [sG.Frame(title="", layout=[url_input, time_from_to], key="-FRAME-")]
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
            #     check = sanitize_input(event, values)
            if event[0] == "-DLBUTTON-":
                dl_videos(event, values)
    window.close()


if __name__ == "__main__":
    main()
