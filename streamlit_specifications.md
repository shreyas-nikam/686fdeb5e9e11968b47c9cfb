
# Streamlit Application Requirements Specification: Central Clearing Impact Simulator

## 1. Application Overview

The Central Clearing Impact Simulator is a Streamlit application designed to illustrate the financial implications of central clearing on derivative contracts, specifically contrasting Exchange-Traded Derivatives (ETDs) like futures with Over-The-Counter (OTC) derivatives like forwards. The application aims to provide a practical tool for risk managers, compliance officers, and institutional finance students to understand how margin requirements and daily settlement reduce cash flow and price differences between these contract types.

**Purpose and Objectives:**
*   **Purpose**: To simulate and visualize the impact of central clearing on derivatives, emphasizing the convergence of OTC derivatives towards futures-like margining and settlement.
*   **Objectives**:
    *   Understand the key insights from financial documents regarding central clearing's role in OTC derivatives markets.
    *   Analyze how margining requirements reduce the cash flow impact difference between ETDs and OTC derivatives.
    *   Identify the implications of central clearing for credit risk.
    *   Explore factors that still contribute to price differences between futures and forwards, even with central clearing (e.g., interest rate correlation and volatility).
    *   Provide an interactive platform for scenario analysis.

## 2. User Interface Requirements

The application will feature an intuitive and interactive interface, primarily organized with input controls in a sidebar and analytical outputs in the main display area.

**Layout and Navigation Structure:**
*   **Sidebar (`st.sidebar`)**: Will host all user input widgets for scenario selection and simulation parameters.
*   **Main Content Area**: Will display key visualizations, summary statistics, credit risk indicators, and narrative explanations. This area will be dynamically updated based on sidebar selections. Sections for different visualizations can be organized using `st.expander` or `st.tabs`.

**Input Widgets and Controls:**
*   **Scenario Selection (`st.radio` or `st.selectbox`)**:
    *   "Non-Centrally Cleared OTC"
    *   "Centrally Cleared OTC"
    *   "Exchange-Traded Futures"
    *   **Help Text**: "Select the type of derivative contract to simulate."
*   **Market Volatility Simulation (`st.slider`)**:
    *   **Parameter**: `volatility` (daily volatility).
    *   **Range**: e.g., $0.005$ to $0.05$.
    *   **Help Text**: "Adjust daily market volatility, influencing spot price changes."
*   **Simulation Parameters (`st.number_input` or `st.slider`)**:
    *   `initial_spot`: Initial asset price.
    *   `days_to_maturity`: Number of days for the simulation.
    *   `risk_free_rate`: Daily risk-free rate.
    *   `contract_size`: Size of the derivative contract.
    *   `initial_margin`: Initial margin requirement (for futures/centrally cleared OTC).
    *   `maintenance_margin`: Maintenance margin requirement (for futures/centrally cleared OTC).
    *   **Help Text for each**: Provide a brief description of the parameter's role.
*   **Heatmap Parameters (`st.slider`)**:
    *   `correlation_range`: Tuple (min, max) for correlation values.
    *   `volatility_range`: Tuple (min, max) for volatility values.
    *   **Help Text**: "Define ranges for correlation and volatility to generate the price difference heatmap data."

**Visualization Components:**
*   **Spot Price Trend Plot**: A line chart showing the simulated `Spot_Price` over `Day`.
    *   **Title**: "Simulated Spot Price Trend"
    *   **Axes**: 'Day' on x-axis, 'Spot Price' on y-axis.
    *   **Interactivity**: Zoom, pan (using Plotly or Altair).
*   **Cash Flow & Margin Visualization**: A time-series plot (line chart) showing:
    *   `Daily_PnL` for all scenarios.
    *   `Margin_Balance` and `Cash_Flow` for "Centrally Cleared OTC" and "Exchange-Traded Futures" scenarios.
    *   **Title**: "Daily Cash Flows and Margin Account Fluctuations"
    *   **Axes**: 'Day' on x-axis, 'Value' on y-axis.
    *   **Legends**: Clearly distinguish between `Daily_PnL`, `Margin_Balance`, and `Cash_Flow`.
    *   **Interactivity**: Zoom, pan.
