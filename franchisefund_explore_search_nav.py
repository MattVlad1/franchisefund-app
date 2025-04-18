
import streamlit as st
import pandas as pd

# Config
st.set_page_config(page_title="FranchiseFund", layout="wide")

# Constants
teams_data = [
    {"name": "London Lions FC", "valuation": 50000000, "equity": 0.01},
    {"name": "Celtics", "valuation": 3000000000, "equity": 0.01},
    {"name": "Yankees", "valuation": 7000000000, "equity": 0.01},
    {"name": "Packers", "valuation": 4000000000, "equity": 0.01},
    {"name": "Lakers", "valuation": 5500000000, "equity": 0.01}
]
total_shares = 10000

# Mock login user
user = "Matthew"

# Persistent user state
if "shares_owned" not in st.session_state:
    st.session_state.shares_owned = {}
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Market"

# Tab buttons
tabs = ["Market", "Portfolio", "Watchlist", "Explore", "Admin"]
cols = st.columns(len(tabs))
for i, tab in enumerate(tabs):
    if cols[i].button(tab):
        st.session_state.active_tab = tab
st.markdown("---")

# MARKET TAB
if st.session_state.active_tab == "Market":
    st.title("Market Overview")
    st.subheader("Top Gainers & Losers")
    data = {
        "Team": ["Celtics", "Packers", "Yankees", "Lakers", "Cardinals", "Warriors"],
        "Price": [18.23, 14.10, 21.76, 12.05, 9.88, 15.42],
        "Change": [0.26, -0.42, 0.40, -0.33, 0.29, 0.55]
    }
    df = pd.DataFrame(data)
    df["Change (%)"] = df["Change"] / (df["Price"] - df["Change"]) * 100
    df["Change"] = df["Change"].apply(lambda x: f"{x:+.2f}")
    df["Change (%)"] = df["Change (%)"].apply(lambda x: f"{x:+.2f}%")
    st.table(df[["Team", "Price", "Change", "Change (%)"]])

# PORTFOLIO TAB
elif st.session_state.active_tab == "Portfolio":
    st.title("Your Portfolio")
    if user in st.session_state.shares_owned:
        rows = []
        for team, shares in st.session_state.shares_owned[user].items():
            t_info = next((t for t in teams_data if t["name"] == team), None)
            if t_info:
                share_price = (t_info["valuation"] * t_info["equity"]) / total_shares
                invested = shares * share_price
                fan_pool_pct = shares / total_shares * 100
                team_pct = t_info["equity"] * (shares / total_shares) * 100
                rows.append({
                    "Team": team,
                    "Shares Owned": shares,
                    "Total Invested ($)": round(invested, 2),
                    "% of Fan Pool": round(fan_pool_pct, 2),
                    "% of Team Owned": round(team_pct, 4)
                })
        st.table(pd.DataFrame(rows))
    else:
        st.info("Go to Explore to start buying shares.")

# WATCHLIST TAB
elif st.session_state.active_tab == "Watchlist":
    st.title("Watchlist")
    st.write("Coming soon: Add teams to your watchlist and track live share prices.")

# EXPLORE TAB
elif st.session_state.active_tab == "Explore":
    st.title("Explore Teams")
    search = st.text_input("Search for a team...")
    for team in teams_data:
        if search.lower() in team["name"].lower():
            share_price = (team["valuation"] * team["equity"]) / total_shares
            st.subheader(team["name"])
            st.write(f"**Valuation:** ${team['valuation']:,}")
            st.write(f"**Equity Offered to Fans:** {team['equity']*100}%")
            st.write(f"**Share Price:** ${share_price:.2f}")
            shares_to_buy = st.number_input(f"Buy shares of {team['name']}", min_value=1, max_value=1000, value=1, key=f"buy_{team['name']}")
            if st.button(f"Buy {shares_to_buy} shares", key=f"btn_{team['name']}"):
                if user not in st.session_state.shares_owned:
                    st.session_state.shares_owned[user] = {}
                st.session_state.shares_owned[user][team["name"]] = (
                    st.session_state.shares_owned[user].get(team["name"], 0) + shares_to_buy
                )
                st.success(f"You bought {shares_to_buy} shares of {team['name']} (${shares_to_buy * share_price:.2f})")

# ADMIN TAB
elif st.session_state.active_tab == "Admin":
    st.title("Admin Panel")
    all_data = []
    for team in teams_data:
        total_raised = 0
        total_shares_sold = 0
        if user in st.session_state.shares_owned and team["name"] in st.session_state.shares_owned[user]:
            shares = st.session_state.shares_owned[user][team["name"]]
            share_price = (team["valuation"] * team["equity"]) / total_shares
            invested = shares * share_price
            fan_pool_pct = shares / total_shares * 100
            team_pct = team["equity"] * (shares / total_shares) * 100
            total_raised += invested
            total_shares_sold += shares
            all_data.append({
                "Team": team["name"],
                "Shares Sold": shares,
                "Raised ($)": round(invested, 2),
                "% of Team Owned": round(team_pct, 4)
            })

    if all_data:
        st.table(pd.DataFrame(all_data))
    else:
        st.info("No investments made yet.")
