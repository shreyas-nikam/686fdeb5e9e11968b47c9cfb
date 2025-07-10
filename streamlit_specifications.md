
# Streamlit Application Requirements Specification: Central Clearing Impact Simulator

This document outlines the requirements for developing a Streamlit application based on the provided Jupyter notebook content and user requirements. It will serve as a blueprint, detailing interactive components and integrating relevant code and mathematical formulas.

## 1. Application Overview

The **Central Clearing Impact Simulator** Streamlit application aims to provide an interactive platform for users to explore and understand the significant impact of central clearing on derivatives markets. Specifically, it will focus on how margin requirements and daily settlement for centrally cleared OTC (Over-the-Counter) contracts reduce the cash flow and price differences between ETDs (Exchange-Traded Derivatives) like futures and OTC forwards.

**Purpose and Objectives:**
*   To enable users to understand the key insights contained in the uploaded document regarding central clearing.
*   To visualize the cash flow dynamics and margin account fluctuations for different derivative contract types (Non-Centrally Cleared OTC, Centrally Cleared OTC, Exchange-Traded Futures).
*   To allow users to simulate various market conditions by adjusting parameters like volatility.
*   To provide a qualitative assessment of credit risk across different clearing scenarios.
*   To illustrate how factors like interest rate correlation and volatility can still lead to price differences between futures and forwards, even with central clearing.

**Target Audience:** Risk managers, compliance officers, and institutional finance students seeking to deepen their understanding of derivatives, central clearing, and associated risks.

## 2. User Interface Requirements

The application will feature a clear and intuitive layout, likely utilizing Streamlit's sidebar for user inputs and the main panel for displaying results, visualizations, and summary information.

### Layout and Navigation Structure

*   **Sidebar:** Will house all input widgets and controls for scenario selection and parameter adjustments.
*   **Main Panel:** Will display the simulation results, interactive charts, data tables, and credit risk indicators.
*   **Sections:** The main panel will be logically divided to present different aspects of the simulation (e.g., "Market Data Simulation," "Cash Flow & Margin Analysis," "Credit Risk Assessment," "Price Difference Analysis").
*   **Visual Aesthetics:** Adhere to a color-blind-friendly palette. All text, including labels, axes, and legends in visualizations, will have a font size $\ge 12$ pt for readability. Clear titles will be provided for all plots and sections.

### Input Widgets and Controls

The application will feature the following interactive input widgets in the sidebar, allowing users to customize simulations:

1.  **Market Scenario Parameters (for `generate_synthetic_data`):**
    *   **Initial Spot Price:** `st.number_input` (e.g., `100.0`, min `1.0`, step `0.1`)
    *   **Daily Volatility:** `st.slider` (e.g., `0.01`, min `0.001`, max `0.1`, step `0.001`)
    *   **Days to Maturity:** `st.slider` (e.g., `20`, min `5`, max `250`, step `1`)
    *   **Daily Risk-Free Rate:** `st.number_input` (e.g., `0.0001`, min `0.00001`, max `0.01`, step `0.00001`)
    *   **Contract Size:** `st.number_input` (e.g., `100`, min `1`, step `1`)
    *   **Initial Margin:** `st.number_input` (e.g., `1000`, min `10`, step `10`)
    *   **Maintenance Margin:** `st.number_input` (e.g., `800`, min `10`, step `10`, ensuring `maintenance_margin < initial_margin`)

2.  **Futures/Forward Pricing Parameters (for `calculate_futures_price_at_inception`):**
    *   **Present Value of Income ($PV_{\text{Income}}$):** `st.number_input` (e.g., `0.0`, min `0.0`, step `0.1`)
    *   **Present Value of Costs ($PV_{\text{Costs}}$):** `st.number_input` (e.g., `0.0`, min `0.0`, step `0.1`)

3.  **Clearing Scenario Selection:**
    *   **Scenario Type:** `st.selectbox` or `st.radio` (options: "Non-Centrally Cleared OTC", "Centrally Cleared OTC", "Exchange-Traded Futures"). This selection will dynamically update the displayed cash flow plot and credit risk indicator.

4.  **Price Difference Heatmap Parameters (for `calculate_price_difference_heatmap_data`):**
    *   **Correlation Range (Min/Max):** Two `st.slider` widgets or `st.columns` with `st.number_input` (e.g., `(-0.5, 0.5)`)
    *   **Volatility Range (Min/Max):** Two `st.slider` widgets or `st.columns` with `st.number_input` (e.g., `(0.1, 0.4)`)

