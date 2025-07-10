id: 686fdeb5e9e11968b47c9cfb_documentation
summary: Pricing and Valuation of Futures Contracts Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Exploring Central Clearing: Futures vs. Forwards with Streamlit

## Introduction to QuLab and Central Clearing
Duration: 0:05

Welcome to QuLab, a practical laboratory for understanding complex financial concepts. In this codelab, we will explore a Streamlit application designed to demystify the impact of central clearing on derivative contracts. This application focuses on comparing Exchange-Traded Derivatives (ETDs) like futures with Over-The-Counter (OTC) derivatives like forwards.

For developers and finance professionals, understanding central clearing is crucial. It directly impacts counterparty risk, market liquidity, and the pricing of derivatives. The core concepts you'll learn and reinforce through this application include:

*   **Exchange-Traded Derivatives (ETDs) vs. Over-The-Counter (OTC) Derivatives:** Their structural differences and how they are traded.
*   **Central Counterparty (CCP):** The role of a CCP in mitigating counterparty risk by becoming the buyer to every seller and seller to every buyer.
*   **Margin Requirements:** How initial and maintenance margins are used to manage risk in cleared transactions.
*   **Daily Settlement (Mark-to-Market):** The process of daily cash flows to reflect changes in contract value, a hallmark of futures and centrally cleared contracts.
*   **Futures vs. Forwards Pricing:** The theoretical and practical reasons for price differences between these contract types, especially considering daily settlement and interest rate effects.

The application provides a hands-on simulator to visualize these concepts, making abstract financial theories tangible. By the end of this codelab, you will have a comprehensive understanding of the application's functionalities and the underlying financial principles.

## Setting up the Development Environment
Duration: 0:10

To get started, you'll need Python installed on your system. We recommend Python 3.8 or newer.

1.  **Create your project directory:**
    ```bash
    mkdir qulab_derivatives
    cd qulab_derivatives
    mkdir application_pages
    ```

2.  **Create the `app.py` file:**
    Inside the `qulab_derivatives` directory, create a file named `app.py` and paste the following content:

    ```python
    import streamlit as st
    st.set_page_config(page_title="QuLab", layout="wide")
    st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
    st.sidebar.divider()
    st.title("QuLab")
    st.divider()
    st.markdown("""
    In this lab, we explore the impact of central clearing on the pricing and valuation of futures contracts.
    We will compare and contrast Exchange-Traded Derivatives (ETDs) like futures with Over-The-Counter (OTC) derivatives like forwards.
    The application aims to provide a practical tool for risk managers, compliance officers, and institutional finance students to understand how margin requirements and daily settlement reduce cash flow and price differences between these contract types.
    """)
    # Your code starts here
    page = st.sidebar.selectbox(label="Navigation", options=["Introduction", "Simulator", "References"])
    if page == "Introduction":
        from application_pages.introduction import run_introduction
        run_introduction()
    elif page == "Simulator":
        from application_pages.simulator import run_simulator
        run_simulator()
    elif page == "References":
        from application_pages.references import run_references
        run_references()
    # Your code ends
    ```

3.  **Create `application_pages/introduction.py`:**
    Inside the `application_pages` directory, create `introduction.py` and paste:

    ```python
    import streamlit as st

    def run_introduction():
        st.header("Introduction to Central Clearing")
        st.markdown("""
        This application simulates the impact of central clearing on derivative contracts.
        Central clearing is a process where a central counterparty (CCP) interposes itself between two parties in a derivative transaction, becoming the buyer to every seller and the seller to every buyer. This reduces counterparty risk and increases market transparency.

        **Key Benefits of Central Clearing:**
        - Reduced Counterparty Risk: The CCP guarantees the performance of the contract, reducing the risk that one party will default.
        - Increased Transparency: Central clearing provides regulators with a clear view of market activity, helping them to identify and manage systemic risk.
        - Standardized Processes: Central clearing standardizes many aspects of derivative trading, such as margining and settlement.

        **In this lab, we will explore:**
        - The differences between Exchange-Traded Derivatives (ETDs) and Over-The-Counter (OTC) derivatives.
        - How margin requirements and daily settlement impact cash flows for different types of derivatives.
        - The role of central clearing in mitigating credit risk.
        - Factors that contribute to price differences between futures and forwards, even with central clearing.
        """)
    ```

