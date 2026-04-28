import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# -------- TITLE --------
st.title("⚡ LIVE POWER STATUS")
st.caption("Real-time outage and maintenance updates")

# -------- DATA --------
url = "https://docs.google.com/spreadsheets/d/1fi9b3wtfoseQ--iCQgegLBT7s0SMPY59yus73g0xc18/export?format=csv"

df = pd.read_csv(url)

# Clean text
df["State"] = df["State"].astype(str).str.strip()
df["Status"] = df["Status"].astype(str).str.strip()

# Filter active only
df_active = df[df["State"] == "Active"]

# -------- STYLE --------
st.markdown("""
<style>
@keyframes blink {
  50% { opacity: 0; }
}
.blink {
  color: red;
  font-size: 26px;
  font-weight: bold;
  animation: blink 1s infinite;
}
.yellow {
  color: orange;
  font-size: 24px;
  font-weight: bold;
}
.card {
  padding: 15px;
  border-radius: 10px;
  background-color: #111;
  margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------- DISPLAY --------
if df_active.empty:
    st.success("✅ All areas are operating normally")
else:
    locations = df_active["Location"].unique()

    for loc in locations:
        st.markdown(f"## 📍 {loc}")

        loc_df = df_active[df_active["Location"] == loc]

        for _, row in loc_df.iterrows():

            if row["Status"] == "Fault":
                st.markdown(f"""
                <div class="card">
                    <div class="blink">🔴 POWER OUTAGE - {row['Feeder']}</div>
                    Reason: {row['Reason']} <br>
                    ⏱ Expected restoration: {row['ETA (hrs)']} hrs
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="card">
                    <div class="yellow">🟡 MAINTENANCE - {row['Feeder']}</div>
                    Work: {row['Reason']} <br>
                    ⏱ Expected completion: {row['ETA (hrs)']} hrs
                </div>
                """, unsafe_allow_html=True)

# -------- REFRESH --------
st.caption("🔄 Auto-updates on refresh")