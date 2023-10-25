import PySimpleGUI as sG

from gui_elements.elements import GUI
from gui_elements.logic import Logic


def main_frame(i):
    gui = GUI(i)
    return gui.valid_url(), gui.url_input(), gui.time_from_to()


def main():
    sG.theme("SystemDefaultForReal")
    gui = GUI(0)
    logic = Logic()
    window = sG.Window("dhaclips", gui.layout())
    i = 1
    while True:
        event, values = window.read()
        if event == sG.WIN_CLOSED:
            print(logic._tasks)
            if len(logic._tasks) != 0:
                for task in logic._tasks:
                    try:
                        task.result(timeout=0.1)
                    except TimeoutError:
                        pass
            break
        if event == "-ADDROW-":
            window.extend_layout(window["-FRAME-"], rows=main_frame(i))
            i += 1
        if isinstance(event, tuple):
            if event[0] == "-DLBUTTON-":
                logic.dl_videos(event, values, window)
    window.close()


if __name__ == "__main__":
    main()
