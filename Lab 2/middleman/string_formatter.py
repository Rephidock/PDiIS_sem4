

class StringFormatter:

    #region //// Misc.

    @staticmethod
    def format_page_display(page_index: int, entries_per_page: int, entries_total: int) -> str:
        if entries_total == 0: return "- - -"
        page_start_entry_index = page_index*entries_per_page
        page_end_entry_index = min(page_start_entry_index+entries_per_page-1, entries_total-1)
        return f"{page_start_entry_index+1}-{page_end_entry_index+1} of {entries_total}"

    @staticmethod
    def format_full_name(first_name: str, last_name: str, middle_name: str) -> str:
        return f"{last_name} {first_name} {middle_name}"

    @staticmethod
    def format_search_result_disabled() -> str:
        return "Search view disabled.\nShowing all entries."

    @staticmethod
    def format_search_result_count(found_count: int, total_count: int) -> str:
        if found_count == 0: return f"No entries found\nof {total_count} total"
        return f"Found {found_count} entries\nof {total_count} total"

    #endregion

    #region //// Popup error texts

    @staticmethod
    def format_popup_error_filename(filename: str) -> dict[str, str]:
        return {
            "title": "Invalid File Location",
            "text": f"File path \"[i]{filename}[/i]\" is invalid"
        }

    @staticmethod
    def format_popup_error_integer(intstr: str) -> dict[str,str]:
        return {
            "title": "Invalid input",
            "text": f"\"[i]{intstr}[/i]\" is not a valid integer"
        }

    @staticmethod
    def format_popup_error_field_is_negative(field: str, intstr: int | str) -> dict[str, str]:
        return {
            "title": "Negative number",
            "text": f"{field} cannot be negative. Got [i]{intstr}[/i]."
        }

    @staticmethod
    def format_popup_error_index_oob(intstr: int | str) -> dict[str, str]:
        return {
            "title": "Index out of bounds",
            "text": f"Index [i]{intstr}[/i] is out of bounds of the table"
        }

    @staticmethod
    def format_popup_error_search_no_filters() -> dict[str, str]:
        return {
            "title": "No predicates",
            "text": f"No filters are active for the search."
        }

    @staticmethod
    def format_popup_error_search_no_names() -> dict[str, str]:
        return {
            "title": "Invalid predicate",
            "text": f"No search names are given"
        }

    @staticmethod
    def format_popup_error_search_no_years() -> dict[str, str]:
        return {
            "title": "Invalid predicate",
            "text": f"No year bounds given"
        }

    #endregion

    #region //// Popup misc texts

    @staticmethod
    def format_popup_search_result(found_count: int | str) -> dict[str, str]:
        if found_count == 0:
            return {
                "title": "Search Inconclusive",
                "text": f"No entries found"
            }

        return {
            "title": "Search Conclusive",
            "text": f"Found {found_count} entries"
        }

    @staticmethod
    def format_popup_remove_result(index: int | str) -> dict[str, str]:
        return {
            "title": "Removal Successful",
            "text": f"Entry No. {index+1} was removed"
        }

    @staticmethod
    def format_popup_search_remove_result(found_count: int | str) -> dict[str, str]:
        if found_count == 0:
            return {
                "title": "Search Inconclusive",
                "text": f"No entries were removed"
            }

        return {
            "title": "Search Conclusive",
            "text": f"Removed {found_count} entries"
        }

    @staticmethod
    def format_popup_clear(removal_count: int | str) -> dict[str, str]:
        return {
            "title": "All cleared",
            "text": f"All {removal_count} entries were removed"
        }

    #endregion
