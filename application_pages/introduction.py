
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