4.  **Create `application_pages/simulator.py`:**
    Inside the `application_pages` directory, create `simulator.py` and paste:

    ```python
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

            st.markdown("")
            st.header("Scenario Selection")
            scenario_type = st.radio(
                "Choose Derivative Type:",
                ("Non-Centrally Cleared OTC", "Centrally Cleared OTC", "Exchange-Traded Futures"),
                help="Select the type of derivative contract to simulate and compare."
            )
            st.markdown("")
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
            st.markdown("")

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
            pv_income_futures = st.number_input("Present Value of Income ($PV_{\\text{Income}}$) for Futures Pricing", value=0.0, help="Present value of any income generated by the underlying asset.")
            pv_costs_futures = st.number_input("Present Value of Costs ($PV_{\\text{Costs}}$) for Futures Pricing", value=0.0, help="Present value of any costs associated with holding the underlying asset.")
            futures_price_inception = calculate_futures_price_at_inception(initial_spot, risk_free_rate, days_to_maturity, pv_income_futures, pv_costs_futures)
            st.metric("Calculated Futures Price at Inception ($F_0$)", f"${futures_price_inception:,.2f}")
            st.markdown("")

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
                st.markdown("")

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
    ```

5.  **Create `application_pages/references.py`:**
    Inside the `application_pages` directory, create `references.py` and paste:

    ```python
    import streamlit as st

    def run_references():
        st.header("References")
        st.markdown("""
        [1] "REFRESHER READING 2024 CFA® PROGRAM LEVEL 1 Derivatives: Pricing and Valuation of Futures Contracts", CFA Institute, 2023. This document explains the impact of central clearing on OTC derivatives and how it affects the differences between futures and forward contracts, including the role of margin requirements.
        """)
        st.markdown("")
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

6.  **Install dependencies:**
    Open your terminal in the `qulab_derivatives` directory and install the required libraries:
    ```bash
    pip install streamlit pandas numpy plotly
    ```

7.  **Run the application:**
    From the `qulab_derivatives` directory, execute the Streamlit command:
    ```bash
    streamlit run app.py
    ```
    This will open the application in your web browser.

## Understanding the Application Structure
Duration: 0:10

The application is structured modularly using Streamlit's multi-page pattern, albeit in a simplified form. This design promotes code organization and readability.

Here's an overview of the file structure and their responsibilities:

```
qulab_derivatives/
├── app.py
└── application_pages/
    ├── introduction.py
    ├── simulator.py
    └── references.py
```

*   **`app.py`**: This is the main entry point of the Streamlit application.
    *   It sets up the basic Streamlit page configuration, including the title and sidebar image.
    *   It renders the main title and an introductory markdown description visible on all pages.
    *   Crucially, it uses a `st.sidebar.selectbox` to enable navigation between different "pages" (modules). Based on the user's selection, it dynamically imports and calls the `run_` function from the respective script in `application_pages/`.

*   **`application_pages/introduction.py`**:
    *   Contains the `run_introduction()` function.
    *   This module provides an overview of central clearing, its benefits, and the key concepts explored within the application. It serves as a foundational context for users.

*   **`application_pages/simulator.py`**:
    *   Contains the `run_simulator()` function, which is the heart of this application.
    *   It hosts all the simulation logic, user input controls (in the sidebar), data generation, calculation functions, and visualization components.
    *   This is where the user interacts with the models to explore the impact of central clearing.

*   **`application_pages/references.py`**:
    *   Contains the `run_references()` function.
    *   This module lists academic or industry references that support the concepts discussed in the application.
    *   It also includes the licensing information for the QuLab application.

This modular setup allows for easy expansion with more features or pages without cluttering the main `app.py` file.

```mermaid
graph TD
    A[app.py: Main Application] --> B[Sidebar Navigation];
    B -- Select "Introduction" --> C[introduction.py: run_introduction()];
    B -- Select "Simulator" --> D[simulator.py: run_simulator()];
    B -- Select "References" --> E[references.py: run_references()];

    D -- User Inputs --> F[Simulation Parameters];
    D -- User Chooses --> G[Derivative Scenario];
    D -- Backend Logic --> H[Generate Synthetic Spot Prices];
    H --> I[Calculate Futures Price at Inception];
    I --> J[Simulate Cash Flows based on Scenario];
    J --> K[Determine Credit Risk];
    K --> L[Generate Price Difference Heatmap];
    H,I,J,K,L --> M[Display Results & Visualizations];