### Visualization Components

The application will utilize interactive charts and tables to display simulation results:

1.  **Synthetic Market Data Plot:**
    *   **Type:** Line chart (`st.line_chart`).
    *   **Content:** Time-series plot of `Spot_Price` over `Day`.
    *   **Purpose:** Visualize the underlying asset's price movement.

2.  **Cash Flow & Margin Visualization (Core Visual - Trend Plot):**
    *   **Type:** Interactive Line/Area chart (e.g., using Altair or Plotly for `st.altair_chart`/`st.plotly_chart`).
    *   **Content:**
        *   Daily Cash Flows for the selected scenario (`Cash_Flow`).
        *   Daily Margin Balance (for Futures and Centrally Cleared OTC scenarios).
    *   **Purpose:** Illustrate "Exhibit 6: Margin Requirements for Centrally Cleared OTC Derivatives" and compare cash flow patterns across different clearing mechanisms.

3.  **Credit Risk Indicator:**
    *   **Type:** Text display (`st.write`).
    *   **Content:** A qualitative indicator ("High", "Medium", "Low") based on the chosen scenario.

4.  **Price Difference Heatmap (Core Visual - Aggregated Comparison):**
    *   **Type:** Interactive Heatmap (e.g., using Altair for `st.altair_chart`).
    *   **Content:** Shows how combinations of `Correlation` and `Volatility` influence simulated price differences between futures and forwards.
    *   **Purpose:** Provide insights into residual price differences even with central clearing.

### Interactive Elements and Feedback Mechanisms

*   **Dynamic Updates:** All plots and displayed information will automatically update as users change input parameters.
*   **Error Handling:** Implement `try-except` blocks for data validation. Invalid inputs or missing data will trigger informative `st.error` messages.
*   **Summary Statistics Display:** Use `st.dataframe` or `st.table` to display the output of `log_summary_statistics`.

## 3. Additional Requirements

### Real-time Updates and Responsiveness

The Streamlit application will leverage Streamlit's reactive model to ensure that all calculations and visualizations update in near real-time as users interact with the input widgets. This provides immediate feedback and a dynamic exploration experience. Performance will be optimized to execute end-to-end within the 5-minute constraint on a mid-spec laptop.

### Annotation and Tooltip Specifications

