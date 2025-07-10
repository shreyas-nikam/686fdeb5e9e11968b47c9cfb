
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
