
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px # Added for consistency, though go is used more for cash flow

# Redefine functions or import them if shared. For simplicity and self-containment per page,
# I'll redefine them here if they are directly used for calculations on this page.
# In a real app, common utilities would be in a separate 'utils.py'.
@st.cache_data
def generate_synthetic_data(initial_spot, volatility, days_to_maturity, risk_free_rate, contract_size, initial_margin, maintenance_margin):
    spot_prices = [initial_spot]
    for i in range(1, days_to_maturity + 1):
        drift = (risk_free_rate - 0.5 * volatility**2)
        random_shock = np.random.normal(0, volatility)
        spot_price = spot_prices[-1] * np.exp(drift + random_shock)
        spot_prices.append(spot_price)
    df = pd.DataFrame({'Day': range(days_to_maturity + 1), 'Spot_Price': spot_prices[:-1]})
    return df

@st.cache_data
def validate_and_process_data(df):
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

@st.cache_data
def calculate_futures_price_at_inception(spot_price, risk_free_rate, time_to_maturity, pv_income, pv_costs):
    return (spot_price - pv_income + pv_costs) * (1 + risk_free_rate)**time_to_maturity

@st.cache_data
def simulate_futures_cash_flows(initial_futures_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    if not simulated_spot_prices:
        raise Exception("Simulated spot prices cannot be empty.")

    # Using initial_futures_price for the first PnL calculation, then current spot.
    # The original notebook's futures_prices list setup was a bit ambiguous for the very first PnL.
    # Let's align with typical MTM where price is compared to previous day's settlement or inception.
    # For simplicity, we assume futures price tracks spot price for MTM for simulation.
    # The initial_futures_price is for the very first step.
    
    daily_pnl = [0.0] * len(simulated_spot_prices) # Initialize PnL
    margin_balance = [0.0] * len(simulated_spot_prices)
    cash_flow = [0.0] * len(simulated_spot_prices)

    # Day 0: Initial setup and first PnL
    # futures_prices are basically the simulated_spot_prices as a proxy for fair value in this simulation
    # The 'futures_prices' in the original notebook's simulate_futures_cash_flows appears to be the current day's spot
    # for the Futures_Price column, and the 'otc_prices' for centrally cleared also uses current day's spot for 'OTC_Cleared_Price'.
    # I will adapt the PnL logic to consistently use (current spot - previous day's spot) for MTM for simplicity of the simulation.
    # The initial_futures_price is mostly used for the initial theoretical value display.

    # Assuming Daily_PnL is (Spot_t - Spot_t-1) * Contract_Size
    # The original notebook code: daily_pnl = [(simulated_spot_prices[i] - futures_prices[i]) * contract_size for i in range(len(simulated_spot_prices))]
    # where futures_prices = [initial_futures_price] + simulated_spot_prices[:-1]
    # This means for day 0 (index 0 of daily_pnl), it's (simulated_spot_prices[0] - initial_futures_price) * contract_size
    # For day i (index i of daily_pnl), it's (simulated_spot_prices[i] - simulated_spot_prices[i-1]) * contract_size
    
    # Recalculate daily_pnl based on current spot minus previous day's spot (for futures-like MTM)
    daily_pnl = [(simulated_spot_prices[i] - (initial_futures_price if i == 0 else simulated_spot_prices[i-1])) * contract_size for i in range(len(simulated_spot_prices))]

    margin_balance[0] = initial_margin + daily_pnl[0]
    cash_flow[0] = 0.0 # Initial cash flow unless margin call on day 0
    if margin_balance[0] < maintenance_margin:
        cash_flow[0] = initial_margin - margin_balance[0]
        margin_balance[0] = initial_margin

    for i in range(1, len(simulated_spot_prices)):
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = daily_pnl[i] # Daily PnL is initially the cash flow

        if margin_balance[i] < maintenance_margin:
            # Margin call occurs
            cash_flow[i] = initial_margin - margin_balance[i]
            margin_balance[i] = initial_margin # Restore margin to initial level

    df = pd.DataFrame({
        'Day': range(len(simulated_spot_prices)), # Day 0 to Day N-1
        'Futures_Price_Track': simulated_spot_prices, # For plotting
        'Daily_PnL': daily_pnl,
        'Margin_Balance': margin_balance,
        'Cash_Flow': cash_flow
    })
    return df

@st.cache_data
def simulate_forward_cash_flows(initial_forward_price, simulated_spot_prices, contract_size, risk_free_rate):
    df = pd.DataFrame({'Spot_Price': simulated_spot_prices})
    df['Day'] = range(len(df)) # Day 0 to N-1
    # Forwards are typically not marked to market daily, only settled at maturity.
    # The 'Forward_MTM_Value' might represent the theoretical value of the forward position.
    df['Forward_MTM_Value'] = (df['Spot_Price'] - initial_forward_price) * contract_size
    df['Cash_Flow'] = 0.0
    # The only cash flow is at maturity
    df.loc[df.index[-1], 'Cash_Flow'] = df['Forward_MTM_Value'].iloc[-1]
    return df[['Day', 'Forward_MTM_Value', 'Cash_Flow']]

@st.cache_data
def simulate_centrally_cleared_otc_cash_flows(initial_otc_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    n_days = len(simulated_spot_prices)
    
    # Similar to futures, assuming daily MTM against spot price changes
    # otc_prices = [initial_otc_price] + simulated_spot_prices[:-1] # This line was in the notebook
    # Re-aligning PnL calculation to be consistent with futures simulation for daily change
    daily_pnl = [(simulated_spot_prices[i] - (initial_otc_price if i == 0 else simulated_spot_prices[i-1])) * contract_size for i in range(n_days)]

    margin_balance = [0.0] * n_days
    cash_flow = [0.0] * n_days

    margin_balance[0] = initial_margin + daily_pnl[0]
    cash_flow[0] = 0.0
    if margin_balance[0] < maintenance_margin:
        cash_flow[0] = initial_margin - margin_balance[0]
        margin_balance[0] = initial_margin

    for i in range(1, n_days):
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = daily_pnl[i]

        if margin_balance[i] < maintenance_margin:
            cash_flow[i] = initial_margin - margin_balance[i]
            margin_balance[i] = initial_margin

    df = pd.DataFrame({
        'Day': range(n_days),
        'OTC_Cleared_Price_Track': simulated_spot_prices, # For plotting
        'Daily_PnL': daily_pnl,
        'Margin_Balance': margin_balance,
        'Cash_Flow': cash_flow
    })
    return df

def run_page2():
    st.header("Cash Flow Simulation")
    st.markdown("""
    This section allows you to simulate the cash flow dynamics of different derivative contracts: Non-Centrally Cleared OTC (Forwards), Centrally Cleared OTC, and Exchange-Traded Futures. Observe how daily mark-to-market and margin requirements impact cash flows over time.
    """)

    # Retrieve parameters from session state
    initial_spot = st.session_state.get('initial_spot', 100.0)
    volatility = st.session_state.get('volatility', 0.01)
    days_to_maturity = st.session_state.get('days_to_maturity', 20)
    risk_free_rate = st.session_state.get('risk_free_rate', 0.0001)
    contract_size = st.session_state.get('contract_size', 100)
    initial_margin = st.session_state.get('initial_margin', 1000)
    maintenance_margin = st.session_state.get('maintenance_margin', 800)

    st.subheader("Theoretical Futures Price at Inception")
    st.sidebar.markdown("### Futures Price at Inception")
    st.sidebar.markdown(r"""
    The theoretical futures price at time $0$ is:
    $$ F_0 = (S_0 - PV_{\text{Income}} + PV_{\text{Costs}}) \times (1 + r)^T $$
    """)
    pv_income_futures = st.number_input("Present Value of Income ($PV_{\text{Income}}$) for Futures Pricing", value=0.0, help="Present value of any income generated by the underlying asset.", key='pv_income_futures')
    pv_costs_futures = st.number_input("Present Value of Costs ($PV_{\text{Costs}}$) for Futures Pricing", value=0.0, help="Present value of any costs associated with holding the underlying asset.", key='pv_costs_futures')
    
    futures_price_inception = calculate_futures_price_at_inception(initial_spot, risk_free_rate, days_to_maturity / 365.0, pv_income_futures, pv_costs_futures) # Assuming T is in years for formula
    st.metric("Calculated Futures Price at Inception ($F_0$)", f"${futures_price_inception:,.2f}")
    st.markdown("---")

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
    \text{If } \text{Margin Balance}_t \geq \text{Maintenance Margin}: \\
    \text{Cash Flow}_t = \text{Daily PnL}_t
    $$
    """)

    st.sidebar.markdown("### Forward Cash Flow Formulas")
    st.sidebar.markdown(r"""
    Forward MTM Value:
    $$ \text{Forward MTM Value}_t = (\text{Spot Price}_t - \text{Initial Forward Price}) \times \text{Contract Size} $$
    Cash Flow at Maturity:
    $$ \text{Cash Flow} = \text{Forward MTM Value}_{\text{maturity}} $$
    """)

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


    scenario_type = st.radio(
        "Choose Derivative Type for Simulation:",
        ("Non-Centrally Cleared OTC", "Centrally Cleared OTC", "Exchange-Traded Futures"),
        help="Select the type of derivative contract to simulate and compare.",
        key='scenario_type_selection'
    )
    st.markdown("---")

    try:
        # Generate synthetic data
        synthetic_data = generate_synthetic_data(initial_spot, volatility, days_to_maturity, risk_free_rate, contract_size, initial_margin, maintenance_margin)
        validated_data = validate_and_process_data(synthetic_data.copy())
        simulated_spot_prices = validated_data['Spot_Price'].tolist()

        df_results = None
        if scenario_type == "Non-Centrally Cleared OTC":
            df_results = simulate_forward_cash_flows(initial_spot, simulated_spot_prices, contract_size, risk_free_rate)
            df_results = df_results.rename(columns={'Forward_MTM_Value': 'MTM_Value'}) # Consistent column name for plotting
        elif scenario_type == "Centrally Cleared OTC":
            df_results = simulate_centrally_cleared_otc_cash_flows(initial_spot, simulated_spot_prices, contract_size, initial_margin, maintenance_margin)
            df_results = df_results.rename(columns={'OTC_Cleared_Price_Track': 'Spot_Price_Proxy'}) # Consistent column name for plotting
        elif scenario_type == "Exchange-Traded Futures":
            df_results = simulate_futures_cash_flows(initial_spot, simulated_spot_prices, contract_size, initial_margin, maintenance_margin)
            df_results = df_results.rename(columns={'Futures_Price_Track': 'Spot_Price_Proxy'}) # Consistent column name for plotting

        if df_results is not None:
            st.subheader(f"Simulation Results for: {scenario_type}")
            st.dataframe(df_results.head())

            st.subheader("Daily Cash Flows and Margin Account Fluctuations")
            fig_cash_flow = go.Figure()
            
            fig_cash_flow.add_trace(go.Scatter(x=df_results['Day'], y=df_results['Cash_Flow'], mode='lines', name='Cash Flow'))
            if 'Daily_PnL' in df_results.columns: # Applicable for Futures and Cleared OTC
                fig_cash_flow.add_trace(go.Scatter(x=df_results['Day'], y=df_results['Daily_PnL'], mode='lines', name='Daily PnL'))
            if 'Margin_Balance' in df_results.columns: # Applicable for Futures and Cleared OTC
                fig_cash_flow.add_trace(go.Scatter(x=df_results['Day'], y=df_results['Margin_Balance'], mode='lines', name='Margin Balance'))
            if 'MTM_Value' in df_results.columns: # Applicable for Non-Centrally Cleared OTC (Forward)
                fig_cash_flow.add_trace(go.Scatter(x=df_results['Day'], y=df_results['MTM_Value'], mode='lines', name='MTM Value (Forward)'))

            fig_cash_flow.update_layout(
                title='Cash Flow & Margin Visualization',
                xaxis_title='Day',
                yaxis_title='Value ($)',
                hovermode='x unified',
                font=dict(size=12)
            )
            st.plotly_chart(fig_cash_flow, use_container_width=True)

    except (ValueError, TypeError, Exception) as e:
        st.error(f"An error occurred: {e}. Please ensure correct inputs and that simulation data is generated. If you navigated directly to this page, go to 'Introduction & Spot Price' first to initialize parameters.")

if __name__ == "__main__":
    run_page2()
