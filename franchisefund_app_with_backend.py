
import streamlit as st
import pandas as pd

st.set_page_config(page_title="FranchiseFund", layout="centered")

st.title("FranchiseFund")
st.subheader("Own a Piece of Real Sports Teams")

# Team info
team_name = "London Lions FC"
team_valuation = 50000000
equity_offered_to_fans = 0.01
total_shares = 10000
share_price = (team_valuation * equity_offered_to_fans) / total_shares

st.markdown("### Investment Opportunity: London Lions FC")
st.write(f"**Team Valuation:** ${team_valuation:,}")
st.write(f"**Equity Offered to Fans:** {equity_offered_to_fans*100}%")
st.write(f"**Share Price:** ${share_price:.2f}")
st.write(f"**Shares Available:** {total_shares}")

# Buy shares
st.markdown("### Buy Shares")
user_name = st.text_input("Enter your name")
shares_to_buy = st.number_input("Number of Shares to Buy", min_value=1, max_value=1000, value=10)
invested_amount = shares_to_buy * share_price
confirm = st.button("Confirm Investment")

# Data persistence (for demo purposes, reset every run)
if "transactions" not in st.session_state:
    st.session_state.transactions = {}

if confirm and user_name:
    st.session_state.transactions[user_name] = st.session_state.transactions.get(user_name, 0) + shares_to_buy
    st.success(f"{user_name} invested ${invested_amount:.2f} for {shares_to_buy} shares!")

# Display portfolio
st.markdown("### Fan Ownership Tracker")
data = []
for user, shares in st.session_state.transactions.items():
    amount = shares * share_price
    fan_pool_pct = shares / total_shares * 100
    team_pct = equity_offered_to_fans * (shares / total_shares) * 100
    data.append({
        "User": user,
        "Shares Owned": shares,
        "Amount Invested ($)": round(amount, 2),
        "% of Fan Pool": round(fan_pool_pct, 2),
        "% of Team Owned": round(team_pct, 4)
    })

if data:
    df = pd.DataFrame(data)
    st.table(df)

st.caption("Powered by FranchiseFund - Real Ownership for Real Fans.")
