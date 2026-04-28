import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Power Status", layout="centered")

# -------- HIDE STREAMLIT UI --------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.blink {
  animation: blink 1s infinite;
  color: red;
  font-size: 28px;
  font-weight: bold;
  text-align: left;
}

@keyframes blink {
  50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# -------- LOAD DATA (CACHED) --------
@st.cache_data(ttl=10)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1fi9b3wtfoseQ--iCQgegLBT7s0SMPY59yus73g0xc18/export?format=csv"
    df = pd.read_csv(url)
    df["State"] = df["State"].astype(str).str.strip()
    df["Status"] = df["Status"].astype(str).str.strip()
    return df

df = load_data()
df_active = df[df["State"] == "Active"]

# -------- HEADER --------
st.title("⚡ Live Power Status")

# -------- MAIN DISPLAY --------
if df_active.empty:
    st.success("✅ All areas are operating normally")

else:
    for index, row in df_active.iterrows():

        location = str(row["Location"]).strip()
        status = str(row["Status"]).strip()

        # 🔴 FAULT → blinking heading
        if status == "Fault":
            st.markdown(f"""
            <div class='blink'>⚠ {location}</div>
            """, unsafe_allow_html=True)

            st.error(
                f"{row['Feeder']} | {row['Reason']} | ETA: {row['ETA (hrs)']} hrs"
            )

        # 🟡 MAINTENANCE → normal heading
        else:
            st.markdown(f"### 📍 {location}")

            st.warning(
                f"{row['Feeder']} | Maintenance | ETA: {row['ETA (hrs)']} hrs"
            )

# -------- FOOTER --------
st.caption("Updated automatically")

# -------- AUTO REFRESH --------
time.sleep(10)
st.rerun()
