import pytest
import pandas as pd
from definition_a32790cd09f74f44999245fb45868ef7 import validate_and_process_data

def test_validate_and_process_data_valid():
    data = {'Day': [1, 2, 3], 'Spot_Price': [100, 101, 102]}
    df = pd.DataFrame(data)
    result = validate_and_process_data(df)
    assert isinstance(result, pd.DataFrame)
    assert 'Day' in result.columns
    assert 'Spot_Price' in result.columns
    assert len(result) == 3

def test_validate_and_process_data_missing_column():
    data = {'Spot_Price': [100, 101, 102]}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="Required column 'Day' is missing."):
        validate_and_process_data(df)

def test_validate_and_process_data_duplicate_day():
    data = {'Day': [1, 2, 2], 'Spot_Price': [100, 101, 102]}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="Duplicate values found in 'Day' column."):
        validate_and_process_data(df)

def test_validate_and_process_data_missing_values():
    data = {'Day': [1, 2, 3], 'Spot_Price': [100, None, 102]}
    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="Missing values found in 'Spot_Price' column."):
        validate_and_process_data(df)

def test_validate_and_process_data_incorrect_type():
    data = {'Day': ['1', '2', '3'], 'Spot_Price': [100, 101, 102]}
    df = pd.DataFrame(data)
    with pytest.raises(TypeError, match="Incorrect data type for 'Day' column. Expected int64, got object."):
        validate_and_process_data(df)
