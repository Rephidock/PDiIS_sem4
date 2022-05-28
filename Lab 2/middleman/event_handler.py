from __future__ import annotations
from typing import TYPE_CHECKING, cast, Callable, Final

from records.record_keeper import RecordKeeper
from records.record import Teacher as Record, TeacherFieldOptions as RecordFieldOptions
from middleman.string_formatter import StringFormatter
from utils import exceptions
from math import ceil

if TYPE_CHECKING:
    from ui.app import RecordEditorApp
    from kivy.uix.screenmanager import Screen
    from kivy.uix.textinput import TextInput
    from kivy.uix.togglebutton import ToggleButton
    from kivymd.uix.selectioncontrol import MDSwitch
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivy.uix.label import Label
    from ui.components.centered_text_input import CenteredTextInput
    from ui.components.records_table import RecordsTable
    from ui.components.data_field_input import DataFieldInput


class EventHandler:

    #region //// Init

    record_keeper: RecordKeeper
    app: RecordEditorApp | None

    __current_page: int
    __search_result: list[int]

    def __init__(self, record_keeper: RecordKeeper):
        self.record_keeper = record_keeper
        self.app = None

        self.__current_page = 0
        self.__search_result = list()

    def set_app(self, app: RecordEditorApp):
        """Sets target app instance."""
        self.app = app

    def on_create(self):
        self.__on_create_toolbar()
        self.__on_create_view()
        self.__on_create_edit()
        self.__on_create_search()

    #endregion

    #region //// Utils

    def validate_text_input_for_int(self, widget: TextInput) -> bool:
        try:
            _ = int(widget.text)
        except ValueError:
            self.app.show_dialog(**StringFormatter.format_popup_error_integer(widget.text))
            return False
        else:
            return True

    def validate_text_input_for_int_or_empty(self, widget: TextInput) -> bool:
        if widget.text == "": return True
        return self.validate_text_input_for_int(widget)

    #endregion

    #region //// File controls

    def on_filename_change(self, widget: TextInput) -> bool:
        """Returns true if filename is valid"""
        try:
            self.record_keeper.set_filepath(widget.text)
        except exceptions.InvalidPathError:
            self.app.show_dialog(**StringFormatter.format_popup_error_filename(widget.text))
            return False
        else:
            return True

    def on_save_press(self):
        valid = self.on_filename_change(self.app.root.ids["file_controls"].ids["text_input"])
        if valid:
            try:
                self.record_keeper.save()
            except exceptions.InvalidPathError:
                self.app.show_dialog(title="Save Failed", text="File location is invalid")

    def on_load_press(self):
        valid = self.on_filename_change(self.app.root.ids["file_controls"].ids["text_input"])
        if valid:
            try:
                self.record_keeper.load()
            except FileNotFoundError:
                self.app.show_dialog(title="Load Failed", text="File was not found.")

            # Also refresh view
            self.view_refresh_page()

    #endregion

    #region //// Tool (Screen) Selection

    dict_button_key_to_screen_name: Final[dict[str, str]] = {
        "view": "screen_view",
        "edit": "screen_edit",
        "search": "screen_search"
    }

    dict_button_key_to_screen_id: Final[dict[str, str]] = {
        "view": "tool_button_view",
        "edit": "tool_button_edit",
        "search": "tool_button_search"
    }

    def __on_create_toolbar(self):
        self.on_tool_selection("view")

    def on_tool_button_state(self, widget: ToggleButton, button_key: str):
        if widget.state == "down":
            self.on_tool_selection(button_key)

    def on_tool_selection(self, button_key: str):
        self.app.root.ids["tool_screens"].current = self.dict_button_key_to_screen_name[button_key]

        # Refresh view when entering view
        if button_key == "view":
            self.view_refresh_page()

        # Refresh search dropdowns
        if button_key == "edit":
            self.update_dropdown_all(self.edit_get_screen())

        if button_key == "search":
            self.update_dropdown_all(self.search_get_screen())

    def force_tool_selection(self, button_key: str):
        force_button_id = self.dict_button_key_to_screen_id[button_key]
        tool_panel = self.app.root.ids["tool_panel"]
        for button_id in self.dict_button_key_to_screen_id.values():
            target_state = "down" if button_id == force_button_id else "normal"
            cast('ToggleButton', tool_panel.ids[button_id]).state = target_state

    #endregion

    #region //// View Screen

    #region //// View Screen: Events

    def __on_create_view(self):
        # Find screen
        screen = cast('Screen', self.app.root.ids["tool_screens"].ids["screen_view"])

        # Set switch
        cast('MDSwitch', screen.ids["table_controls"].ids["filter_view_switch"]).active = False

        # Force update page
        self.view_goto_page(0)

    def on_view_press_first(self):
        self.view_goto_page(0)

    def on_view_press_prev(self):
        if self.__current_page > 0:
            self.view_goto_page(self.__current_page - 1)

    def on_view_press_next(self):
        if self.__current_page < self.view_get_page_count() - 1:
            self.view_goto_page(self.__current_page + 1)

    def on_view_press_last(self):
        self.view_goto_page(self.view_get_page_count()-1)

    def on_view_filter_switch(self):
        self.view_goto_page(0)

    def on_view_records_per_page_state(self, widget: ToggleButton, count: int):
        if widget.state == "down":
            self.on_view_records_per_page_selection(count)

    def on_view_records_per_page_selection(self, count: int):
        self.view_get_records_table().set_data_row_count(count)
        self.view_refresh_page()

    #endregion

    #region //// View Screen: Getters

    def view_get_controls(self) -> MDBoxLayout:
        return cast('MDBoxLayout', self.app.root.ids["tool_screens"].ids["screen_view"].ids["table_controls"])

    def view_get_records_table(self) -> RecordsTable:
        return cast('RecordsTable', self.app.root.ids["tool_screens"].ids["screen_view"].ids["records_table"])

    def view_get_page_count(self) -> int:
        active_count = len(self.__search_result)\
                        if self.view_get_filter_switch_state()\
                        else self.record_keeper.count
        if active_count == 0: return 1
        return ceil(active_count / self.view_get_records_table().data_rows)

    def view_get_filter_switch_state(self) -> bool:
        return cast('MDSwitch', self.view_get_controls().ids["filter_view_switch"]).active

    def view_force_switch_state(self, state: bool):
        cast('MDSwitch', self.view_get_controls().ids["filter_view_switch"]).active = state

    #endregion

    #region //// View Screen: Apply changes

    def view_record_to_strings(self, index: int) -> tuple[str, ...]:
        # Out of bounds
        if index < 0 or index >= self.record_keeper.count:
            return tuple("" for _ in range(7))

        # Actual record in bounds
        record: Record = self.record_keeper[index]
        return (
            str(index+1),
            record.faculty,
            record.department,
            StringFormatter.format_full_name(record.name, record.surname, record.midname),
            record.academic_title,
            record.scholastic_degree,
            str(record.experience_years)
        )

    def view_goto_page(self, page_index: int):
        self.__current_page = page_index
        self.view_refresh_page()

    def view_refresh_page(self):
        if self.view_get_filter_switch_state():
            self.view_update_display_filtered()
        else:
            self.view_update_display_regular()

    def view_update_display_regular(self):

        controls = self.view_get_controls()
        records_table = self.view_get_records_table()
        entries_per_page = records_table.data_rows

        # Search result
        search_result_display = cast('Label', controls.ids["filter_view_count"])
        search_result_display.text = StringFormatter.format_search_result_disabled()

        # Page index display
        page_display = cast('Label', controls.ids["page_selection_label"])
        page_display.text = StringFormatter.format_page_display(
                                    self.__current_page,
                                    entries_per_page,
                                    self.record_keeper.count
                                )

        # Display entries
        page_start_entry_index = self.__current_page * entries_per_page
        page_end_entry_index = page_start_entry_index + entries_per_page - 1
        for row, i in enumerate(range(page_start_entry_index, page_end_entry_index+1)):
            strings = self.view_record_to_strings(i)
            for col, string in enumerate(strings):
                records_table.set_non_header_text(row, col, string)

    def view_update_display_filtered(self):
        controls = self.view_get_controls()
        records_table = self.view_get_records_table()
        entries_per_page = records_table.data_rows

        # Search result
        search_result_display = cast('Label', controls.ids["filter_view_count"])
        search_result_display.text = StringFormatter.format_search_result_count(
                                                        len(self.__search_result),
                                                        self.record_keeper.count
                                                    )

        # Page index display
        page_display = cast('Label', controls.ids["page_selection_label"])
        page_display.text = StringFormatter.format_page_display(
            self.__current_page,
            entries_per_page,
            len(self.__search_result)
        )

        # Display entries
        page_start_entry_index = self.__current_page * entries_per_page
        page_end_entry_index = page_start_entry_index + entries_per_page - 1
        for row, search_i in enumerate(range(page_start_entry_index, page_end_entry_index + 1)):
            entry_i = self.__search_result[search_i] if search_i < len(self.__search_result) else -1
            strings = self.view_record_to_strings(entry_i)
            for col, string in enumerate(strings):
                records_table.set_non_header_text(row, col, string)

    #endregion

    #endregion

    #region //// Edit, Search dropdowns

    def update_dropdown_departments(self, screen: Screen, faculty_name: str):
        department_field = cast('DataFieldInput', screen.ids["data_field_department"])

        departments = self.record_keeper.field_options.departments.get(faculty_name, None)
        if departments is None:
            department_field.set_dropdown_spinner_items(list())
        else:
            department_field.set_dropdown_spinner_items(departments)

    def update_dropdown_all(self, screen: Screen):
        faculty_field = cast('DataFieldInput', screen.ids["data_field_faculty"])
        department_field = cast('DataFieldInput', screen.ids["data_field_department"])
        title_field = cast('DataFieldInput', screen.ids["data_field_title"])
        degree_field = cast('DataFieldInput', screen.ids["data_field_degree"])

        field_options: RecordFieldOptions = self.record_keeper.field_options

        faculty_field.set_dropdown_spinner_items(field_options.faculties)
        department_field.set_dropdown_spinner_items(list())
        title_field.set_dropdown_spinner_items(field_options.academic_titles)
        degree_field.set_dropdown_spinner_items(field_options.scholastic_degrees)

    #endregion

    #region //// Edit Screen

    #region //// Edit Screen: Events

    def __on_create_edit(self):
        # Find screen
        screen = self.edit_get_screen()

        # Add int checks
        index_input = cast('CenteredTextInput', screen.ids["record_controls"].ids["input_index"])
        years_field = cast('DataFieldInput', screen.ids["data_field_years"])
        index_input.bind(on_text_validate=self.validate_text_input_for_int)
        years_field.bind_on_text_input_validate(0, self.validate_text_input_for_int)

        # Dropdowns
        faculty_field = cast('DataFieldInput', screen.ids["data_field_faculty"])
        faculty_field.bind_on_text_input_text(0, self.on_edit_faculty_text)
        self.update_dropdown_all(self.edit_get_screen())

    def on_edit_load(self):
        if self.edit_validate_index():
            text_input = cast('CenteredTextInput', self.edit_get_screen().ids["record_controls"].ids["input_index"])
            self.edit_record_split(self.record_keeper[int(text_input.text)-1])

    def on_edit_save(self):
        if self.edit_validate_index():
            record = self.edit_record_try_join()
            if record is not None:
                text_input = cast('CenteredTextInput', self.edit_get_screen().ids["record_controls"].ids["input_index"])
                self.record_keeper[int(text_input.text)-1] = record
                self.update_dropdown_all(self.edit_get_screen())

    def on_edit_append(self):
        record = self.edit_record_try_join()
        if record is not None:
            self.record_keeper.add(record)
            self.update_dropdown_all(self.edit_get_screen())

    def on_edit_faculty_text(self, _: CenteredTextInput, text: str):
        self.update_dropdown_departments(self.edit_get_screen(), text)

    #endregion

    #region //// Edit Screen: Getters, Setters, Validators

    def edit_get_screen(self) -> Screen:
        return cast('Screen', self.app.root.ids["tool_screens"].ids["screen_edit"])

    def edit_validate_index(self) -> bool:
        text_input = cast('CenteredTextInput', self.edit_get_screen().ids["record_controls"].ids["input_index"])

        # Check if int
        result = self.validate_text_input_for_int(text_input)
        if not result: return False

        # Check if in bounds
        index = int(text_input.text)-1
        if index < 0 or index >= self.record_keeper.count:
            self.app.show_dialog(**StringFormatter.format_popup_error_index_oob(text_input.text))
            return False

        return True

    def edit_record_split(self, record: Record):
        """Splits a record into strings and puts them into DataFieldInputs"""

        screen = self.edit_get_screen()

        # Faculty, Department, Title, Degree, Years
        cast('DataFieldInput', screen.ids["data_field_faculty"]).get_text_input().text = record.faculty
        cast('DataFieldInput', screen.ids["data_field_department"]).get_text_input().text = record.department
        cast('DataFieldInput', screen.ids["data_field_title"]).get_text_input().text = record.academic_title
        cast('DataFieldInput', screen.ids["data_field_degree"]).get_text_input().text = record.scholastic_degree
        cast('DataFieldInput', screen.ids["data_field_years"]).get_text_input().text = str(record.experience_years)

        # Name
        name_field = cast('DataFieldInput', screen.ids["data_field_name"])
        name_field.get_text_input(0).text = str(record.surname)
        name_field.get_text_input(1).text = str(record.name)
        name_field.get_text_input(2).text = str(record.midname)

    def edit_record_try_join(self) -> Record | None:
        """
        Tries to compile strings from DataFieldInputs into a record.
        Shows a popup with an error if fails and returns None.
        Otherwise, returns the Record.
        """

        screen = self.edit_get_screen()

        # Validation
        years_valid_int = self.validate_text_input_for_int(screen.ids["data_field_years"].get_text_input())
        if not years_valid_int: return None

        years_int = int(cast('DataFieldInput', screen.ids["data_field_years"]).get_text_input().text)
        if years_int < 0:
            self.app.show_dialog(**StringFormatter.format_popup_error_field_is_negative("Experience Years", years_int))
            return None

        # Forming
        name_field = cast('DataFieldInput', screen.ids["data_field_name"])
        return Record(
            faculty=cast('DataFieldInput', screen.ids["data_field_faculty"]).get_text_input().text,
            department=cast('DataFieldInput', screen.ids["data_field_department"]).get_text_input().text,
            name=name_field.get_text_input(1).text,
            surname=name_field.get_text_input(0).text,
            midname=name_field.get_text_input(2).text,
            academic_title=cast('DataFieldInput', screen.ids["data_field_title"]).get_text_input().text,
            scholastic_degree=cast('DataFieldInput', screen.ids["data_field_degree"]).get_text_input().text,
            experience_years=years_int
        )

    #endregion

    #endregion

    #region //// Search Screen

    #region //// Search Screen: Events

    def __on_create_search(self):
        # Find screen
        screen = self.search_get_screen()

        # Add int checks
        index_input = cast('CenteredTextInput', screen.ids["input_index"])
        years_field = cast('DataFieldInput', screen.ids["data_field_years"])
        index_input.bind(on_text_validate=self.validate_text_input_for_int)
        years_field.bind_on_text_input_validate(0, self.validate_text_input_for_int_or_empty)
        years_field.bind_on_text_input_validate(1, self.validate_text_input_for_int_or_empty)

        # Dropdowns
        faculty_field = cast('DataFieldInput', screen.ids["data_field_faculty"])
        faculty_field.bind_on_text_input_text(0, self.on_search_faculty_text)

    def on_search_remove_at(self):
        if self.search_validate_index():
            index = int(self.search_get_index_input().text) - 1
            self.record_keeper.remove_at(index)
            self.app.show_dialog(**StringFormatter.format_popup_remove_result(index))

    def on_search_clear(self):
        removal_count = self.record_keeper.count
        self.record_keeper.clear()
        self.app.show_dialog(**StringFormatter.format_popup_clear(removal_count))

    def on_search_search(self):
        # Search and popup
        predicates = self.search_form_predicate_list()
        if predicates is None: return

        self.__search_result = list(self.record_keeper.search(*predicates))
        self.app.show_dialog(
            **StringFormatter.format_popup_search_result(len(self.__search_result))
        )

        # Force open view screen and turn on switch
        self.view_force_switch_state(True)
        self.force_tool_selection("view")

    def on_search_remove_search(self):
        predicates = self.search_form_predicate_list()
        if predicates is None: return

        remove_count = self.record_keeper.search_and_remove(*predicates)
        self.app.show_dialog(
            **StringFormatter.format_popup_search_remove_result(remove_count)
        )

    def on_search_faculty_text(self, _: CenteredTextInput, text: str):
        self.update_dropdown_departments(self.search_get_screen(), text)

    #endregion

    #region //// Search Screen: Getters, Setters, Validators

    def search_get_screen(self) -> Screen:
        return cast('Screen', self.app.root.ids["tool_screens"].ids["screen_search"])

    def search_get_index_input(self) -> CenteredTextInput:
        return cast('CenteredTextInput', self.search_get_screen().ids["input_index"])

    def search_validate_index(self) -> bool:
        text_input = self.search_get_index_input()

        # Check if int
        result = self.validate_text_input_for_int(text_input)
        if not result: return False

        # Check if in bounds
        index = int(text_input.text)-1
        if index < 0 or index >= self.record_keeper.count:
            self.app.show_dialog(**StringFormatter.format_popup_error_index_oob(text_input.text))
            return False

        return True

    def search_form_predicate_list(self) -> list[Callable[[Record], bool]] | None:
        """
        Forms are returns a list of predicates for search.
        Shows a popup and returns None for malformed input.
        """

        # Get Fields
        screen = self.search_get_screen()
        faculty_field = cast('DataFieldInput', screen.ids["data_field_faculty"])
        department_field = cast('DataFieldInput', screen.ids["data_field_department"])
        names_field = cast('DataFieldInput', screen.ids["data_field_name"])
        title_field = cast('DataFieldInput', screen.ids["data_field_title"])
        degree_field = cast('DataFieldInput', screen.ids["data_field_degree"])
        years_field = cast('DataFieldInput', screen.ids["data_field_years"])

        # Form lambdas
        predicates = list()

        # Single equalities
        if faculty_field.checkbox.state == "down":
            predicates.append(lambda x: x.faculty == faculty_field.get_text_input().text)

        if department_field.checkbox.state == "down":
            predicates.append(lambda x: x.department == department_field.get_text_input().text)

        if title_field.checkbox.state == "down":
            predicates.append(lambda x: x.academic_title == title_field.get_text_input().text)

        if degree_field.checkbox.state == "down":
            predicates.append(lambda x: x.scholastic_degree == degree_field.get_text_input().text)

        # Name
        if names_field.checkbox.state == "down":
            surname = names_field.get_text_input(0).text
            name = names_field.get_text_input(1).text
            midname = names_field.get_text_input(2).text

            # Check for empty
            if surname == name == midname == "":
                self.app.show_dialog(**StringFormatter.format_popup_error_search_no_names())
                return None

            if surname != "": predicates.append(lambda x: x.surname == surname)
            if name != "": predicates.append(lambda x: x.name == name)
            if midname != "": predicates.append(lambda x: x.midname == midname)

        # Years
        if years_field.checkbox.state == "down":

            if not self.validate_text_input_for_int_or_empty(years_field.get_text_input(0)): return None
            if not self.validate_text_input_for_int_or_empty(years_field.get_text_input(1)): return None

            bound_low_str = years_field.get_text_input(0).text
            bound_high_str = years_field.get_text_input(1).text

            bound_low_present = bound_low_str != ""
            bound_high_present = bound_high_str != ""

            if not bound_high_present and not bound_low_present:
                self.app.show_dialog(**StringFormatter.format_popup_error_search_no_years())
                return None

            if bound_low_present:
                predicates.append(lambda x: x.experience_years >= int(bound_low_str))

            if bound_high_present:
                predicates.append(lambda x: x.experience_years <= int(bound_high_str))

        # Check for empty
        if len(predicates) == 0:
            self.app.show_dialog(**StringFormatter.format_popup_error_search_no_filters())
            return None

        return predicates

    #endregion

    #endregion
