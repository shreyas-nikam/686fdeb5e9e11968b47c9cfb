import pytest
from definition_90d7769a6446461383046d19c9c5e9ad import generate_synthetic_data
import pandas as pd

def is_valid_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        return False
    if not all(col in df.columns for col in ['Day', 'Spot_Price']):
        return False
    if not pd.api.types.is_numeric_dtype(df['Spot_Price']):
        return False
    return True


def test_generate_synthetic_data_positive_case():
    df = generate_synthetic_data(100, 0.01, 30, 0.05, 1, 10, 5)
    assert is_valid_dataframe(df)
    assert len(df) > 0

def test_generate_synthetic_data_zero_volatility():
    df = generate_synthetic_data(100, 0.0, 30, 0.05, 1, 10, 5)
    assert is_valid_dataframe(df)
    assert len(df) > 0
    assert all(df['Spot_Price'] == 100 for price in df['Spot_Price'])


def test_generate_synthetic_data_long_maturity():
    df = generate_synthetic_data(100, 0.01, 365, 0.05, 1, 10, 5)
    assert is_valid_dataframe(df)
    assert len(df) == 365

def test_generate_synthetic_data_contract_size():
    df = generate_synthetic_data(100, 0.01, 30, 0.05, 100, 10, 5)
    assert is_valid_dataframe(df)
    assert len(df) > 0

def test_generate_synthetic_data_initial_spot_zero():
    df = generate_synthetic_data(0, 0.01, 30, 0.05, 1, 10, 5)
    assert is_valid_dataframe(df)
    assert len(df) > 0
