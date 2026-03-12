import pytest
from tools.log_parser import parse_log

def test_correct_counts(): # test to check if the total number of errors and warnings are correct
    result = parse_log("sample_data/sample.log")
    assert result["total_errors"] == 2
    assert result["total_warnings"] == 1

def test_correct_line_numbers(): # test to check if the line numbers of the findings are correct
    result = parse_log("sample_data/sample.log")
    assert result["findings"][0]["line_number"] == 1
    assert result["findings"][1]["line_number"] == 2

def test_missing_file_exits(): # test to check if the program exits with an error code if the file is not found
    with pytest.raises(SystemExit) as e: # use pytest to raise a SystemExit exception if the file is not found
        parse_log("fakefile.log")
    assert e.value.code == 1 # check if the error code is 1