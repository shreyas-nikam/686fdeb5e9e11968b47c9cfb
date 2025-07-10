import pytest
from definition_955dbd97a9af4d7ab4fdb1e26d4029cd import simulate_centrally_cleared_otc_cash_flows
import pandas as pd

def create_mock_data():
    data = {
        'Day': range(5),
        'Spot_Price': [100 + i for i in range(5)]
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_data():
    return create_mock_data()


def test_simulate_centrally_cleared_otc_cash_flows_typical(mock_data):
    initial_otc_price = 100
    contract_size = 1
    initial_margin = 10
    maintenance_margin = 8
    result = simulate_centrally_cleared_otc_cash_flows(initial_otc_price, mock_data['Spot_Price'].tolist(), contract_size, initial_margin, maintenance_margin)
    assert isinstance(result, pd.DataFrame)
    assert 'Day' in result.columns
    assert 'OTC_Cleared_Price' in result.columns
    assert 'Daily_PnL' in result.columns
    assert 'Margin_Balance' in result.columns
    assert 'Cash_Flow' in result.columns


def test_simulate_centrally_cleared_otc_cash_flows_no_price_change(mock_data):
    initial_otc_price = 100
    simulated_spot_prices = [100] * 5
    contract_size = 1
    initial_margin = 10
    maintenance_margin = 8
    result = simulate_centrally_cleared_otc_cash_flows(initial_otc_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin)
    assert result['Daily_PnL'].sum() == 0.0


def test_simulate_centrally_cleared_otc_cash_flows_large_price_change(mock_data):
    initial_otc_price = 100
    contract_size = 1
    initial_margin = 10
    maintenance_margin = 5
    result = simulate_centrally_cleared_otc_cash_flows(initial_otc_price, mock_data['Spot_Price'].tolist(), contract_size, initial_margin, maintenance_margin)
    assert result['Margin_Balance'].min() >= 0


def test_simulate_centrally_cleared_otc_cash_flows_zero_contract_size(mock_data):
    initial_otc_price = 100
    contract_size = 0
    initial_margin = 10
    maintenance_margin = 8
    result = simulate_centrally_cleared_otc_cash_flows(initial_otc_price, mock_data['Spot_Price'].tolist(), contract_size, initial_margin, maintenance_margin)
    assert result['Daily_PnL'].sum() == 0.0


def test_simulate_centrally_cleared_otc_cash_flows_empty_spot_prices():
    initial_otc_price = 100
    simulated_spot_prices = []
    contract_size = 1
    initial_margin = 10
    maintenance_margin = 8
    with pytest.raises(IndexError):
        simulate_centrally_cleared_otc_cash_flows(initial_otc_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin)
