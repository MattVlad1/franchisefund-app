
import streamlit as st
import pandas as pd

# Simulated team data
team_name = "London Lions FC"
valuation = 50000000
equity_offered = 0.01
total_shares = 10000
share_price = (valuation * equity_offered) / total_shares

# Setup persistent session state
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "shares_owned" not in st.session_state:
    st.session_state.shares_owned = {}

# App layout
st.set_page_config(page_title="FranchiseFund", layout="wide")

# Tabs
tab = st.sidebar.radio("Navigation", ["Explore", "Portfolio", "Watchlist", "Admin"])

# Tab: Explore
if tab == "Explore":
    st.title("Explore Teams")
    st.subheader(team_name)
    st.write(f"**Valuation:** ${valuation:,}")
    st.write(f"**Equity Available to Fans:** {equity_offered*100}%")
    st.write(f"**Share Price:** ${share_price:.2f}")
    st.write(f"**Total Shares:** {total_shares}")

    if st.session_state.user_name == "":
        st.session_state.user_name = st.text_input("Enter your name to start:", key="name_input")

    if st.session_state.user_name:
        shares_to_buy = st.number_input("How many shares would you like to buy?", min_value=1, max_value=1000, value=10)
        if st.button("Buy Shares"):
            user = st.session_state.user_name
            st.session_state.shares_owned[user] = st.session_state.shares_owned.get(user, 0) + shares_to_buy
            st.success(f"{user} bought {shares_to_buy} shares (${shares_to_buy * share_price:.2f})")

# Tab: Portfolio
elif tab == "Portfolio":
    st.title("Your Portfolio")
    user = st.session_state.user_name
    if user and user in st.session_state.shares_owned:
        shares = st.session_state.shares_owned[user]
        investment = shares * share_price
        fan_pool_pct = shares / total_shares * 100
        team_pct = equity_offered * (shares / total_shares) * 100

        data = {
            "Team": [team_name],
            "Shares Owned": [shares],
            "Total Invested ($)": [round(investment, 2)],
            "% of Fan Pool": [round(fan_pool_pct, 2)],
            "% of Team Owned": [round(team_pct, 4)]
        }
        st.table(pd.DataFrame(data))
    else:
        st.info("Go to Explore to start buying shares.")

# Tab: Watchlist (placeholder)
elif tab == "Watchlist":
    st.title("Watchlist")
    st.write("Coming soon: Add teams to your watchlist to track their share prices.")

# Tab: Admin
elif tab == "Admin":
    st.title("Admin Panel")
    all_data = []
    total_raised = 0
    for user, shares in st.session_state.shares_owned.items():
        invested = shares * share_price
        fan_pool_pct = shares / total_shares * 100
        team_pct = equity_offered * (shares / total_shares) * 100
        total_raised += invested
        all_data.append({
            "User": user,
            "Shares Owned": shares,
            "Invested ($)": round(invested, 2),
            "% of Fan Pool": round(fan_pool_pct, 2),
            "% of Team Owned": round(team_pct, 4)
        })

    if all_data:
        df = pd.DataFrame(all_data)
        df.loc["TOTAL"] = ["—", sum(df["Shares Owned"]), round(total_raised, 2), "100%", f"{equity_offered*100:.2f}%"]
        st.table(df)
    else:
        st.info("No user data yet.")
