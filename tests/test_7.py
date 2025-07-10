import pytest
from definition_bc70b47ad3db42e59a65d8f0ecfff079 import determine_credit_risk

@pytest.mark.parametrize("scenario_type, max_unrealized_mtm, expected", [
    ("Non-Centrally Cleared OTC", 1000, "High"),
    ("Centrally Cleared OTC", 500, "Low"),
    ("Exchange-Traded Futures", None, "Low"),
    ("Invalid Scenario", 100, None), 
    ("Non-Centrally Cleared OTC", None, "High"),
])

def test_determine_credit_risk(scenario_type, max_unrealized_mtm, expected):
    if expected is None:
        with pytest.raises(Exception):
            determine_credit_risk(scenario_type, max_unrealized_mtm)
    else:
        assert determine_credit_risk(scenario_type, max_unrealized_mtm) == expected
