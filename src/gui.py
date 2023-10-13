import PySimpleGUI as sG

from gui_elements.elements import GUI
from gui_elements.logic import dl_videos


def main_frame(i):
    gui = GUI(i)
    return gui.valid_url(), gui.url_input(), gui.time_from_to()


def main():
    sG.theme("SystemDefaultForReal")
    gui = GUI(0)
    window = sG.Window("dhaclips", gui.layout())
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
