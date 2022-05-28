from typing import cast

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from ui.components.wrapped_label import WrappedLabel


class RecordsTable(GridLayout):

    #region //// Init, Create Widgets

    _grid_cols: int = 7
    _grid_default_data_rows: int = 10

    _header_height = dp(30)
    _header_names_and_sizes: tuple[tuple[str, float]] = (
        ("No.", 1),
        ("Faculty", 2.5),
        ("Department", 2.5),
        ("Full name", 2.5),
        ("Academic title", 2),
        ("Scholastic Degree", 2),
        ("Exp. Years", 1)
    )

    __non_header_cells: list[WrappedLabel]

    def __init__(self, **kwargs):
        super().__init__(cols=self._grid_cols, **kwargs)

        self.__non_header_cells = list()
        self.__data_rows = self._grid_default_data_rows

        Clock.schedule_once(self.fill_widgets)  # Run on the next frame

    def fill_widgets(self, _=None):
        self.clear_widgets()
        self.__non_header_cells.clear()

        # Form header
        for name, size in self._header_names_and_sizes:
            label = WrappedLabel(
                    text=name,
                    bold=True,
                    size_hint=(size, None),
                    height=self._header_height
                )
            self.add_widget(label)

        # Form empty cells
        for i in range(self.__data_rows * self._grid_cols):
            size = self._header_names_and_sizes[i % self.cols][1]
            label = WrappedLabel(
                bold=False,
                text="",
                size_hint=(size, 1)
            )
            self.__non_header_cells.append(label)
            self.add_widget(label)

    #endregion

    def set_non_header_text(self, row_index: int, column_index: int, value: str):
        cast(WrappedLabel, self.__non_header_cells[row_index*self._grid_cols+column_index]).text = value

    @property
    def data_rows(self):
        return self.__data_rows

    def set_data_row_count(self, count: int):
        self.__data_rows = count
        self.fill_widgets()
