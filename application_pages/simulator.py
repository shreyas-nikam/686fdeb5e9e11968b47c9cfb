
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def run_simulator():
    st.header("Central Clearing Impact Simulator")
    st.write("Explore the impact of central clearing on the differences between exchange-traded derivatives (ETDs) like futures and over-the-counter (OTC) derivatives like forwards.")

    with st.sidebar:
        st.header("Simulation Parameters")
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
                raise ValueError(f"Required column '{{col}}' is missing.")
        if not pd.api.types.is_integer_dtype(df['Day']):
            raise TypeError(f"Incorrect data type for 'Day' column. Expected int64, got {{df['Day'].dtype}}.")
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
            st.write(f"**Column: '{{col}}'**")
            st.dataframe(df[col].describe())
        st.markdown("---")

    @st.cache_data
    def calculate_futures_price_at_inception(spot_price, risk_free_rate, time_to_maturity, pv_income, pv_costs):
        return (spot_price - pv_income + pv_costs) * (1 + risk_free_rate)**time_to_maturity

    @st.cache_data
    def simulate_futures_cash_flows(initial_futures_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
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

    @st.cache_data
    def simulate_forward_cash_flows(initial_forward_price, simulated_spot_prices, contract_size, risk_free_rate):
        df = pd.DataFrame({'Spot_Price': simulated_spot_prices})
        df['Day'] = range(1, len(df) + 1)
        df['Forward_MTM_Value'] = (df['Spot_Price'] - initial_forward_price) * contract_size
        df['Cash_Flow'] = 0.0
        df.loc[df.index[-1], 'Cash_Flow'] = df['Forward_MTM_Value'].iloc[-1]
        return df[['Day', 'Forward_MTM_Value', 'Cash_Flow']]

    @st.cache_data
    def simulate_centrally_cleared_otc_cash_flows(initial_otc_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
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
            cash_flow[i] = 0.0

            if margin_balance[i] < maintenance_margin:
                cash_flow[i] = initial_margin - margin_balance[i]
                margin_balance[i] = initial_margin

        df = pd.DataFrame({
            'Day': range(n_days),
            'OTC_Cleared_Price': simulated_spot_prices,
            'Daily_PnL': daily_pnl,
            'Margin_Balance': margin_balance,
            'Cash_Flow': cash_flow
        })
        return df

    def determine_credit_risk(scenario_type):
        if scenario_type == "Non-Centrally Cleared OTC":
            return "High"
        elif scenario_type == "Centrally Cleared OTC":
            return "Low"
        elif scenario_type == "Exchange-Traded Futures":
            return "Low"
        else:
            return "N/A"

    @st.cache_data
    def calculate_price_difference_heatmap_data(correlation_range, volatility_range):
        if not (isinstance(correlation_range, tuple) and isinstance(volatility_range, tuple)):
            raise TypeError("Ranges must be tuples.")

        correlation_start, correlation_end = correlation_range
        volatility_start, volatility_end = volatility_range

        num_points = 10
        correlation_values = np.linspace(min(correlation_start, correlation_end), max(correlation_start, correlation_end), num_points)
        volatility_values = np.linspace(min(volatility_start, volatility_end), max(volatility_start, volatility_end), num_points)

        price_difference_data = np.random.rand(num_points, num_points)

        df = pd.DataFrame(price_difference_data, index=correlation_values.round(2), columns=volatility_values.round(3))
        df.index.name = "Interest Rate Correlation"
        df.columns.name = "Interest Rate Volatility"
        return df

    try:
        synthetic_data = generate_synthetic_data(initial_spot, volatility, days_to_maturity, risk_free_rate, contract_size, initial_margin, maintenance_margin)
        validated_data = validate_and_process_data(synthetic_data.copy())

        st.subheader("1. Simulated Spot Price Trend")
        fig_spot = px.line(validated_data, x='Day', y='Spot_Price', title='Simulated Spot Price Over Time')
        fig_spot.update_layout(yaxis_title="Spot Price ($)", xaxis_title="Day", font_size=12)
        st.plotly_chart(fig_spot, use_container_width=True)

        log_summary_statistics(validated_data)

        st.subheader("2. Theoretical Futures Price at Inception")
        pv_income_futures = st.number_input("Present Value of Income ($PV_{\text{Income}}$) for Futures Pricing", value=0.0, help="Present value of any income generated by the underlying asset.")
        pv_costs_futures = st.number_input("Present Value of Costs ($PV_{\text{Costs}}$) for Futures Pricing", value=0.0, help="Present value of any costs associated with holding the underlying asset.")
        futures_price_inception = calculate_futures_price_at_inception(initial_spot, risk_free_rate, days_to_maturity, pv_income_futures, pv_costs_futures)
        st.metric("Calculated Futures Price at Inception ($F_0$)", f"${futures_price_inception:,.2f}")
        st.markdown("---")

        st.subheader(f"3. Simulation Results for: {scenario_type}")

        df_results = None
        if scenario_type == "Non-Centrally Cleared OTC":
            df_results = simulate_forward_cash_flows(initial_spot, validated_data['Spot_Price'].tolist(), contract_size, risk_free_rate)
            df_results = df_results.rename(columns={'Forward_MTM_Value': 'MTM_Value'})
        elif scenario_type == "Centrally Cleared OTC":
            df_results = simulate_centrally_cleared_otc_cash_flows(initial_spot, validated_data['Spot_Price'].tolist(), contract_size, initial_margin, maintenance_margin)
            df_results = df_results.rename(columns={'OTC_Cleared_Price': 'Futures_Price'})
        elif scenario_type == "Exchange-Traded Futures":
            df_results = simulate_futures_cash_flows(initial_spot, validated_data['Spot_Price'].tolist(), contract_size, initial_margin, maintenance_margin)

        if df_results is not None:
            st.dataframe(df_results.head())

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

            st.subheader("Credit Risk Assessment")
            credit_risk = determine_credit_risk(scenario_type)
            st.metric("Credit Risk Exposure", credit_risk)
            st.markdown("---")

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
