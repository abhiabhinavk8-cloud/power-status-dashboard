import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Power Status", layout="wide")

# Auto refresh every 10 sec
st_autorefresh(interval=10000, key="refresh")

# ---------------- HIDE STREAMLIT UI ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div style="background-color:#0b3d91;padding:15px;border-radius:8px">
    <h1 style="color:white;margin:0;">⚡ Electricity Board – Live Power Status</h1>
    <p style="color:white;margin:0;">Real-time outage and maintenance updates</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- DATA ----------------
url = "https://docs.google.com/spreadsheets/d/1fi9b3wtfoseQ--iCQgegLBT7s0SMPY59yus73g0xc18/export?format=csv"

df = pd.read_csv(url)

df["State"] = df["State"].astype(str).str.strip()
df["Status"] = df["Status"].astype(str).str.strip()

df_active = df[df["State"] == "Active"]

# ---------------- STATUS BANNER ----------------
if df_active.empty:
    st.markdown("""
    <div style="background-color:#28a745;padding:15px;border-radius:8px;text-align:center">
        <h2 style="color:white;">✅ All areas are operating normally</h2>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="background-color:#dc3545;padding:15px;border-radius:8px;text-align:center">
        <h2 style="color:white;">⚠️ Power interruptions reported</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- CSS ----------------
st.markdown("""
<style>
.card {
  padding: 15px;
  border-radius: 10px;
  background-color: #f8f9fa;
  margin-bottom: 10px;
  border-left: 6px solid red;
}
.maintenance {
  border-left: 6px solid orange;
}
.blink {
  animation: blink 1s infinite;
  font-weight: bold;
  color: red;
}
@keyframes blink {
  50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- DISPLAY ----------------
if not df_active.empty:
    locations = df_active["Location"].unique()

    for loc in locations:
        st.markdown(f"### 📍 {loc}")

        loc_df = df_active[df_active["Location"] == loc]

        for _, row in loc_df.iterrows():

            if row["Status"] == "Fault":
                st.markdown(f"""
                <div class="card">
                    <div class="blink">🔴 POWER OUTAGE – {row['Feeder']}</div>
                    <b>Reason:</b> {row['Reason']}<br>
                    <b>Expected restoration:</b> {row['ETA (hrs)']} hrs
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="card maintenance">
                    <div style="color:orange;font-weight:bold;">🟡 MAINTENANCE – {row['Feeder']}</div>
                    <b>Work:</b> {row['Reason']}<br>
                    <b>Expected completion:</b> {row['ETA (hrs)']} hrs
                </div>
                """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<hr>
<p style="text-align:center;color:gray;">
This is a public information system. Data is updated by field staff.
</p>
""", unsafe_allow_html=True)