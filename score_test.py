import unittest
import pandas as pd

from app import find_score


class TestFindScore(unittest.TestCase):

    def test_find_score(self):
        # Prepare test data
        questions = [
            {'actual': 'Answer1', 'Choice': 'Answer1'},
            {'actual': 'Answer2', 'Choice': 'Answer1'},
            {'actual': 'Answer1', 'Choice': 'Answer2'},
            {'actual': 'Answer3', 'Choice': 'Answer3'},
            {'actual': 'Answer4', 'Choice': 'Answer4'},
        ]
        dataframe = pd.DataFrame.from_dict(questions)
        expected_score = 3

        # Run the function and check the results
        result = find_score('actual', dataframe)
        self.assertEqual(result, expected_score)


if __name__ == "__main__":
    unittest.main()