*   **Price Difference Heatmap**: A heatmap showing how factors like interest rate correlation and volatility might still cause price differences between futures and forwards.
    *   **Title**: "Residual Price Differences: Impact of Correlation and Volatility"
    *   **Axes**: 'Correlation' on one axis, 'Volatility' on the other.
    *   **Color Scale**: Represent price difference magnitude.
    *   **Interactivity**: Tooltips on hover to show exact values.

**Interactive Elements and Feedback Mechanisms:**
*   **Real-time Updates**: Changes to any input widget will automatically re-run the relevant calculations and update all displayed outputs and visualizations.
*   **Tooltips and Inline Help**: All input controls will have `st.help` or `st.tooltip` to describe their function.
*   **Credit Risk Indicator**: A qualitative output (e.g., `st.metric` or `st.write`) displaying "High", "Medium", or "Low" credit risk based on the selected scenario.
*   **Data Validation Feedback**: Error messages (`st.error`) will be displayed if input data fails validation checks (e.g., missing columns, wrong data types, null values).
*   **Summary Statistics Display**: Numerical summary statistics for generated data will be displayed in a table (`st.dataframe` or `st.table`).

## 3. Additional Requirements

**Real-time Updates and Responsiveness:**
*   The Streamlit application inherently provides real-time updates: any change to an input widget will trigger a re-run of the script and update all dependent outputs and visualizations immediately.
*   The application must remain responsive and execute end-to-end within a reasonable time (e.g., less than 5 minutes) on mid-spec hardware, given the synthetic nature of the data and fixed number of simulation days.

**Annotation and Tooltip Specifications:**
*   **Input Widgets**: As detailed in section 2, provide clear, concise help text or tooltips for every adjustable parameter (`st.number_input`, `st.slider`, `st.radio`, `st.selectbox`).
*   **Visualizations**:
    *   All charts and graphs (`Spot Price Trend`, `Cash Flow & Margin`, `Price Difference Heatmap`) will have clear, descriptive titles.
    *   Axes will be appropriately labeled with units where applicable.
    *   Legends will be present to differentiate multiple series in line plots.
    *   A color-blind-friendly palette will be used for all visualizations.
    *   Font size for titles, labels, and legends will be $\geq 12$ pt for readability.
    *   Interactive plot libraries (e.g., Plotly, Altair) will enable hover-over tooltips to display specific data points (e.g., `Day`, `Spot_Price`, `Cash_Flow`, `Margin_Balance` or `Correlation`, `Volatility`, `Price Difference`).

## 4. Notebook Content and Code Requirements

This section details how the provided Jupyter notebook content will be integrated into the Streamlit application. All required Python functions will be extracted and called appropriately based on user interaction.

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px # For interactive plots
import plotly.graph_objects as go # For heatmap if needed, or px.imshow

