from records.record import Teacher as Record
from records.record_keeper import RecordKeeper
from random import choice, randint


class RandomRecordFiller:

    #region //// Components and settings

    faculties_and_departments: dict[str, list[str]] = {
        "Faculty of History": [
            "Department of Ancient World History",
            "Department of Recent History",
            "Department of Archeology",
            "Department of Ethnology"
        ],

        "Faculty of Linguistics": [
            "Department of Entymology",
            "Department of Computer Linguistics",
            "Department of Foreign Languages"
        ],

        "Faculty of Economics": [
            "Department of Logistics",
            "Department of Bank Economics",
            "Department of Management",
            "Department of Analytic Economics",
            "Department of Corporate Finances"
        ],

        "Faculty of Mathematics": [
            "Department of High Mathematics",
            "Department of Geometry",
            "Department of Mathematical Analysis",
            "Department of Modeling"
        ],

        "Faculty of Law": [
            "Department of History of Law",
            "Department of International Law",
            "Department of Crime Law"
        ],

        "Faculty of Computer Science": [
            "Department of Computer Security",
            "Department of Artificial Intelligence",
            "Department of Game Design"
        ],

        "Faculty of Geography": [
            "Department of Physical Geography",
            "Department of Ecology"
        ]
    }

    names_male: list[str] = [
        "George",
        "Oliver",
        "Alexandar",
        "Michal",
        "David",
        "Nicolas",
        "Ali",
        "Vasilii",
        "Victor",
        "Albert",
        "Philip",
        "Dmitriy",
        "Denis",
        "Vlad",
        "Joel",
        "Pavel",
        "Peter",
        "Max",
        "Stephan",
        "Stanislav",
        "Yan",
        "Dan"
    ]

    names_female: list[str] = [
        "Lili",
        "Ruby",
        "Alexandra",
        "Maria",
        "Anna",
        "Mira",
        "Christine",
        "Victoria",
        "Elisabeth",
        "Regina",
        "Camila",
        "Rose",
        "Stephanie",
        "Yana",
        "Dana"
    ]

    surnames: list[tuple[str, str]] = [
        # Male, Female
        ("Karpenko", "Karpenko"),
        ("Karsakov", "Karsakova"),
        ("Kerget", "Kerget"),
        ("Minin", "Minina"),
        ("Ivanov", "Invanova"),
        ("Vorsa", "Vorsa"),
        ("Madich", "Madich"),
        ("Brenko", "Brenko"),
        ("Radich", "Radich"),
        ("Lisin", "Lisina"),
        ("Zaitsev", "Zaitseva"),
        ("Korolyov", "Korolyova"),
        ("Kazlov", "Kazlova"),
        ("Shuba", "Shuba"),
        ("Laskevich", "Laskevich"),
        ("Tur", "Tur"),
        ("Platonov", "Platonova"),
        ("Yurkov", "Yurkova"),
        ("Golenkov", "Golenkova"),
        ("Basav", "Basava"),
        ("Korsak", "Korsak")
    ]

    midnames: list[tuple[str, str]] = [
        # Male, Female
        ("Invanovich", "Ivanovna"),
        ("Vasilievich", "Vasilienvna"),
        ("Nikolaevich", "Nikolaevna"),
        ("Cheslavovich", "Cheslavovna"),
        ("Stepanovich", "Stepanovna"),
        ("Pavlovich", "Pavlovna"),
        ("Alexandrovich", "Alexandrovna"),
        ("Vladimirovich", "Vladimirovna"),
        ("Markovich", "Markovna"),
        ("Frolovich", "Frolovna"),
        ("Yanovich", "Yanovna"),
        ("Semyonovich", "Semyonovna"),
        ("Petrovich", "Petrovna"),
        ("Sergeevich", "Sergeevna"),
        ("Lvovich", "Lvovna"),
        ("Egorovich", "Egorovna")
    ]

    academic_titles: list[str] = [
        "Professor",
        "Associate Professor",
        "Lecturer",
        "Researcher",
        #"Dean",
        #"Vice-Dean",
        #"Head of Department"
    ]

    scholastic_degrees: list[str] = [
        "Bachelor",
        "Master",
        "Professor"
    ]

    years_range: tuple[int, int] = (4, 25)

    #endregion

    @classmethod
    def fill_keeper(cls, keeper: RecordKeeper, count: int):
        for _ in range(count):
            record = Record()

            # Faculty and department
            record.faculty = choice(list(cls.faculties_and_departments.keys()))
            record.department = choice(cls.faculties_and_departments[record.faculty])

            # Name
            is_male = choice([True, False])
            record.name = choice(cls.names_male if is_male else cls.names_female)
            record.surname = choice(cls.surnames)[0 if is_male else 1]
            record.midname = choice(cls.midnames)[0 if is_male else 1]

            # Title and degree
            record.academic_title = choice(cls.academic_titles)
            record.scholastic_degree = choice(cls.scholastic_degrees)

            # Years
            record.experience_years = randint(*cls.years_range)

            keeper.add(record)
