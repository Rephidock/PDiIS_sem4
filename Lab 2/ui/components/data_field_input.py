from typing import Iterable, Callable, Any

from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.label import Label
from ui.components.centered_text_input import CenteredTextInput
from kivy.uix.spinner import Spinner


class DataFieldInput(BoxLayout):

    #region //// Setup kivy properties

    show_checkbox = BooleanProperty(defaultvalue=False)
    label_text = StringProperty(defaultvalue="")
    label_width = NumericProperty(defaultvalue=None, allownone=True)
    input_count = NumericProperty(defaultvalue=1)
    input_hint = StringProperty(defaultvalue=None, allownone=True)
    input_hints = ListProperty(defaultvalue=None, allownone=True)
    show_dropdown = BooleanProperty(defaultvalue=False)

    #endregions

    #region //// Init, Create widgets

    __checkbox: MDCheckbox | None
    __label: Label
    __text_inputs: list[CenteredTextInput]
    __dropdown_spinner: Spinner | None

    _dropdown_spinner_select_text: str = "v Select v"

    def __init__(self, **kwargs):
        """
        Creates a DataFieldInput widget.
        Widget has BoxLayout settings in addition to:
        - show_checkbox: bool
            Toggles adding checkbox on the left. False by default.
        - label_text: str
            Name of the label next to the input.
        - label_width: float|None
            Fixed with of the label or dynamic if None
        - input_count: int
            Number of input fields. 1 by default.
        - input_hint: str|None
            1st field's input hint. None by default, equivalent to empty.
        - input_hints: Iterable[str]|None
            All field's input hints. Overrides input_hint if provided.
            None by default, equivalent to all empty and no override.
        - show_dropdown: bool
            Toggles adding dropdown menu at the end. False by default.
            Dropdown menu will only fill the last input field.
        """
        super().__init__(
                    orientation="horizontal",
                    **kwargs
                )
        Clock.schedule_once(self.fill_widgets)  # Run on the next frame

    def fill_widgets(self, _=None):
        self.clear_widgets()

        # Checkbox
        self.__checkbox = None
        if self.show_checkbox:
            self.__checkbox = MDCheckbox(
                                size_hint=(None, None),
                                size=(dp(48), dp(48)),
                                pos_hint={"center_y": .5}
                            )
            self.add_widget(self.__checkbox)

        # Label
        self.__label = Label(text=self.label_text)
        self.add_widget(self.__label)

        # Label width
        if self.label_width is not None:
            self.__label.size_hint = (None, 1)
            self.__label.width = self.label_width

        # Inputs
        self.__text_inputs = [CenteredTextInput(multiline=False) for _ in range(self.input_count)]
        for text_input in self.__text_inputs:
            self.add_widget(text_input)

        # Input hints
        if self.input_hints is None:
            if self.input_hint is not None and self.input_count >= 1:
                self.__text_inputs[0].hint_text = self.input_hint
        else:
            for text_input, hint in zip(self.__text_inputs, self.input_hints):
                text_input.hint_text = hint

        # Dropdown menu
        self.__dropdown_spinner = None
        if self.show_dropdown:
            self.__dropdown_spinner = Spinner(text=self._dropdown_spinner_select_text)
            self.__dropdown_spinner.bind(text=self._on_spinner_selection)
            self.add_widget(self.__dropdown_spinner)

    #endregion

    #region //// Dropdown menu

    def _on_spinner_selection(self, spinner, text):
        """Called by the spinner dropdown when selection text changes"""

        # Avoid firing when setting to default text
        if text == self._dropdown_spinner_select_text: return
        # Set spinner text
        spinner.text = self._dropdown_spinner_select_text
        # Set input field (only affects the last text field)
        if len(self.__text_inputs) > 0:
            self.__text_inputs[-1].text = text

    def set_dropdown_spinner_items(self, items: Iterable[str]):
        if self.__dropdown_spinner is None: return
        self.__dropdown_spinner.values = tuple(items)

    #endregion

    #region //// Getters

    @property
    def checkbox(self) -> MDCheckbox | None:
        return self.__checkbox

    @property
    def label(self) -> Label:
        return self.__label

    def get_text_input(self, index: int = 0) -> CenteredTextInput:
        return self.__text_inputs[index]

    #endregion

    #region //// Bind events

    def bind_on_text_input_text(self, index: int, callback: Callable[[CenteredTextInput, str], Any]):
        self.get_text_input(index).bind(text=callback)

    def bind_on_text_input_validate(self, index: int, callback: Callable[[CenteredTextInput], Any]):
        self.get_text_input(index).bind(on_text_validate=callback)

    #endregion
