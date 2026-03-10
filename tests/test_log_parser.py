import pytest
from tools.log_parser import parse_log

def test_correct_counts():
    result = parse_log("sample_data/sample.log")
    assert result["total_errors"] == 2
    assert result["total_warnings"] == 1

def test_correct_line_numbers():
    result = parse_log("sample_data/sample.log")
    assert result["findings"][0]["line_number"] == 1
    assert result["findings"][1]["line_number"] == 2

def test_missing_file_exits():
    with pytest.raises(SystemExit) as e:
        parse_log("fakefile.log")
    assert e.value.code == 1