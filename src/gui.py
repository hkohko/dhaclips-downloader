import PySimpleGUI as sG


def main_frame():
    url_input = [
        sG.InputText(
            "https://www.youtube.com/watch?v=zr5coQfT9IM", size=(42, 10), key="-URL-"
        ),
        sG.Button("+", size=(2, 1), key="-ADDROW-"),
    ]
    time_from_to = [
        sG.InputText("", size=(8, 10), key="-FROM-"),
        sG.InputText("", size=(8, 10), key="-TO-"),
        sG.Button(button_text="download", key="-DLBUTTON-"),
    ]

    return url_input, time_from_to


def main():
    sG.theme("SystemDefaultForReal")
    url_input, time_from_to = main_frame()
    frame = [sG.Frame(title="", layout=[url_input, time_from_to], key="-FRAME-")]
    layout = [frame]

    window = sG.Window("dhaclips", layout)

    while True:
        event, value = window.read()

        if event == sG.WIN_CLOSED:
            break
        if event == "-ADDROW-":
            window.extend_layout(window["-FRAME-"], rows=main_frame())
        print(event, value)
    window.close()


if __name__ == "__main__":
    main()
