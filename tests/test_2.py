import pytest
import pandas as pd
from definition_23aa04642e494a8b873b86bc3d8f7eae import log_summary_statistics
import io
import sys

def capture_stdout(func, *args, **kwargs):
    """Captures stdout output of a function."""
    captured_output = io.StringIO()
    sys.stdout = captured_output
    func(*args, **kwargs)
    sys.stdout = sys.__stdout__
    return captured_output.getvalue()

def test_log_summary_statistics_empty_dataframe():
    df = pd.DataFrame()
    output = capture_stdout(log_summary_statistics, df)
    assert "DataFrame is empty." in output

def test_log_summary_statistics_no_numeric_columns():
    df = pd.DataFrame({'col1': ['a', 'b'], 'col2': ['c', 'd']})
    output = capture_stdout(log_summary_statistics, df)
    assert "No numeric columns to summarize." in output

def test_log_summary_statistics_with_numeric_columns():
    df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4.0, 5.0, 6.0], 'col3': ['a', 'b', 'c']})
    output = capture_stdout(log_summary_statistics, df)
    assert "col1" in output
    assert "col2" in output
    assert "col3" not in output

def test_log_summary_statistics_mixed_numeric_types():
    df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4.5, 5.5, 6.5]})
    output = capture_stdout(log_summary_statistics, df)
    assert "col1" in output
    assert "col2" in output
    assert "mean" in output

def test_log_summary_statistics_large_dataframe():
    data = {'col1': range(100), 'col2': [float(i) for i in range(100)]}
    df = pd.DataFrame(data)
    output = capture_stdout(log_summary_statistics, df)
    assert "col1" in output
    assert "col2" in output
    assert "max" in output
