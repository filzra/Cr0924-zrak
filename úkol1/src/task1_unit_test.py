import unittest
from collections import defaultdict
from data_cleanup import find_rows_indexes

class TestFindRowsIndexes(unittest.TestCase):
    
    def test_find_rows_indexes(self):
        # Table-driven test: Each set contains input data and expected output
        test_cases = [
            {
                "name": "Prázdný soubor",
                "input_data": [],
                "expected_output": []
            },
            {
                "name": "Všechny řádky neprázdné",
                "input_data": [
                    {"ObjectID": "abc", "Name": "Item0", "1": "ahoj", "2": "aho"},
                    {"ObjectID": "abc", "Name": "Item1", "1": "bhoj", "2": "bho"},
                    {"ObjectID": "dbc", "Name": "Item2", "1": "choj", "2": "cho"},
                    {"ObjectID": "dbc", "Name": "Item3", "1": "dhoj", "2": "dho"},
                ],
                "expected_output": []  # No rows to remove, no empty name fields
            },
            {
                "name": "Smíšené prázdné a neprázdné pro více ObjectID",
                "input_data": [
                    {"ObjectID": "abc", "Name": "Item0", "1": "ahoj", "2": "aho"},
                    {"ObjectID": "abc", "Name": "", "1": "bhoj", "2": "bho"},
                    {"ObjectID": "abc", "Name": "Item1", "1": "choj", "2": "cho"},
                    {"ObjectID": "dbc", "Name": "", "1": "dhoj", "2": "dho"},
                    {"ObjectID": "dbc", "Name": "", "1": "ehoj", "2": "eho"},
                    {"ObjectID": "dbc", "Name": "Item2", "1": "fhoj", "2": "fho"},
                ],
                "expected_output": [1, 3, 4]  # Empty rows for "abc" and "dbc should be removed, objectID has non empty name values
            },
            {
                "name": "Ponechání prvního prázdného řádku pro více ObjectID",
                "input_data": [
                    {"ObjectID": "abc", "Name": "", "1": "ahoj", "2": "aho"},
                    {"ObjectID": "abc", "Name": "", "1": "bhoj", "2": "bho"},
                    {"ObjectID": "abc", "Name": "", "1": "choj", "2": "cho"},
                    {"ObjectID": "dbc", "Name": "", "1": "dhoj", "2": "dho"},
                    {"ObjectID": "dbc", "Name": "", "1": "ehoj", "2": "eho"},
                    {"ObjectID": "dbc", "Name": "", "1": "fhoj", "2": "fho"},                    
                ],
                "expected_output": [1, 2, 4, 5]  # Keep empty first row for objectIDs with all but empty names, remove the rest
            }
        ]

        
        for case in test_cases:
            with self.subTest(case=case["name"]):                
                result = find_rows_indexes(case["input_data"])
                self.assertEqual(result, case["expected_output"])
                
    # Invalid data test cases such as empty or invalid file...
    # "input_data": [], "expected_output": []

if __name__ == "__main__":
    unittest.main()