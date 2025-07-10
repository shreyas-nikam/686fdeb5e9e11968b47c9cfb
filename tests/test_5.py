import pytest
import pandas as pd
from definition_9cc123988054411db9fb467983caf61d import simulate_forward_cash_flows

@pytest.fixture
def sample_spot_prices():
    return pd.Series([100, 102, 105, 103, 106])

def test_simulate_forward_cash_flows_basic(sample_spot_prices):
    initial_forward_price = 101
    contract_size = 10
    risk_free_rate = 0.05
    result = simulate_forward_cash_flows(initial_forward_price, sample_spot_prices, contract_size, risk_free_rate)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == len(sample_spot_prices)
    assert 'Day' in result.columns
    assert 'Forward_MTM_Value' in result.columns
    assert 'Cash_Flow' in result.columns

def test_simulate_forward_cash_flows_no_price_change(sample_spot_prices):
    initial_forward_price = 100
    contract_size = 10
    risk_free_rate = 0.05
    result = simulate_forward_cash_flows(initial_forward_price, sample_spot_prices, contract_size, risk_free_rate)
    assert result['Forward_MTM_Value'][0] == 0  # Initial MTM should be zero

def test_simulate_forward_cash_flows_decreasing_prices(sample_spot_prices):
    initial_forward_price = 107
    contract_size = 10
    risk_free_rate = 0.05
    result = simulate_forward_cash_flows(initial_forward_price, sample_spot_prices, contract_size, risk_free_rate)
    assert (result['Forward_MTM_Value'] < 0).any()  # MTM value should be negative at some point

def test_simulate_forward_cash_flows_zero_contract_size(sample_spot_prices):
    initial_forward_price = 101
    contract_size = 0
    risk_free_rate = 0.05
    result = simulate_forward_cash_flows(initial_forward_price, sample_spot_prices, contract_size, risk_free_rate)
    assert (result['Cash_Flow'] == 0).all()

def test_simulate_forward_cash_flows_zero_risk_free_rate(sample_spot_prices):
    initial_forward_price = 101
    contract_size = 10
    risk_free_rate = 0.0
    result = simulate_forward_cash_flows(initial_forward_price, sample_spot_prices, contract_size, risk_free_rate)
    # Checks that the Cash_Flow and Forward_MTM_value is not empty and has data
    assert not result['Cash_Flow'].empty
    assert not result['Forward_MTM_Value'].empty