*   Every input widget will be accompanied by concise, inline help text or tooltips (using Streamlit's `help` parameter or `st.info` for longer descriptions) to explain its purpose and impact on the simulation.
*   Charts will include clearly labeled axes, titles, and legends to ensure interpretability without external reference.

## 4. Notebook Content and Code Requirements

This section details how the functions and concepts from the Jupyter notebook will be integrated into the Streamlit application.

### General Structure for Streamlit Application

```python
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt # For advanced plotting like heatmaps

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Central Clearing Impact Simulator")

st.title("Central Clearing Impact Simulator")
st.markdown("""
This application explores the impact of central clearing on the differences between
exchange-traded derivatives (ETDs) like futures and over-the-counter (OTC) derivatives like forwards.
It focuses on how margin requirements and daily settlement for centrally cleared OTC contracts
reduce the cash flow and price differences.
""")

# --- 1. Define all functions from the Jupyter Notebook ---

# (Detailed function definitions will go here)

# --- 2. Sidebar for User Inputs ---
st.sidebar.header("Simulation Parameters")

# Parameters for generate_synthetic_data
initial_spot = st.sidebar.number_input("Initial Spot Price ($S_0$)", value=100.0, min_value=1.0, step=0.1, help="Starting price of the underlying asset.")
volatility = st.sidebar.slider("Daily Volatility", value=0.01, min_value=0.001, max_value=0.1, step=0.001, help="Magnitude of daily price fluctuations for the asset.")
days_to_maturity = st.sidebar.slider("Days to Maturity ($T$)", value=20, min_value=5, max_value=250, step=1, help="Number of days until the contract matures.")
risk_free_rate = st.sidebar.number_input("Daily Risk-Free Rate ($r$)", value=0.0001, min_value=0.00001, max_value=0.01, format="%.5f", help="Daily risk-free interest rate for discounting.")
contract_size = st.sidebar.number_input("Contract Size", value=100, min_value=1, step=1, help="The number of units of the underlying asset per contract.")
initial_margin = st.sidebar.number_input("Initial Margin", value=1000, min_value=10, step=10, help="Initial capital required to open a margined position.")
maintenance_margin = st.sidebar.number_input("Maintenance Margin", value=800, min_value=10, step=10, help="Minimum margin level required to keep a position open. A margin call occurs if balance falls below this.")
if maintenance_margin >= initial_margin:
    st.sidebar.error("Maintenance Margin must be less than Initial Margin.")
    st.stop()

# Parameters for calculate_futures_price_at_inception (additional inputs)
pv_income = st.sidebar.number_input("PV of Income ($PV_{\\text{Income}}$)", value=0.0, min_value=0.0, step=0.1, help="Present value of any income generated by the underlying asset (e.g., dividends).")
pv_costs = st.sidebar.number_input("PV of Costs ($PV_{\\text{Costs}}$)", value=0.0, min_value=0.0, step=0.1, help="Present value of any costs associated with holding the underlying asset (e.g., storage costs).")

st.sidebar.markdown("---")
st.sidebar.header("Scenario Selection")
scenario_type = st.sidebar.radio(
    "Select Derivative Scenario:",
    ("Exchange-Traded Futures", "Centrally Cleared OTC", "Non-Centrally Cleared OTC")
)

st.sidebar.markdown("---")
st.sidebar.header("Price Difference Heatmap Parameters")
col_corr_min, col_corr_max = st.sidebar.columns(2)
with col_corr_min:
    correlation_min = st.number_input("Min Correlation", value=-0.5, min_value=-1.0, max_value=1.0, step=0.05, help="Minimum correlation between futures prices and interest rates.")
with col_corr_max:
    correlation_max = st.number_input("Max Correlation", value=0.5, min_value=-1.0, max_value=1.0, step=0.05, help="Maximum correlation between futures prices and interest rates.")
correlation_range = (correlation_min, correlation_max)

col_vol_min, col_vol_max = st.sidebar.columns(2)
with col_vol_min:
    volatility_min = st.number_input("Min IR Volatility", value=0.1, min_value=0.0, max_value=1.0, step=0.01, help="Minimum interest rate volatility.")
with col_vol_max:
    volatility_max = st.number_input("Max IR Volatility", value=0.4, min_value=0.0, max_value=1.0, step=0.01, help="Maximum interest rate volatility.")
volatility_range = (volatility_min, volatility_max)

# --- 3. Main Panel: Calculations and Displays ---

# Call synthetic data generation and validation
st.header("1. Synthetic Market Data Generation")
with st.expander("Explanation: Generating Synthetic Market Data"):
    st.markdown("""
    To accurately simulate the behavior of derivatives, we first need realistic,
    albeit synthetic, market data. This function generates a series of spot prices
    over time, which serve as the underlying asset's price movements. This allows
    us to test different scenarios and observe how various derivative contracts behave
    under changing market conditions, providing a controlled environment for analysis
    without relying on volatile real-world data.

    The formula for the daily spot price movement is:
    $$ S_t = S_{t-1} \\times e^{(\\text{drift} + \\text{random\\_shock})} $$
    where:
    - $S_t$ is the spot price at time $t$.
    - $S_{t-1}$ is the spot price at the previous time step.
    - $\\text{drift} = (\\text{risk\\_free\\_rate} - 0.5 \\times \\text{volatility}^2)$ accounts for the expected return and a term to adjust for volatility.
    - $\\text{random\\_shock} = \\text{np.random.normal}(0, \\text{volatility})$ introduces randomness based on a normal distribution, with volatility determining the magnitude of daily price fluctuations.
    """)

synthetic_data = None
try:
    synthetic_data = generate_synthetic_data(initial_spot, volatility, days_to_maturity, risk_free_rate, contract_size, initial_margin, maintenance_margin)
    st.success("Synthetic data generated successfully!")

    st.subheader("Generated Spot Prices")
    st.line_chart(synthetic_data.set_index('Day'))

    st.header("2. Data Validation and Pre-processing")
    with st.expander("Explanation: Data Validation"):
        st.markdown("""
        Before performing any financial calculations or simulations, it is paramount to ensure the
        integrity and quality of the input data. Incorrect or malformed data can lead to erroneous
        results, flawed conclusions, and potentially significant financial risks.
        This function acts as a gatekeeper, preventing such issues by enforcing data quality standards.
        This is essential for building reliable and trustworthy financial models.
        """)
    validated_data = validate_and_process_data(synthetic_data.copy())
    st.success("Data validated successfully!")

    st.header("3. Summary Statistics")
    with st.expander("Explanation: Logging Summary Statistics"):
        st.markdown("""
        Understanding the fundamental statistical properties of your data is a crucial first step in
        any data analysis or financial modeling task. This function provides a quick, yet comprehensive,
        overview of the numerical columns in the dataset. This helps risk managers and analysts quickly
        identify trends, outliers, or potential data entry errors, ensuring that subsequent complex
        calculations are built on a solid understanding of the underlying data distribution.
        """)
    st.write("Summary statistics for generated data:")
    log_summary_statistics_st(validated_data) # Using a Streamlit-friendly wrapper
except (ValueError, TypeError, Exception) as e:
    st.error(f"Error in data generation or validation: {e}")

if synthetic_data is not None:
    st.header("4. Theoretical Futures Price at Inception")
    with st.expander("Explanation: Calculating Futures Price at Inception"):
        st.markdown("""
        Determining the fair price of a futures contract at the time of its creation
        is essential for market participants. This function calculates this theoretical price,
        providing a benchmark for evaluating actual market prices and identifying potential arbitrage opportunities.
        This is crucial for traders, risk managers, and analysts to assess the value and manage
        the risks associated with futures contracts.

        The formula used is the cost of carry model:
        $$ F_0 = (S_0 - PV_{\\text{Income}} + PV_{\\text{Costs}}) \\times (1 + r)^T $$
        where:
        - $F_0$ is the theoretical futures price at time 0.
        - $S_0$ is the spot price of the underlying asset at time 0.
        - $PV_{\\text{Income}}$ is the present value of any income generated by the underlying asset during the life of the contract.
        - $PV_{\\text{Costs}}$ is the present value of any costs associated with holding the underlying asset during the life of the contract.
        - $r$ is the risk-free rate.
        - $T$ is the time to maturity of the futures contract.
        """)
    initial_futures_price_calc = calculate_futures_price_at_inception(initial_spot, risk_free_rate, days_to_maturity, pv_income, pv_costs)
    st.info(f"The theoretical futures price at inception is: ${initial_futures_price_calc:.2f}")

    st.header("5. Cash Flow and Margin Analysis")
    st.markdown("""
    This section compares the daily cash flow dynamics and margin account fluctuations for different derivative scenarios.
    """)

    scenario_data = None
    if scenario_type == "Exchange-Traded Futures":
        with st.expander("Explanation: Simulating Futures Cash Flows"):
            st.markdown("""
            Understanding the daily cash flow dynamics of a futures contract is critical for managing
            liquidity and assessing the financial risks. This function simulates the daily mark-to-market (MTM)
            process, margin adjustments, and resulting cash flows for a futures contract.

            The formulas are:
            1. Daily PnL: $$ \\text{Daily PnL}_t = (\\text{Futures Price}_t - \\text{Futures Price}_{t-1}) \\times \\text{Contract Size} $$
            2. Margin Balance Update: $$ \\text{Margin Balance}_t = \\text{Margin Balance}_{t-1} + \\text{Daily PnL}_t $$
            3. Cash Flow Determination:
            $$ \\text{If } \\text{Margin Balance}_t < \\text{Maintenance Margin}: \\\\ \\text{Cash Flow}_t = \\text{Initial Margin} - \\text{Margin Balance}_t $$
            The margin balance is then reset to the initial margin. Otherwise, the cash flow is equal to the daily PnL:
            $$ \\text{If } \\text{Margin Balance}_t \\ge \\text{Maintenance Margin}: \\\\ \\text{Cash Flow}_t = \\text{Daily PnL}_t $$
            """)
        scenario_data = simulate_futures_cash_flows(initial_spot, synthetic_data['Spot_Price'].tolist(), contract_size, initial_margin, maintenance_margin)
        st.subheader("Simulated Futures Cash Flows")
        st.dataframe(scenario_data)

        # Plotting cash flow and margin balance
        chart_data = scenario_data[['Day', 'Cash_Flow', 'Margin_Balance']].set_index('Day')
        st.line_chart(chart_data)
        st.caption("Daily Cash Flow and Margin Balance for Futures Contract")

    elif scenario_type == "Non-Centrally Cleared OTC":
        with st.expander("Explanation: Simulating Forward Cash Flows"):
            st.markdown("""
            Unlike futures contracts, forward contracts typically do not involve daily cash flows
            or margin requirements. The cash flow is realized only at the maturity of the contract.
            This function simulates the mark-to-market value of a forward contract and calculates the
            single cash flow that occurs at the contract's expiration.

            The formulas are:
            1. Forward MTM Value: $$ \\text{Forward MTM Value}_t = (\\text{Spot Price}_t - \\text{Initial Forward Price}) \\times \\text{Contract Size} $$
            2. Cash Flow at Maturity: $$ \\text{Cash Flow} = \\text{Forward MTM Value}_{\\text{maturity}} $$
            """)
        scenario_data = simulate_forward_cash_flows(initial_spot, synthetic_data['Spot_Price'].tolist(), contract_size, risk_free_rate)
        st.subheader("Simulated Non-Centrally Cleared OTC (Forward) Cash Flows")
        st.dataframe(scenario_data)

        # Plotting MTM value and cash flow
        chart_data = scenario_data[['Day', 'Forward_MTM_Value', 'Cash_Flow']].set_index('Day')
        st.line_chart(chart_data)
        st.caption("Daily MTM Value and Cash Flow for Non-Centrally Cleared OTC (Forward) Contract")


    elif scenario_type == "Centrally Cleared OTC":
        with st.expander("Explanation: Simulating Centrally Cleared OTC Cash Flows"):
            st.markdown("""
            Central clearing brings OTC derivatives closer to the exchange-traded futures model
            by introducing margining and daily settlement. This reduces counterparty risk and promotes
            market stability. This function simulates the daily mark-to-market process, margin adjustments,
            and resulting cash flows for a centrally cleared OTC contract.

            The formulas are:
            1. Daily PnL: $$ \\text{Daily PnL}_t = (\\text{Spot Price}_t - \\text{OTC Cleared Price}_{t-1}) \\times \\text{Contract Size} $$
            2. Margin Balance Update: $$ \\text{Margin Balance}_t = \\text{Margin Balance}_{t-1} + \\text{Daily PnL}_t $$
            3. Cash Flow Determination:
            $$ \\text{If } \\text{Margin Balance}_t < \\text{Maintenance Margin}: \\\\ \\text{Cash Flow}_t = \\text{Initial Margin} - \\text{Margin Balance}_t $$
            The margin balance is then reset to the initial margin.
            """)
        scenario_data = simulate_centrally_cleared_otc_cash_flows(initial_spot, synthetic_data['Spot_Price'].tolist(), contract_size, initial_margin, maintenance_margin)
        st.subheader("Simulated Centrally Cleared OTC Cash Flows")
        st.dataframe(scenario_data)

        # Plotting cash flow and margin balance
        chart_data = scenario_data[['Day', 'Cash_Flow', 'Margin_Balance']].set_index('Day')
        st.line_chart(chart_data)
        st.caption("Daily Cash Flow and Margin Balance for Centrally Cleared OTC Contract")

    st.header("6. Credit Risk Assessment")
    with st.expander("Explanation: Determining Credit Risk"):
        st.markdown("""
        Central clearing is primarily aimed at mitigating counterparty credit risk in derivatives markets.
        This function provides a simple, qualitative assessment of the credit risk associated with
        different clearing scenarios.
        """)
    # Note: max_unrealized_mtm parameter in determine_credit_risk is not utilized in the provided function logic.
    credit_risk_indicator = determine_credit_risk(scenario_type, max_unrealized_mtm=0) # Passing dummy 0 as it's not used
    st.info(f"Credit Risk for '{scenario_type}': **{credit_risk_indicator}**")

    st.header("7. Price Difference Heatmap")
    with st.expander("Explanation: Calculating Price Difference Heatmap Data"):
        st.markdown("""
        Even with central clearing, various factors can still cause price differences between
        futures and forward contracts, such as correlations between futures prices and interest rates,
        and interest rate volatility. This function is designed to generate data that can be visualized
        as a heatmap. This heatmap allows risk managers and financial analysts to intuitively understand
        how different combinations of correlation and volatility impact these residual price differences.

        **Note:** The current implementation uses dummy price difference data. In a real-world scenario,
        this would be replaced with a sophisticated model to calculate actual price differences.
        """)

    try:
        heatmap_data_df = calculate_price_difference_heatmap_data(correlation_range, volatility_range)
        st.subheader("Simulated Futures vs. Forwards Price Difference Heatmap")

        # Prepare data for Altair
        source = heatmap_data_df.stack().reset_index()
        source.columns = ['Correlation', 'Volatility', 'Price_Difference']

        chart = alt.Chart(source).mark_rect().encode(
            x=alt.X('Volatility:O', axis=alt.Axis(title='Interest Rate Volatility')),
            y=alt.Y('Correlation:O', axis=alt.Axis(title='Interest Rate Correlation')),
            color=alt.Color('Price_Difference:Q', title='Price Difference', scale=alt.Scale(range="heatmap")),
            tooltip=['Correlation:Q', 'Volatility:Q', 'Price_Difference:Q']
        ).properties(
            title='Futures vs. Forwards Price Difference'
        ).interactive()

        st.altair_chart(chart, use_container_width=True)
    except TypeError as e:
        st.error(f"Error generating heatmap data: {e}")

# --- 8. References ---
st.markdown("---")
st.header("References")
st.markdown("""
[1] "REFRESHER READING 2024 CFA® PROGRAM LEVEL 1 Derivatives: Pricing and Valuation of Futures Contracts", CFA Institute, 2023.
This document explains the impact of central clearing on OTC derivatives and how it affects the
differences between futures and forward contracts, including the role of margin requirements.
""")

st.markdown("---")
st.caption("""
© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  
- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@quantuniversity.com](mailto:info@quantuniversity.com)
""")


# --- Function Definitions (to be placed at the top of the Streamlit script) ---
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

def validate_and_process_data(df):
    """Validates and processes the input DataFrame.
    """
    required_columns = ['Day', 'Spot_Price']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' is missing.")

    if not pd.api.types.is_integer_dtype(df['Day']):
        raise TypeError(f"Incorrect data type for 'Day' column. Expected integer, got {df['Day'].dtype}.")

    if df['Day'].duplicated().any():
        raise ValueError("Duplicate values found in 'Day' column.")

    if df['Spot_Price'].isnull().any():
        raise ValueError("Missing values found in 'Spot_Price' column.")

    return df

def log_summary_statistics_st(df):
    """Provide summary statistics for numeric columns (Streamlit friendly)."""
    if df.empty:
        st.write("DataFrame is empty.")
        return

    numeric_columns = df.select_dtypes(include=['number'])

    if numeric_columns.empty:
        st.write("No numeric columns to summarize.")
        return

    for col in numeric_columns:
        st.markdown(f"**Summary statistics for column '{col}':**")
        st.dataframe(df[col].describe())

def calculate_futures_price_at_inception(spot_price, risk_free_rate, time_to_maturity, pv_income, pv_costs):
    """
    Compute the theoretical futures price at t=0 using the cost of carry model.

    Args:
        spot_price (float): Initial spot price of the underlying asset ($S_0$).
        risk_free_rate (float): Risk-free rate ($r$). Note: Ensure this aligns with the time unit of time_to_maturity.
                                If time_to_maturity is in days, risk_free_rate should be daily.
        time_to_maturity (int): Time to maturity of the contract ($T$).
                                Note: This function assumes time_to_maturity is already in the correct unit (e.g., years)
                                or that the risk_free_rate is consistent with `days_to_maturity` being `T`.
                                For consistency with `generate_synthetic_data`'s `days_to_maturity`, we treat `days_to_maturity` as $T$.
        pv_income (float): Present value of any income generated by the underlying asset ($PV_{\text{Income}}$).
        pv_costs (float): Present value of any costs associated with holding the underlying asset ($PV_{\text{Costs}}$).

    Returns:
        float: The theoretical futures price at inception ($F_0$).
    """
    # Assuming risk_free_rate is daily and time_to_maturity is in days for consistency with other functions
    # If risk_free_rate is annual, it should be converted to daily: (1 + annual_rate)^(1/365) - 1
    # Or time_to_maturity should be converted to years: days_to_maturity / 365
    # Sticking to the notebook's example usage where risk_free_rate and time_to_maturity seem to be treated consistently.
    return (spot_price - pv_income + pv_costs) * (1 + risk_free_rate)**time_to_maturity

def simulate_futures_cash_flows(initial_futures_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    """Simulate daily MTM, cash flows, and margin account balances for a futures contract."""

    if not simulated_spot_prices:
        raise Exception("Simulated spot prices cannot be empty.")

    futures_prices = [initial_futures_price] + simulated_spot_prices[:-1]  # Lag spot prices to get previous day's futures price
    daily_pnl = [(simulated_spot_prices[i] - futures_prices[i]) * contract_size for i in range(len(simulated_spot_prices))]

    margin_balance = [0.0] * len(simulated_spot_prices)
    cash_flow = [0.0] * len(simulated_spot_prices)

    margin_balance[0] = initial_margin + daily_pnl[0]
    cash_flow[0] = daily_pnl[0]

    for i in range(1, len(simulated_spot_prices)):
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = daily_pnl[i]

        if margin_balance[i] < maintenance_margin:
            # Margin call: bring balance back to initial margin
            cash_flow[i] += (initial_margin - margin_balance[i])
            margin_balance[i] = initial_margin

    df = pd.DataFrame({
        'Day': range(1, len(simulated_spot_prices) + 1),
        'Futures_Price': simulated_spot_prices,
        'Daily_PnL': daily_pnl,
        'Margin_Balance': margin_balance,
        'Cash_Flow': cash_flow
    })

    return df

def simulate_forward_cash_flows(initial_forward_price, simulated_spot_prices, contract_size, risk_free_rate):
    """Simulate MTM and cash flow for a forward contract."""

    df = pd.DataFrame({'Spot_Price': simulated_spot_prices})
    df['Day'] = range(1, len(df) + 1)
    df['Forward_MTM_Value'] = (df['Spot_Price'] - initial_forward_price) * contract_size
    df['Cash_Flow'] = 0.0
    # Cash flow occurs only at maturity
    df.loc[df.index[-1], 'Cash_Flow'] = df['Forward_MTM_Value'].iloc[-1]

    return df[['Day', 'Forward_MTM_Value', 'Cash_Flow']]

def simulate_centrally_cleared_otc_cash_flows(initial_otc_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    """Simulate daily MTM, cash flows, and margin account balances for a centrally cleared OTC contract."""

    n_days = len(simulated_spot_prices)
    otc_prices = [initial_otc_price] * n_days # This represents the settlement price or previous day's price for PnL calculation
    daily_pnl = [0.0] * n_days
    margin_balance = [0.0] * n_days
    cash_flow = [0.0] * n_days

    # Initial margin and PnL for Day 0 (first day's calculation)
    margin_balance[0] = initial_margin
    daily_pnl[0] = (simulated_spot_prices[0] - initial_otc_price) * contract_size
    margin_balance[0] += daily_pnl[0]

    for i in range(1, n_days):
        # OTC_Cleared_Price represents the previous day's settlement price for PnL
        otc_prices[i] = simulated_spot_prices[i-1] # Or could be fixed initial_otc_price, but previous day's spot aligns with MTM
        daily_pnl[i] = (simulated_spot_prices[i] - otc_prices[i]) * contract_size
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = 0.0  # Initialize cash flow for the day

        if margin_balance[i] < maintenance_margin:
            cash_flow[i] = initial_margin - margin_balance[i]
            margin_balance[i] = initial_margin # Reset to initial margin because of margin call

    df = pd.DataFrame({
        'Day': range(n_days), # Days start from 0 for consistency with the loop
        'OTC_Cleared_Price': otc_prices, # This is effectively previous day's spot for PnL calc.
        'Daily_PnL': daily_pnl,
        'Margin_Balance': margin_balance,
        'Cash_Flow': cash_flow
    })
    # Adjust 'Day' to start from 1 if preferred for display
    df['Day'] = df['Day'] + 1

    return df

def determine_credit_risk(scenario_type, max_unrealized_mtm):
    """
    Provide a qualitative credit risk indicator based on the scenario.
    Note: max_unrealized_mtm parameter is not utilized in the provided function logic.
    """
    if scenario_type == "Non-Centrally Cleared OTC":
        return "High"
    elif scenario_type == "Centrally Cleared OTC":
        return "Low"
    elif scenario_type == "Exchange-Traded Futures":
        return "Low"
    else:
        raise Exception("Invalid scenario type")

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
    # The original notebook uses np.random.rand, which produces values between 0 and 1.
    # To make it more "difference-like" and potentially negative, we can adjust it.
    price_difference_data = (np.random.rand(num_points, num_points) - 0.5) * 10 # Scale and shift for more meaningful "difference"

    # Create a Pandas DataFrame for the heatmap
    # Rounding index and columns for cleaner display in Streamlit chart tooltips
    df = pd.DataFrame(price_difference_data,
                      index=np.round(correlation_values, 2),
                      columns=np.round(volatility_values, 3))

    return df
```
