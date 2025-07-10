import pytest
from definition_ce992dad00e54f3a94cadbdf7659a72a import calculate_futures_price_at_inception

@pytest.mark.parametrize("spot_price, risk_free_rate, time_to_maturity, pv_income, pv_costs, expected", [
    (100, 0.05, 1, 0, 0, 105),
    (100, 0.05, 0.5, 0, 0, 102.46950765955309),
    (50, 0.10, 2, 5, 2, 59.4),
    (100, 0, 1, 10, 0, 90),
    (100, 0.05, 1, 0, 10, 115.5),
])
def test_calculate_futures_price_at_inception(spot_price, risk_free_rate, time_to_maturity, pv_income, pv_costs, expected):
    assert calculate_futures_price_at_inception(spot_price, risk_free_rate, time_to_maturity, pv_income, pv_costs) == expected
