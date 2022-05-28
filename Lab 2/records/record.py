from dataclasses import dataclass, field


@dataclass
class Teacher:
    faculty: str = "[unknown]"
    department: str = "[unknown]"
    name: str = "[unknown]"
    surname: str = "[unknown]"
    midname: str = "[unknown]"
    academic_title: str = "[unknown]"
    scholastic_degree: str = "[unknown]"
    experience_years: int = 0


@dataclass
class TeacherFieldOptions:
    # Known issue: field options are only added, and can't be easily removed

    faculties: set[str] = field(default_factory=lambda: set())
    departments: dict[str, set[str]] = field(default_factory=lambda: dict())
    academic_titles: set[str] = field(default_factory=lambda: set())
    scholastic_degrees: set[str] = field(default_factory=lambda: set())

    def add_options_from(self, *args: Teacher):
        for teacher in args:

            # Faculty
            if teacher.faculty not in self.faculties:
                # In faculties
                self.faculties.add(teacher.faculty)
                # In departments as keys
                self.departments[teacher.faculty] = set()

            # Department
            if teacher.department not in self.departments[teacher.faculty]:
                self.departments[teacher.faculty].add(teacher.department)

            # Title
            if teacher.academic_title not in self.academic_titles:
                self.academic_titles.add(teacher.academic_title)

            # Degree
            if teacher.scholastic_degree not in self.scholastic_degrees:
                self.scholastic_degrees.add(teacher.scholastic_degree)
