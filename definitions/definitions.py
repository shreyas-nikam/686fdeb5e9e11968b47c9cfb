import pandas as pd
import numpy as np

def generate_synthetic_data(initial_spot, volatility, days_to_maturity, risk_free_rate, contract_size, initial_margin, maintenance_margin):
    """
    Generates synthetic time-series data for asset prices.

    Args:
        initial_spot: Initial asset price.
        volatility: Daily volatility.
        days_to_maturity: Number of days.
        risk_free_rate: Risk-free rate.
        contract_size: Contract size.
        initial_margin: Initial margin.
        maintenance_margin: Maintenance margin.

    Returns:
        A pandas DataFrame with 'Day' and 'Spot_Price' columns.
    """
    spot_prices = [initial_spot]
    for i in range(1, days_to_maturity + 1):
        drift = (risk_free_rate - 0.5 * volatility**2)
        random_shock = np.random.normal(0, volatility)
        spot_price = spot_prices[-1] * np.exp(drift + random_shock)
        spot_prices.append(spot_price)

    df = pd.DataFrame({'Day': range(days_to_maturity + 1), 'Spot_Price': spot_prices[:-1]})
    return df

import pandas as pd

def validate_and_process_data(df):
    """Validates and processes the input DataFrame.
    """

    required_columns = ['Day', 'Spot_Price']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' is missing.")

    if not pd.api.types.is_integer_dtype(df['Day']):
        raise TypeError(f"Incorrect data type for 'Day' column. Expected int64, got {df['Day'].dtype}.")

    if df['Day'].duplicated().any():
        raise ValueError("Duplicate values found in 'Day' column.")

    if df['Spot_Price'].isnull().any():
        raise ValueError("Missing values found in 'Spot_Price' column.")

    return df

import pandas as pd

def log_summary_statistics(df):
    """Provide summary statistics for numeric columns."""
    if df.empty:
        print("DataFrame is empty.")
        return

    numeric_columns = df.select_dtypes(include=['number'])

    if numeric_columns.empty:
        print("No numeric columns to summarize.")
        return

    for col in numeric_columns:
        print(f"Summary statistics for column '{col}':")
        print(df[col].describe())
        print("-" * 30)

def calculate_futures_price_at_inception(spot_price, risk_free_rate, time_to_maturity, pv_income, pv_costs):
    """Compute the theoretical futures price at t=0."""
    return (spot_price - pv_income + pv_costs) * (1 + risk_free_rate)**time_to_maturity

import pandas as pd

def simulate_futures_cash_flows(initial_futures_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    """Simulate daily MTM, cash flows, and margin account balances for a futures contract."""

    if not simulated_spot_prices:
        raise Exception("Simulated spot prices cannot be empty.")

    futures_prices = [initial_futures_price] + simulated_spot_prices[:-1]  # Lag spot prices to get previous day's futures price
    daily_pnl = [(simulated_spot_prices[i] - futures_prices[i]) * contract_size for i in range(len(simulated_spot_prices))]
    
    margin_balance = [0.0] * len(simulated_spot_prices)
    cash_flow = [0.0] * len(simulated_spot_prices)
    
    margin_balance[0] = initial_margin + daily_pnl[0]
    cash_flow[0] = daily_pnl[0] if margin_balance[0] >= 0 else initial_margin + daily_pnl[0]
    
    for i in range(1, len(simulated_spot_prices)):
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = daily_pnl[i]
        
        if margin_balance[i] < maintenance_margin:
            cash_flow[i] = cash_flow[i] - (initial_margin - margin_balance[i]) #cash_flow[i] - (maintenance_margin - margin_balance[i])
            margin_balance[i] = initial_margin #maintenance_margin #reset to initial margin because of margin call

    df = pd.DataFrame({
        'Day': range(1, len(simulated_spot_prices) + 1),
        'Futures_Price': simulated_spot_prices,
        'Daily_PnL': daily_pnl,
        'Margin_Balance': margin_balance,
        'Cash_Flow': cash_flow
    })
    
    return df

import pandas as pd

def simulate_forward_cash_flows(initial_forward_price, simulated_spot_prices, contract_size, risk_free_rate):
    """Simulate MTM and cash flow for a forward contract."""

    df = pd.DataFrame({'Spot_Price': simulated_spot_prices})
    df['Day'] = range(1, len(df) + 1)
    df['Forward_MTM_Value'] = (df['Spot_Price'] - initial_forward_price) * contract_size
    df['Cash_Flow'] = 0.0
    df.loc[df.index[-1], 'Cash_Flow'] = df['Forward_MTM_Value'].iloc[-1]

    return df[['Day', 'Forward_MTM_Value', 'Cash_Flow']]

import pandas as pd

def simulate_centrally_cleared_otc_cash_flows(initial_otc_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    """Simulate daily MTM, cash flows, and margin account balances."""

    n_days = len(simulated_spot_prices)
    otc_prices = [initial_otc_price] * n_days
    daily_pnl = [0.0] * n_days
    margin_balance = [0.0] * n_days
    cash_flow = [0.0] * n_days

    margin_balance[0] = initial_margin
    daily_pnl[0] = (simulated_spot_prices[0] - initial_otc_price) * contract_size
    margin_balance[0] += daily_pnl[0]

    for i in range(1, n_days):
        otc_prices[i] = simulated_spot_prices[i-1]
        daily_pnl[i] = (simulated_spot_prices[i] - otc_prices[i]) * contract_size
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = 0.0  # Initialize cash flow for the day

        if margin_balance[i] < maintenance_margin:
            cash_flow[i] = initial_margin - margin_balance[i]
            margin_balance[i] = initial_margin


    df = pd.DataFrame({
        'Day': range(n_days),
        'OTC_Cleared_Price': otc_prices,
        'Daily_PnL': daily_pnl,
        'Margin_Balance': margin_balance,
        'Cash_Flow': cash_flow
    })

    return df

def determine_credit_risk(scenario_type, max_unrealized_mtm):
    """Provide a qualitative credit risk indicator based on the scenario."""

    if scenario_type == "Non-Centrally Cleared OTC":
        return "High"
    elif scenario_type == "Centrally Cleared OTC":
        return "Low"
    elif scenario_type == "Exchange-Traded Futures":
        return "Low"
    else:
        raise Exception("Invalid scenario type")

import pandas as pd
import numpy as np

def calculate_price_difference_heatmap_data(correlation_range, volatility_range):
    """Generate data for the price difference heatmap."""

    if not (isinstance(correlation_range, tuple) and isinstance(volatility_range, tuple)):
        raise TypeError("Ranges must be tuples.")

    # Handle reversed ranges
    correlation_start, correlation_end = correlation_range
    volatility_start, volatility_end = volatility_range

    num_points = 10  # Number of points in each range for the heatmap
    correlation_values = np.linspace(min(correlation_start, correlation_end), max(correlation_start, correlation_end), num_points)
    volatility_values = np.linspace(min(volatility_start, volatility_end), max(volatility_start, volatility_end), num_points)

    # Create dummy price difference data (replace with actual calculation)
    price_difference_data = np.random.rand(num_points, num_points)

    # Create a Pandas DataFrame for the heatmap
    df = pd.DataFrame(price_difference_data, index=correlation_values, columns=volatility_values)

    return df