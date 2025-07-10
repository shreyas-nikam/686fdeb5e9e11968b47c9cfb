
import streamlit as st
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
In this lab, we will explore the impact of central clearing on derivatives markets, specifically focusing on how margin requirements and daily settlement for centrally cleared OTC contracts reduce the cash flow and price differences between ETDs like futures and OTC forwards.
This application allows you to simulate different market conditions and clearing scenarios to visualize these effects.
""")
# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Central Clearing Impact Simulator"])
if page == "Central Clearing Impact Simulator":
    from application_pages.central_clearing_simulator import run_central_clearing_simulator
    run_central_clearing_simulator()
# Your code ends
st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
            "Any reproduction of this demonstration "
            "requires prior written consent from QuantUniversity. "
            "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors")
