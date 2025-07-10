
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Redefine functions or import them if shared.
@st.cache_data
def calculate_price_difference_heatmap_data(correlation_range, volatility_range):
    if not (isinstance(correlation_range, tuple) and isinstance(volatility_range, tuple)):
        raise TypeError("Ranges must be tuples.")

    correlation_start, correlation_end = correlation_range
    volatility_start, volatility_end = volatility_range

    num_points = 10
    correlation_values = np.linspace(min(correlation_start, correlation_end), max(correlation_start, correlation_end), num_points)
    volatility_values = np.linspace(min(volatility_start, volatility_end), max(volatility_start, volatility_end), num_points)

    # Create dummy price difference data (as per specification)
    price_difference_data = np.random.rand(num_points, num_points)

    df = pd.DataFrame(price_difference_data, index=correlation_values.round(2), columns=volatility_values.round(3))
    df.index.name = "Interest Rate Correlation"
    df.columns.name = "Interest Rate Volatility"
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

def run_page3():
    st.header("Risk Analysis & Heatmap")
    st.markdown("""
    This page provides a qualitative assessment of credit risk based on the chosen derivative scenario and visualizes the potential residual price differences between futures and forwards influenced by factors like interest rate correlation and volatility.
    """)

    st.subheader("Credit Risk Assessment")
    # Retrieve scenario_type from session state or provide a default if not set
    # This might be tricky if a user directly navigates here without setting scenario_type on page2.
    # To handle this, we can offer a basic radio button for credit risk analysis specific to this page
    # or rely on the user having visited page 2. For now, assume session_state might be set.
    
    # If scenario_type isn't set, default to a sensible option or prompt the user.
    # We will use a dedicated radio button for this page's credit risk display
    # so it works independently.
    scenario_type_for_risk = st.radio(
        "Select Derivative Type for Credit Risk Assessment:",
        ("Non-Centrally Cleared OTC", "Centrally Cleared OTC", "Exchange-Traded Futures"),
        key='scenario_type_risk_assessment'
    )
    credit_risk = determine_credit_risk(scenario_type_for_risk)
    st.metric("Credit Risk Exposure", credit_risk)
    st.markdown("---")

    st.subheader("Residual Price Differences: Impact of Correlation and Volatility")
    st.markdown("""
    Even with central clearing, factors like interest rate correlation and volatility can still contribute to price differences between futures and forwards. This heatmap illustrates these potential residual differences (using dummy data for demonstration).
    """)

    # Heatmap Parameters
    st.sidebar.header("Heatmap Parameters")
    corr_min = st.sidebar.slider("Min Correlation", -1.0, 1.0, st.session_state.get('corr_min', -0.5), 0.1, key='corr_min_input')
    corr_max = st.sidebar.slider("Max Correlation", -1.0, 1.0, st.session_state.get('corr_max', 0.5), 0.1, key='corr_max_input')
    vol_min = st.sidebar.slider("Min Volatility (Heatmap)", 0.0, 1.0, st.session_state.get('vol_min', 0.1), 0.01, key='vol_min_input')
    vol_max = st.sidebar.slider("Max Volatility (Heatmap)", 0.0, 1.0, st.session_state.get('vol_max', 0.4), 0.01, key='vol_max_input')
    
    st.session_state['corr_min'] = corr_min
    st.session_state['corr_max'] = corr_max
    st.session_state['vol_min'] = vol_min
    st.session_state['vol_max'] = vol_max

    correlation_range = (corr_min, corr_max)
    volatility_range = (vol_min, vol_max)

    try:
        heatmap_data = calculate_price_difference_heatmap_data(correlation_range, volatility_range)
        fig_heatmap = px.imshow(heatmap_data,
                                 labels=dict(x="Interest Rate Volatility", y="Interest Rate Correlation", color="Price Difference"),
                                 x=[f"{col:.3f}" for col in heatmap_data.columns.astype(float)], # Format for better display
                                 y=[f"{idx:.2f}" for idx in heatmap_data.index.astype(float)], # Format for better display
                                 color_continuous_scale="Viridis",
                                 title="Price Difference Heatmap (Dummy Data)")
        fig_heatmap.update_layout(font_size=12)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown("*(Note: Heatmap data is currently dummy data and would be replaced by actual calculations based on "
                    "interest rate correlation and volatility in a production environment.)*")
    except TypeError as e:
        st.error(f"Error generating heatmap: {e}. Please ensure correlation and volatility ranges are valid.")

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

if __name__ == "__main__":
    run_page3()
