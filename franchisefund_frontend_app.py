
import streamlit as st
import pandas as pd

st.set_page_config(page_title="FranchiseFund", layout="centered")

# Title
st.title("FranchiseFund")
st.subheader("Own a Piece of Real Sports Teams")

# Team overview
st.markdown("### Investment Opportunity: London Lions FC")
st.write("**Team Valuation:** $50,000,000")
st.write("**Equity Offered to Fans:** 1%")
st.write("**Share Price:** $50.00")
st.write("**Shares Available:** 10,000")

# Progress bar (simulated)
progress = 8750  # Simulated shares sold
st.progress(progress / 10000)

# User investment input
st.markdown("### Buy Shares")
shares = st.number_input("Number of Shares to Buy", min_value=1, max_value=1000, value=10)
total = shares * 50
if st.button("Confirm Investment"):
    st.success(f"You've invested ${total:.2f} in London Lions FC for {shares} shares.")

# Portfolio tracker (sample data)
st.markdown("### Your Portfolio")
data = {
    "Team": ["London Lions FC"],
    "Shares Owned": [200],
    "Total Invested ($)": [10000.00],
    "% of Fan Pool": ["2.00%"],
    "% of Team Owned": ["0.0200%"]
}
df = pd.DataFrame(data)
st.table(df)

st.caption("Powered by FranchiseFund - Real Ownership for Real Fans.")
