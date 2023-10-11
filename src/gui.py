import PySimpleGUI as sG


def main_frame(i):
    url_input = [
        sG.InputText(
            "https://www.youtube.com/watch?v=zr5coQfT9IM",
            size=(42, 10),
            key=("-URL-", i),
        )
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
        # if isinstance(event, tuple):
        #     check = sanitize_input(event, values)

        print(event, values)
    window.close()


if __name__ == "__main__":
    main()
