from kivy.uix.textinput import TextInput


class CenteredTextInput(TextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            size=lambda *x:
                self.setter('padding_y')(self, [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0])
            )