```

## Deep Dive into the Simulator - Core Concepts & Parameters
Duration: 0:15

Navigate to the "Simulator" page in the Streamlit application. This section is where you can interact with the core logic and parameters that drive the derivatives simulation.

The `application_pages/simulator.py` script houses the `run_simulator()` function, which sets up the user interface and orchestrates the simulation.

### Simulation Parameters (Sidebar)

The left sidebar provides interactive controls to adjust the simulation environment:

*   **Initial Spot Price ($S_0$)**: The starting price of the underlying asset (e.g., a stock, commodity). This is the base value from which all price movements and derivative valuations begin.
    *   Code: `st.number_input("Initial Spot Price ($S_0$)", value=100.0)`
*   **Days to Maturity ($T$)**: The total number of days over which the simulation will run, representing the life of the derivative contract.
    *   Code: `st.number_input("Days to Maturity ($T$)", value=20)`
*   **Daily Volatility ($\sigma$)**: A measure of the expected daily fluctuations in the underlying asset's price. Higher volatility implies greater price swings. This is used in the Geometric Brownian Motion model for spot price generation.
    *   Code: `st.slider("Daily Volatility", value=0.01)`
*   **Daily Risk-Free Rate ($r$)**: The theoretical rate of return of an investment with zero risk. Used for discounting and compounding in derivative pricing.
    *   Code: `st.number_input("Daily Risk-Free Rate ($r$)", value=0.0001)`
*   **Contract Size**: The number of units of the underlying asset represented by one derivative contract. For example, if a contract size is 100, then a $1 price change results in a $100 PnL for the contract.
    *   Code: `st.number_input("Contract Size", value=100)`
*   **Initial Margin**: The upfront collateral required by the clearinghouse (or counterparty in OTC) to enter into a futures or centrally cleared OTC contract. It acts as a performance bond.
    *   Code: `st.number_input("Initial Margin", value=1000)`
*   **Maintenance Margin**: The minimum amount of margin that must be maintained in a margin account. If the margin balance falls below this level, a margin call is triggered, requiring the trader to deposit additional funds to bring the balance back up to the initial margin level.
    *   Code: `st.number_input("Maintenance Margin", value=800)`

<aside class="positive">
<b>Experimentation Tip:</b> Change these parameters and observe their impact on the simulated spot prices, cash flows, and margin account behavior. For instance, increasing volatility will lead to more erratic spot price movements and larger daily PnL swings, potentially triggering more margin calls.
</aside>

### Scenario Selection (Sidebar)

This crucial radio button allows you to choose the type of derivative contract to simulate:

*   **Non-Centrally Cleared OTC**: Represents a traditional Over-The-Counter forward contract, where settlement typically occurs only at maturity, and there's direct counterparty exposure.
*   **Centrally Cleared OTC**: Represents an OTC contract that is submitted to a CCP for clearing. This introduces daily mark-to-market and margining, similar to exchange-traded futures.
*   **Exchange-Traded Futures**: Represents a standard futures contract traded on an exchange, which is inherently centrally cleared with daily mark-to-market and margin requirements.

By comparing the cash flow patterns and credit risk assessment across these scenarios, you can visually grasp the impact of central clearing.

### Heatmap Parameters (Sidebar)

These sliders control the range for the dummy data used in the "Residual Price Differences" heatmap. While the current heatmap data is random, these parameters highlight that in a real-world scenario, factors like interest rate correlation and volatility would drive the differences between futures and forward prices even under central clearing.

*   **Min Correlation / Max Correlation**: Range for interest rate correlation on the heatmap axis.
*   **Min Volatility / Max Volatility (Heatmap)**: Range for interest rate volatility on the heatmap axis.

## Simulating Spot Prices and Futures Pricing at Inception
Duration: 0:15

The simulator begins by generating a plausible path for the underlying asset's spot price and then calculates the theoretical futures price at inception.

### 1. Simulated Spot Price Trend

The `generate_synthetic_data` function simulates the daily spot price path of the underlying asset. It uses a simplified form of Geometric Brownian Motion, which is commonly used to model asset prices in financial mathematics.

The formula for the daily price movement is:
$$S_t = S_{t-1} \cdot e^{(\mu - \frac{1}{2}\sigma^2) \Delta t + \sigma \sqrt{\Delta t} Z_t}$$
Where:
*   $S_t$: Spot price at time $t$
*   $S_{t-1}$: Spot price at previous time step ($t-1$)
*   $\mu$: Drift rate (approximated by `risk_free_rate` in this simplified model)
*   $\sigma$: Volatility (`volatility`)
*   $\Delta t$: Time step (daily, so $\Delta t = 1$)
*   $Z_t$: A random sample from a standard normal distribution (a random shock)

In the code, the drift term is `(risk_free_rate - 0.5 * volatility**2)` and `random_shock` represents $\sigma Z_t$. The simulation generates prices for `days_to_maturity` + 1 days (from Day 0 to Day $T$).

```python
# From application_pages/simulator.py
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
```

<aside class="positive">
<b>Code Efficiency:</b> The `@st.cache_data` decorator is used here to memoize the results of `generate_synthetic_data`. This means that if the input parameters to this function don't change, Streamlit will use the cached results instead of re-running the function, significantly speeding up the application.
</aside>

The `validate_and_process_data` function ensures that the generated DataFrame has the expected columns, data types, and no missing or duplicate values, adding robustness to the application. The `log_summary_statistics` function, when called, displays basic descriptive statistics of the simulated data, which is useful for quick data sanity checks.

### 2. Theoretical Futures Price at Inception

The application calculates the theoretical no-arbitrage futures price at inception using the cost-of-carry model. This model states that the futures price ($F_0$) is the spot price ($S_0$) compounded at the risk-free rate, adjusted for any income (like dividends) or costs (like storage costs) associated with holding the underlying asset until maturity.

The formula used is:
$$F_0 = (S_0 - PV_{\text{Income}} + PV_{\text{Costs}}) \cdot (1 + r)^T$$
Where:
*   $F_0$: Theoretical futures price at time 0
*   $S_0$: Initial Spot Price
*   $PV_{\text{Income}}$: Present Value of any income generated by the underlying (e.g., dividends).
*   $PV_{\text{Costs}}$: Present Value of any costs associated with holding the underlying (e.g., storage costs).
*   $r$: Daily Risk-Free Rate
*   $T$: Days to Maturity

You can input values for $PV_{\text{Income}}$ and $PV_{\text{Costs}}$ to see how they affect the initial futures price. The calculated price is displayed using `st.metric`.

```python
# From application_pages/simulator.py
@st.cache_data
def calculate_futures_price_at_inception(spot_price, risk_free_rate, time_to_maturity, pv_income, pv_costs):
    return (spot_price - pv_income + pv_costs) * (1 + risk_free_rate)**time_to_maturity
