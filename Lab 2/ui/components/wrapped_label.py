from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label


class WrappedLabel(Label):
    # From https://stackoverflow.com/questions/43666381/wrapping-the-text-of-a-kivy-label

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x: self.setter('text_size')(self, (self.width, None))
            #texture_size=lambda *x: self.setter('height')(self, self.texture_size[1])
        )

    #
    #def on_size(self, *args):
    #    self.canvas.before.clear()
    #    with self.canvas.before:
    #        Color(0, 1, 0, 0.25)
    #        Rectangle(pos=self.pos, size=self.size)