# --- Application Configuration ---
st.set_page_config(
    page_title="Central Clearing Impact Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. Generating Synthetic Market Data ---
# Business Value: To accurately simulate the behavior of derivatives, we first need realistic,
# albeit synthetic, market data.
# Technical Implementation: Simplified geometric Brownian motion model.

# LaTeX Formula for reference in the app
st.sidebar.markdown("### Market Data Simulation")
st.sidebar.markdown(r"""
The daily spot price movement is modeled by:
$$ S_t = S_{t-1} \times e^{(\text{drift} + \text{random\_shock})} $$
where:
- $S_t$ is the spot price at time $t$.
- $S_{t-1}$ is the spot price at the previous time step.
- $\text{drift} = (\text{risk\_free\_rate} - 0.5 \times \text{volatility}^2)$
- $\text{random\_shock} = \text{np.random.normal}(0, \text{volatility})$
""")

@st.cache_data
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

# --- 2. Data Validation and Pre-processing ---
# Business Value: Ensures data integrity and quality before financial calculations.
# Technical Implementation: Checks for column presence, data types, duplicates, and missing values.

@st.cache_data
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

# --- 3. Logging Summary Statistics ---
# Business Value: Provides a quick, comprehensive overview of numerical data.
# Technical Implementation: Uses pandas `describe()` method.

def log_summary_statistics(df):
    """Provide summary statistics for numeric columns."""
    if df.empty:
        st.write("DataFrame is empty.")
        return
    numeric_columns = df.select_dtypes(include=['number'])
    if numeric_columns.empty:
        st.write("No numeric columns to summarize.")
        return
    st.subheader("Summary Statistics for Simulated Data")
    for col in numeric_columns:
        st.write(f"**Column: '{col}'**")
        st.dataframe(df[col].describe()) # Display as Streamlit DataFrame
    st.markdown("---")

# --- 4. Calculating Futures Price at Inception ---
# Business Value: Determines the fair price of a futures contract at creation.
# Technical Implementation: Uses the cost of carry model.

# LaTeX Formula for reference in the app
st.sidebar.markdown("### Futures Price at Inception")
st.sidebar.markdown(r"""
The theoretical futures price at time $0$ is:
$$ F_0 = (S_0 - PV_{\text{Income}} + PV_{\text{Costs}}) \times (1 + r)^T $$
""")

@st.cache_data
def calculate_futures_price_at_inception(spot_price, risk_free_rate, time_to_maturity, pv_income, pv_costs):
    """Compute the theoretical futures price at t=0."""
    return (spot_price - pv_income + pv_costs) * (1 + risk_free_rate)**time_to_maturity

# --- 5. Simulating Futures Cash Flows ---
# Business Value: Critical for managing liquidity and assessing financial risks.
# Technical Implementation: Simulates daily mark-to-market (MTM) process and margin adjustments.

# LaTeX Formulas for reference in the app
st.sidebar.markdown("### Futures Cash Flow Formulas")
st.sidebar.markdown(r"""
Daily PnL calculation:
$$ \text{Daily PnL}_t = (\text{Futures Price}_t - \text{Futures Price}_{t-1}) \times \text{Contract Size} $$
Margin Balance update:
$$ \text{Margin Balance}_t = \text{Margin Balance}_{t-1} + \text{Daily PnL}_t $$
Cash Flow determination (Margin Call):
$$
\text{If } \text{Margin Balance}_t < \text{Maintenance Margin}: \\
\text{Cash Flow}_t = \text{Initial Margin} - \text{Margin Balance}_t
$$
Otherwise:
$$
\text{If } \text{Margin Balance}_t >= \text{Maintenance Margin}: \\
\text{Cash Flow}_t = \text{Daily PnL}_t
$$
""")

@st.cache_data
def simulate_futures_cash_flows(initial_futures_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    """Simulate daily MTM, cash flows, and margin account balances for a futures contract."""
    if not simulated_spot_prices:
        raise Exception("Simulated spot prices cannot be empty.")

    futures_prices = [initial_futures_price] + simulated_spot_prices[:-1]
    daily_pnl = [(simulated_spot_prices[i] - futures_prices[i]) * contract_size for i in range(len(simulated_spot_prices))]

    margin_balance = [0.0] * len(simulated_spot_prices)
    cash_flow = [0.0] * len(simulated_spot_prices)

    margin_balance[0] = initial_margin + daily_pnl[0]
    cash_flow[0] = daily_pnl[0] if margin_balance[0] >= maintenance_margin else initial_margin - margin_balance[0]
    if margin_balance[0] < maintenance_margin:
        margin_balance[0] = initial_margin

    for i in range(1, len(simulated_spot_prices)):
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = daily_pnl[i]

        if margin_balance[i] < maintenance_margin:
            cash_flow[i] = initial_margin - margin_balance[i]
            margin_balance[i] = initial_margin

    df = pd.DataFrame({
        'Day': range(1, len(simulated_spot_prices) + 1),
        'Futures_Price': simulated_spot_prices,
        'Daily_PnL': daily_pnl,
        'Margin_Balance': margin_balance,
        'Cash_Flow': cash_flow
    })
    return df

# --- 6. Simulating Forward Cash Flows ---
# Business Value: Allows comparison of cash flow dynamics between forwards and futures.
# Technical Implementation: Calculates MTM and a single cash flow at maturity.

# LaTeX Formulas for reference in the app
st.sidebar.markdown("### Forward Cash Flow Formulas")
st.sidebar.markdown(r"""
Forward MTM Value:
$$ \text{Forward MTM Value}_t = (\text{Spot Price}_t - \text{Initial Forward Price}) \times \text{Contract Size} $$
Cash Flow at Maturity:
$$ \text{Cash Flow} = \text{Forward MTM Value}_{\text{maturity}} $$
""")

@st.cache_data
def simulate_forward_cash_flows(initial_forward_price, simulated_spot_prices, contract_size, risk_free_rate):
    """Simulate MTM and cash flow for a forward contract."""
    df = pd.DataFrame({'Spot_Price': simulated_spot_prices})
    df['Day'] = range(1, len(df) + 1)
    df['Forward_MTM_Value'] = (df['Spot_Price'] - initial_forward_price) * contract_size
    df['Cash_Flow'] = 0.0
    df.loc[df.index[-1], 'Cash_Flow'] = df['Forward_MTM_Value'].iloc[-1]
    return df[['Day', 'Forward_MTM_Value', 'Cash_Flow']]

# --- 7. Simulating Centrally Cleared OTC Cash Flows ---
# Business Value: Understand how central clearing mitigates credit risk and alters cash flow.
# Technical Implementation: Simulates daily MTM, margin adjustments, and cash flows for cleared OTC.

# LaTeX Formulas for reference in the app
st.sidebar.markdown("### Centrally Cleared OTC Cash Flow Formulas")
st.sidebar.markdown(r"""
Daily PnL calculation:
$$ \text{Daily PnL}_t = (\text{Spot Price}_t - \text{OTC Cleared Price}_{t-1}) \times \text{Contract Size} $$
Margin Balance update:
$$ \text{Margin Balance}_t = \text{Margin Balance}_{t-1} + \text{Daily PnL}_t $$
Cash Flow determination (Margin Call):
$$
\text{If } \text{Margin Balance}_t < \text{Maintenance Margin}: \\
\text{Cash Flow}_t = \text{Initial Margin} - \text{Margin Balance}_t
$$
""")

@st.cache_data
def simulate_centrally_cleared_otc_cash_flows(initial_otc_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    """Simulate daily MTM, cash flows, and margin account balances."""
    n_days = len(simulated_spot_prices)
    otc_prices = [initial_otc_price] + simulated_spot_prices[:-1]
    daily_pnl = [(simulated_spot_prices[i] - otc_prices[i]) * contract_size for i in range(n_days)]

    margin_balance = [0.0] * n_days
    cash_flow = [0.0] * n_days

    margin_balance[0] = initial_margin + daily_pnl[0]
    if margin_balance[0] < maintenance_margin:
        cash_flow[0] = initial_margin - margin_balance[0]
        margin_balance[0] = initial_margin

    for i in range(1, n_days):
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = 0.0  # Initialize cash flow for the day

        if margin_balance[i] < maintenance_margin:
            cash_flow[i] = initial_margin - margin_balance[i]
            margin_balance[i] = initial_margin

    df = pd.DataFrame({
        'Day': range(n_days),
        'OTC_Cleared_Price': simulated_spot_prices, # The 'otc_prices' in the original notebook calculation was previous day's spot. This matches the spirit of daily settlement.
        'Daily_PnL': daily_pnl,
        'Margin_Balance': margin_balance,
        'Cash_Flow': cash_flow
    })
    return df


# --- 8. Determining Credit Risk ---
# Business Value: Provides a qualitative assessment of credit risk for different clearing scenarios.
# Technical Implementation: Simple conditional logic.

def determine_credit_risk(scenario_type):
    """Provide a qualitative credit risk indicator based on the scenario."""
    if scenario_type == "Non-Centrally Cleared OTC":
        return "High"
    elif scenario_type == "Centrally Cleared OTC":
        return "Low"
    elif scenario_type == "Exchange-Traded Futures":
        return "Low"
    else:
        return "N/A" # Should not happen with radio buttons

# --- 9. Calculating Price Difference Heatmap Data ---
# Business Value: Visualize how correlation and volatility impact residual price differences.
# Technical Implementation: Generates dummy data (to be replaced with a sophisticated model).

@st.cache_data
def calculate_price_difference_heatmap_data(correlation_range, volatility_range):
    """Generate data for the price difference heatmap."""
    if not (isinstance(correlation_range, tuple) and isinstance(volatility_range, tuple)):
        raise TypeError("Ranges must be tuples.")

    correlation_start, correlation_end = correlation_range
    volatility_start, volatility_end = volatility_range

    num_points = 10  # Number of points in each range for the heatmap
    correlation_values = np.linspace(min(correlation_start, correlation_end), max(correlation_start, correlation_end), num_points)
    volatility_values = np.linspace(min(volatility_start, volatility_end), max(volatility_start, volatility_end), num_points)

    # Create dummy price difference data (replace with actual calculation in a real app)
    # The current notebook uses np.random.rand, which will be replicated here.
    price_difference_data = np.random.rand(num_points, num_points)

    df = pd.DataFrame(price_difference_data, index=correlation_values.round(2), columns=volatility_values.round(3))
    df.index.name = "Interest Rate Correlation"
    df.columns.name = "Interest Rate Volatility"
    return df

# --- Streamlit UI Layout and Logic ---

st.title("Central Clearing Impact Simulator")
st.write("Explore the impact of central clearing on the differences between exchange-traded derivatives (ETDs) like futures and over-the-counter (OTC) derivatives like forwards.")

with st.sidebar:
    st.header("Simulation Parameters")
    # Simulation Parameters
    initial_spot = st.number_input("Initial Spot Price ($S_0$)", value=100.0, min_value=1.0, help="Initial price of the underlying asset.")
    days_to_maturity = st.number_input("Days to Maturity ($T$)", value=20, min_value=1, help="Number of days for the simulation period.")
    volatility = st.slider("Daily Volatility", value=0.01, min_value=0.001, max_value=0.05, step=0.001, format="%.3f", help="Magnitude of daily price fluctuations (standard deviation).")
    risk_free_rate = st.number_input("Daily Risk-Free Rate ($r$)", value=0.0001, min_value=0.00001, max_value=0.001, step=0.00001, format="%.5f", help="Daily risk-free interest rate for compounding.")
    contract_size = st.number_input("Contract Size", value=100, min_value=1, help="Number of units of the underlying asset per contract.")
    initial_margin = st.number_input("Initial Margin", value=1000, min_value=100, help="Initial amount of collateral required to open a position.")
    maintenance_margin = st.number_input("Maintenance Margin", value=800, min_value=50, help="Minimum margin balance to be maintained; triggers a margin call if breached.")

    st.markdown("---")
    st.header("Scenario Selection")
    scenario_type = st.radio(
        "Choose Derivative Type:",
        ("Non-Centrally Cleared OTC", "Centrally Cleared OTC", "Exchange-Traded Futures"),
        help="Select the type of derivative contract to simulate and compare."
    )
    st.markdown("---")
    st.header("Heatmap Parameters")
    corr_min = st.slider("Min Correlation", -1.0, 1.0, -0.5, 0.1)
    corr_max = st.slider("Max Correlation", -1.0, 1.0, 0.5, 0.1)
    vol_min = st.slider("Min Volatility (Heatmap)", 0.0, 1.0, 0.1, 0.01)
    vol_max = st.slider("Max Volatility (Heatmap)", 0.0, 1.0, 0.4, 0.01)
    correlation_range = (corr_min, corr_max)
    volatility_range = (vol_min, vol_max)


# --- Simulation Logic ---
try:
    # Generate synthetic data
    synthetic_data = generate_synthetic_data(initial_spot, volatility, days_to_maturity, risk_free_rate, contract_size, initial_margin, maintenance_margin)

    # Validate data
    validated_data = validate_and_process_data(synthetic_data.copy())

    # Display spot price trend
    st.subheader("1. Simulated Spot Price Trend")
    fig_spot = px.line(validated_data, x='Day', y='Spot_Price', title='Simulated Spot Price Over Time')
    fig_spot.update_layout(yaxis_title="Spot Price ($)", xaxis_title="Day", font_size=12)
    st.plotly_chart(fig_spot, use_container_width=True)

    # Log summary statistics
    log_summary_statistics(validated_data)

    # Calculate and display theoretical futures price at inception
    st.subheader("2. Theoretical Futures Price at Inception")
    pv_income_futures = st.number_input("Present Value of Income ($PV_{\\text{Income}}$) for Futures Pricing", value=0.0, help="Present value of any income generated by the underlying asset.")
    pv_costs_futures = st.number_input("Present Value of Costs ($PV_{\\text{Costs}}$) for Futures Pricing", value=0.0, help="Present value of any costs associated with holding the underlying asset.")
    futures_price_inception = calculate_futures_price_at_inception(initial_spot, risk_free_rate, days_to_maturity, pv_income_futures, pv_costs_futures)
    st.metric("Calculated Futures Price at Inception ($F_0$)", f"${futures_price_inception:,.2f}")
    st.markdown("---")

    st.subheader(f"3. Simulation Results for: {scenario_type}")

    df_results = None
    if scenario_type == "Non-Centrally Cleared OTC":
        df_results = simulate_forward_cash_flows(initial_spot, validated_data['Spot_Price'].tolist(), contract_size, risk_free_rate)
        # Rename columns for consistent plotting if necessary
        df_results = df_results.rename(columns={'Forward_MTM_Value': 'MTM_Value'})
    elif scenario_type == "Centrally Cleared OTC":
        df_results = simulate_centrally_cleared_otc_cash_flows(initial_spot, validated_data['Spot_Price'].tolist(), contract_size, initial_margin, maintenance_margin)
        df_results = df_results.rename(columns={'OTC_Cleared_Price': 'Futures_Price'}) # Align column names
    elif scenario_type == "Exchange-Traded Futures":
        df_results = simulate_futures_cash_flows(initial_spot, validated_data['Spot_Price'].tolist(), contract_size, initial_margin, maintenance_margin)

    if df_results is not None:
        st.dataframe(df_results.head())

        # Plot Cash Flows and Margin (if applicable)
        st.subheader("Daily Cash Flows and Margin Account Fluctuations")
        fig_cash_flow = go.Figure()
        fig_cash_flow.add_trace(go.Scatter(x=df_results['Day'], y=df_results['Cash_Flow'], mode='lines', name='Cash Flow'))
        if 'Daily_PnL' in df_results.columns:
            fig_cash_flow.add_trace(go.Scatter(x=df_results['Day'], y=df_results['Daily_PnL'], mode='lines', name='Daily PnL'))
        if 'Margin_Balance' in df_results.columns:
            fig_cash_flow.add_trace(go.Scatter(x=df_results['Day'], y=df_results['Margin_Balance'], mode='lines', name='Margin Balance'))
        
        fig_cash_flow.update_layout(
            title='Cash Flow & Margin Visualization',
            xaxis_title='Day',
            yaxis_title='Value ($)',
            hovermode='x unified',
            font=dict(size=12)
        )
        st.plotly_chart(fig_cash_flow, use_container_width=True)

        # Credit Risk Indicator
        st.subheader("Credit Risk Assessment")
        # The determine_credit_risk function in notebook does not use max_unrealized_mtm.
        # It only takes scenario_type.
        credit_risk = determine_credit_risk(scenario_type)
        st.metric("Credit Risk Exposure", credit_risk)
        st.markdown("---")

    # Price Difference Heatmap
    st.subheader("4. Residual Price Differences: Impact of Correlation and Volatility")
    try:
        heatmap_data = calculate_price_difference_heatmap_data(correlation_range, volatility_range)
        fig_heatmap = px.imshow(heatmap_data,
                                 labels=dict(x="Interest Rate Volatility", y="Interest Rate Correlation", color="Price Difference"),
                                 x=heatmap_data.columns.astype(str),
                                 y=heatmap_data.index.astype(str),
                                 color_continuous_scale="Viridis",
                                 title="Price Difference Heatmap (Dummy Data)")
        fig_heatmap.update_layout(font_size=12)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown("*(Note: Heatmap data is currently dummy data and would be replaced by actual calculations based on "
                    "interest rate correlation and volatility in a production environment.)*")
    except TypeError as e:
        st.error(f"Error generating heatmap: {e}. Please ensure correlation and volatility ranges are valid.")


except (ValueError, TypeError, Exception) as e:
    st.error(f"An error occurred: {e}. Please check your inputs.")


st.markdown("---")
st.header("References")
st.markdown("""
[1] "REFRESHER READING 2024 CFA® PROGRAM LEVEL 1 Derivatives: Pricing and Valuation of Futures Contracts", CFA Institute, 2023. This document explains the impact of central clearing on OTC derivatives and how it affects the differences between futures and forward contracts, including the role of margin requirements.
""")

st.markdown("---")
st.markdown("## QuantUniversity License")
st.markdown("""
© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  
- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@quantuniversity.com](mailto:info@quantuniversity.com)
""")
```