```
<aside class="negative">
<b>Important Note:</b> The simulation uses `days_to_maturity` as the `time_to_maturity` for the `calculate_futures_price_at_inception` function. For typical futures pricing, a continuous compounding formula is often used, and the `time_to_maturity` would be in years. Here, it's simplified to a daily discrete compounding for consistency with the daily simulation.
</aside>

## Understanding Derivative Contract Cash Flows
Duration: 0:20

This section is the core of the simulation, demonstrating how cash flows differ based on the derivative type and the presence of central clearing. The application simulates the mark-to-market process and margin calls for cleared contracts.

### Non-Centrally Cleared OTC (Forwards)

The `simulate_forward_cash_flows` function models a traditional forward contract. In this scenario, there are generally no intermediate cash flows. The profit or loss (MTM Value) is realized as a single cash flow at the maturity date.

```python
# From application_pages/simulator.py
@st.cache_data
def simulate_forward_cash_flows(initial_forward_price, simulated_spot_prices, contract_size, risk_free_rate):
    df = pd.DataFrame({'Spot_Price': simulated_spot_prices})
    df['Day'] = range(1, len(df) + 1)
    df['Forward_MTM_Value'] = (df['Spot_Price'] - initial_forward_price) * contract_size
    df['Cash_Flow'] = 0.0
    # Only the last day has a cash flow equal to the final MTM value
    df.loc[df.index[-1], 'Cash_Flow'] = df['Forward_MTM_Value'].iloc[-1]
    return df[['Day', 'Forward_MTM_Value', 'Cash_Flow']]
