import pytest
import pandas as pd

from app import find_score, NUM_QUESTIONS


def test_find_score():
    # Prepare test data
    questions = [
        {'actual': 'Answer1', 'Choice': 'Answer1'},
        {'actual': 'Answer2', 'Choice': 'Answer1'},
        {'actual': 'Answer1', 'Choice': 'Answer2'},
        {'actual': 'Answer3', 'Choice': 'Answer3'},
        {'actual': 'Answer4', 'Choice': 'Answer4'},]
    df = pd.DataFrame.from_dict(questions)

    assert find_score('actual', df) == 3


def test_data_quality():
    df = pd.read_csv('lines_2.txt', sep='*')
    cols_in_place = all(col in df.columns.to_list() for col
                        in ['Context','Question', 'Answer', 'Part'])
    len_all_data = len(df)
    len_main_part = len(df[df.Part == 'Middle_4'])

    assert cols_in_place == True
    assert len_all_data > 0
    assert NUM_QUESTIONS <= len_main_part


if __name__ == "__main__":
    pytest.main()
