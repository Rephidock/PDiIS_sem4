import unittest
from records.record import Teacher as Record
from records.record_keeper import RecordKeeper


class RecordKeeperTests(unittest.TestCase):

    def test_storage(self):
        keeper = RecordKeeper()

        # Store
        keeper.add(
            Record(name="George"),
            Record(name="Kevin"),
            Record(name="Josef")
        )
        self.assertEqual(keeper[0].name, "George")
        self.assertEqual(keeper[1].name, "Kevin")
        self.assertEqual(keeper[2].name, "Josef")
        self.assertEqual(keeper.count, 3)
        self.assertEqual(len(keeper), 3)

        # Add
        keeper.add(Record(name="Ruby"))
        self.assertEqual(keeper[3].name, "Ruby")
        self.assertEqual(keeper.count, 4)
        self.assertEqual(len(keeper), 4)

        # Mutate
        keeper[2].name = "Oliver"
        self.assertEqual(keeper[2].name, "Oliver")
        self.assertEqual(keeper.count, 4)
        self.assertEqual(len(keeper), 4)

        # Override
        keeper[1] = Record(name="Mira")
        self.assertEqual(keeper[1].name, "Mira")
        self.assertEqual(keeper.count, 4)
        self.assertEqual(len(keeper), 4)

        # Remove at
        keeper.remove_at(2)
        self.assertEqual(keeper[0].name, "George")
        self.assertEqual(keeper[1].name, "Mira")
        self.assertEqual(keeper[2].name, "Ruby")
        self.assertEqual(keeper.count, 3)
        self.assertEqual(len(keeper), 3)

    def test_search(self):
        keeper = RecordKeeper()
        keeper.add(
            Record(name="George", surname="Smith", experience_years=5),  # index 0
            Record(name="Kevin", surname="Marosov", experience_years=6),
            Record(name="Josef", surname="Markov", experience_years=15),
            Record(name="Ruby", surname="Adams", experience_years=20),  # index 3
            Record(name="Mira", surname="Smith", experience_years=18),
            Record(name="Oliver", surname="Smith", experience_years=8),
            Record(name="Kevin", surname="Denton", experience_years=11),  # index 6
            Record(name="Kevin", surname="Adams", experience_years=17),
            Record(name="George", surname="Freeman", experience_years=12)
        )

        # Searches with results
        expected_result = [1, 6, 7]
        search_result = keeper.search(
            lambda x: x.name == "Kevin"
        )
        self.assertListEqual(list(search_result), expected_result)

        expected_result = [4, 5]
        search_result = keeper.search(
            lambda x: x.name != "George",
            lambda x: x.surname == "Smith"
        )
        self.assertListEqual(list(search_result), expected_result)

        expected_result = [2, 3, 4, 6, 7, 8]
        search_result = keeper.search(
            lambda x: x.experience_years > 10
        )
        self.assertListEqual(list(search_result), expected_result)

        expected_result = [0, 2, 6, 8]
        search_result = keeper.search(
            lambda x: x.experience_years <= 15,
            lambda x: x.experience_years != 6,
            lambda x: x.name != "Oliver"
        )
        self.assertListEqual(list(search_result), expected_result)

        # Searches without results
        expected_result = []
        search_result = keeper.search(
            lambda x: x.experience_years < 5,
        )
        self.assertListEqual(list(search_result), expected_result)

        expected_result = []
        search_result = keeper.search(
            lambda x: x.experience_years >= 5,
            lambda x: x.name == "Miles"
        )
        self.assertListEqual(list(search_result), expected_result)

        # Searches with full result
        search_result = keeper.search(
        )
        self.assertListEqual(list(search_result), list(range(len(keeper))))

        search_result = keeper.search(
            lambda x: x.experience_years >= 0
        )
        self.assertListEqual(list(search_result), list(range(len(keeper))))

    def test_search_and_remove(self):
        keeper = RecordKeeper()
        keeper.add(
            Record(name="George", surname="Smith", experience_years=5),  # index 0
            Record(name="Kevin", surname="Marosov", experience_years=6),
            Record(name="Josef", surname="Markov", experience_years=15),
            Record(name="Ruby", surname="Adams", experience_years=20),  # index 3
            Record(name="Mira", surname="Smith", experience_years=18),
            Record(name="Oliver", surname="Smith", experience_years=8),
            Record(name="Kevin", surname="Denton", experience_years=11),  # index 6
            Record(name="Kevin", surname="Adams", experience_years=17),
            Record(name="George", surname="Freeman", experience_years=12)
        )

        # Remove
        removed_count = keeper.search_and_remove(
            lambda x: x.experience_years < 10
        )

        # Check
        self.assertEqual(removed_count, 3)
        self.assertEqual(keeper.count, 6)
        for record in keeper:
            self.assertFalse(record.experience_years < 10)


if __name__ == '__main__':
    unittest.main()
