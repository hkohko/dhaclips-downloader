import PySimpleGUI as sG


class GUI:
    def __init__(self, i):
        self._i = i

    def valid_url(self):
        _element = [sG.Text("URL status:"), sG.Text("", key=("-VALIDURL-", self._i))]
        return _element

    def url_input(self):
        _element = [
            sG.InputText(
                "",
                size=(42, 10),
                key=("-URL-", self._i),
            ),
            sG.Combo(
                values=("1080p", "720p", "480p", "360p"),
                default_value=["1080p"],
                readonly=True,
                background_color="White",
                key=("-RES-", self._i),
            ),
        ]
        return _element

    def time_from_to(self):
        _element = [
            sG.T("From:"),
            sG.InputText("", size=(8, 10), key=("-FROM-", self._i)),
            sG.T("To:"),
            sG.InputText("", size=(8, 10), key=("-TO-", self._i)),
            sG.Button(button_text="download", key=("-DLBUTTON-", self._i)),
        ]
        return _element

    def layout(self):
        dl_frame = [
            sG.Frame(
                title="",
                layout=[self.valid_url(), self.url_input(), self.time_from_to()],
                key="-FRAME-",
            )
        ]
        layout = [dl_frame, [sG.Button("+", size=(2, 1), key="-ADDROW-")]]
        return layout
