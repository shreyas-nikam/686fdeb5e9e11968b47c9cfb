
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def run_page1():
    st.header("Introduction & Spot Price")
    st.markdown("""
    This page focuses on generating synthetic market data and visualizing the simulated spot price trend. Understanding the underlying data generation process is crucial for analyzing the impact of central clearing.
    """)

    # --- 1. Generating Synthetic Market Data ---
    st.sidebar.markdown("### Market Data Simulation")
    st.sidebar.markdown(r"""
    The daily spot price movement is modeled by:
    $$ S_t = S_{t-1} 	imes e^{(	ext{drift} + 	ext{random\_shock})} $$
    where:
    - $S_t$ is the spot price at time $t$.
    - $S_{t-1}$ is the spot price at the previous time step.
    - $	ext{drift} = (	ext{risk\_free\_rate} - 0.5 	imes 	ext{volatility}^2)$
    - $	ext{random\_shock} = 	ext{np.random.normal}(0, 	ext{volatility})$
    """)

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

    def log_summary_statistics(df):
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
            st.dataframe(df[col].describe())
        st.markdown("---")
    
    # Input widgets (using st.session_state to persist values across page changes)
    if 'initial_spot' not in st.session_state:
        st.session_state['initial_spot'] = 100.0
    if 'volatility' not in st.session_state:
        st.session_state['volatility'] = 0.01
    if 'days_to_maturity' not in st.session_state:
        st.session_state['days_to_maturity'] = 20
    if 'risk_free_rate' not in st.session_state:
        st.session_state['risk_free_rate'] = 0.0001
    if 'contract_size' not in st.session_state:
        st.session_state['contract_size'] = 100
    if 'initial_margin' not in st.session_state:
        st.session_state['initial_margin'] = 1000
    if 'maintenance_margin' not in st.session_state:
        st.session_state['maintenance_margin'] = 800

    initial_spot = st.sidebar.number_input("Initial Spot Price ($S_0$)", value=st.session_state['initial_spot'], min_value=1.0, help="Initial price of the underlying asset.", key='initial_spot_input')
    volatility = st.sidebar.slider("Daily Volatility", value=st.session_state['volatility'], min_value=0.001, max_value=0.05, step=0.001, format="%.3f", help="Magnitude of daily price fluctuations (standard deviation).", key='volatility_input')
    days_to_maturity = st.sidebar.number_input("Days to Maturity ($T$)", value=st.session_state['days_to_maturity'], min_value=1, help="Number of days for the simulation period.", key='days_to_maturity_input')
    risk_free_rate = st.sidebar.number_input("Daily Risk-Free Rate ($r$)", value=st.session_state['risk_free_rate'], min_value=0.00001, max_value=0.001, step=0.00001, format="%.5f", help="Daily risk-free interest rate for compounding.", key='risk_free_rate_input')
    contract_size = st.sidebar.number_input("Contract Size", value=st.session_state['contract_size'], min_value=1, help="Number of units of the underlying asset per contract.", key='contract_size_input')
    initial_margin = st.sidebar.number_input("Initial Margin", value=st.session_state['initial_margin'], min_value=100, help="Initial amount of collateral required to open a position.", key='initial_margin_input')
    maintenance_margin = st.sidebar.number_input("Maintenance Margin", value=st.session_state['maintenance_margin'], min_value=50, help="Minimum margin balance to be maintained; triggers a margin call if breached.", key='maintenance_margin_input')


    # Generate synthetic data
    try:
        synthetic_data = generate_synthetic_data(initial_spot, volatility, days_to_maturity, risk_free_rate, contract_size, initial_margin, maintenance_margin)

        # Validate data
        validated_data = validate_and_process_data(synthetic_data.copy())

        # Display spot price trend
        st.subheader("Simulated Spot Price Trend")
        fig_spot = px.line(validated_data, x='Day', y='Spot_Price', title='Simulated Spot Price Over Time')
        fig_spot.update_layout(yaxis_title="Spot Price ($)", xaxis_title="Day", font_size=12)
        st.plotly_chart(fig_spot, use_container_width=True)

        # Log summary statistics
        log_summary_statistics(validated_data)

    except (ValueError, TypeError) as e:
        st.error(f"An error occurred: {e}. Please check your inputs.")

if __name__ == "__main__":
    run_page1()