```
<aside class="positive">
<b>Key Takeaway:</b> Observe that for non-centrally cleared forwards, the `Cash_Flow` column will be zero until the last day, where the entire Mark-to-Market (MTM) value is settled. This contrasts sharply with futures.
</aside>

### Exchange-Traded Futures

The `simulate_futures_cash_flows` function models an exchange-traded futures contract, characterized by daily mark-to-market and margin requirements.

*   **Daily PnL**: Each day, the contract is "marked to market." The profit or loss for the day is calculated as (Current Futures Price - Previous Futures Price) * Contract Size. This PnL is added to or subtracted from the margin account.
*   **Margin Balance**: This is the total collateral held with the clearinghouse. It starts with the `Initial Margin`.
*   **Margin Calls**: If the `Margin Balance` falls below the `Maintenance Margin` level, a margin call is issued. The trader must then deposit funds to bring the `Margin Balance` back up to the `Initial Margin` level. These deposits are reflected as negative `Cash_Flow`.

```python
# From application_pages/simulator.py
@st.cache_data
def simulate_futures_cash_flows(initial_futures_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    # ... (code as provided in simulator.py)
    # The crucial part for cash flow and margin calls:
    for i in range(1, len(simulated_spot_prices)):
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = daily_pnl[i] # Daily PnL is the cash flow unless a margin call happens

        if margin_balance[i] < maintenance_margin:
            # Margin call: cash needed to top up to initial margin
            cash_flow[i] = initial_margin - margin_balance[i]
            margin_balance[i] = initial_margin
    # ... (rest of the function)
```

### Centrally Cleared OTC

The `simulate_centrally_cleared_otc_cash_flows` function demonstrates how a centrally cleared OTC contract behaves very similarly to an exchange-traded future due to the CCP's margining and daily settlement rules. The logic for daily PnL, margin balance, and margin calls is essentially the same as for futures.

```python
# From application_pages/simulator.py
@st.cache_data
def simulate_centrally_cleared_otc_cash_flows(initial_otc_price, simulated_spot_prices, contract_size, initial_margin, maintenance_margin):
    # ... (code largely mirrors simulate_futures_cash_flows in terms of margin logic)
    # The key difference is the initial cash_flow[i] = 0.0 before margin call check,
    # meaning actual PnL is not immediately a cash flow unless it triggers a margin call,
    # or the contract closes. This is a subtle modeling choice.
    for i in range(1, n_days):
        margin_balance[i] = margin_balance[i-1] + daily_pnl[i]
        cash_flow[i] = 0.0 # By default, PnL is absorbed by margin unless a call

        if margin_balance[i] < maintenance_margin:
            cash_flow[i] = initial_margin - margin_balance[i]
            margin_balance[i] = initial_margin
    # ... (rest of the function)
```

### Daily Cash Flows and Margin Account Fluctuations Visualization

After running a simulation, the application displays an interactive Plotly chart. This chart is critical for visualizing:
*   `Cash Flow`: The actual cash moving in or out of your account on a given day.
*   `Daily PnL`: The profit or loss for that specific day.
*   `Margin Balance`: The current balance in your margin account.

By comparing these charts across the different scenario types, you can clearly see how daily mark-to-market and margin calls lead to frequent cash flows for cleared contracts, reducing the single large settlement risk of traditional forwards.

### Credit Risk Assessment

The `determine_credit_risk` function provides a qualitative assessment of credit risk based on the chosen scenario.

*   **Non-Centrally Cleared OTC**: "High" credit risk, as you face the direct counterparty risk of the other party defaulting.
*   **Centrally Cleared OTC**: "Low" credit risk, as the CCP guarantees performance, insulating you from the default of the original counterparty.
*   **Exchange-Traded Futures**: "Low" credit risk, also due to the CCP's guarantee.

This metric highlights one of the primary benefits of central clearing.

## Exploring Residual Price Differences (Heatmap)
Duration: 0:10

Even with central clearing, slight price differences can persist between futures and forwards. These differences often stem from factors related to the reinvestment of daily gains or the funding of daily losses, which are affected by interest rate dynamics and correlations.

The `calculate_price_difference_heatmap_data` function in the application is designed to illustrate this concept. In a fully developed financial model, this function would calculate the actual theoretical price differences between futures and forwards under various interest rate correlation and volatility scenarios.

Currently, the function generates **dummy random data** for the heatmap. However, its purpose is to convey the idea that these factors are relevant:

```python
# From application_pages/simulator.py
@st.cache_data
def calculate_price_difference_heatmap_data(correlation_range, volatility_range):
    # ... (generates random data within the specified ranges)
    price_difference_data = np.random.rand(num_points, num_points)
    # ...
    return df
```

The heatmap visualizes `Price Difference` across varying levels of `Interest Rate Correlation` (Y-axis) and `Interest Rate Volatility` (X-axis). The sliders in the sidebar (`Min Correlation`, `Max Correlation`, `Min Volatility (Heatmap)`, `Max Volatility (Heatmap)`) allow you to define the ranges for these axes.

<aside class="positive">
<b>Concept Reinforcement:</b> While this heatmap uses dummy data, it's a powerful visual placeholder. In a real-world scenario, you would observe how significant correlations between the underlying asset price and interest rates, or high interest rate volatility, could lead to non-trivial basis differences between futures and forwards, even when both are centrally cleared. This is due to the impact of daily settlement cash flows being reinvested or funded at prevailing (and potentially stochastic) interest rates.
</aside>

This section underscores that central clearing, while vastly reducing credit risk and standardizing processes, does not necessarily eliminate all theoretical price differences caused by complex market dynamics.

## Review and Further Exploration
Duration: 0:05

You have successfully navigated and understood the core functionalities of the QuLab Streamlit application focusing on central clearing.

### Key Takeaways

*   **Central clearing** significantly reduces **counterparty risk** by interposing a **CCP**.
*   **Futures contracts** and **centrally cleared OTC derivatives** share similar characteristics, primarily **daily mark-to-market** and **margin requirements**, leading to frequent cash flows.
*   **Traditional OTC forwards** involve a single cash flow at maturity, exposing parties to higher counterparty risk over the contract's life.
*   The application demonstrates how **margin calls** are triggered when the margin balance falls below the maintenance level, requiring additional collateral.
*   Even with central clearing, subtle price differences between futures and forwards can arise due to factors like **interest rate correlation and volatility**, impacting the value of interim cash flows.

### Further Exploration

1.  **Parameter Sensitivity**: Go back to the "Simulator" and actively change the `Initial Margin`, `Maintenance Margin`, and `Daily Volatility`. Observe how these changes affect the `Margin Balance` and `Cash Flow` graphs, especially the frequency and magnitude of margin calls.
2.  **Code Enhancements**:
    *   **Real Data for Heatmap**: Replace the dummy data generation in `calculate_price_difference_heatmap_data` with a more sophisticated model that genuinely calculates the futures-forward basis under varying interest rate environments. This would involve stochastic interest rate models.
    *   **Multiple Simulations**: Add an option to run multiple simulations of spot prices to get a distribution of outcomes for cash flows and final PnL.
    *   **Advanced Risk Metrics**: Implement calculations for Value at Risk (VaR) or Expected Shortfall (ES) for the different derivative types.
3.  **Educational Content**: Expand the "Introduction" and "References" sections with more detailed explanations, examples, and links to relevant academic papers or industry reports.

This application provides a robust foundation for understanding a critical aspect of modern financial markets. Continue experimenting, learning, and building!

<button>
  [Explore QuantUniversity Resources](https://www.quantuniversity.com)
</button>
