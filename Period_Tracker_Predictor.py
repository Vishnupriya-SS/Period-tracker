import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import timedelta
import os

st.set_page_config(page_title="Period Tracker", layout="centered")
st.title("🩸 Period Tracker & Mood Logger")

# Initialize CSV file if not present
DATA_FILE = 'period_data.csv'
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        'start_date', 'end_date', 'duration', 'cycle_length', 'flow', 'pain', 'clots', 'mood'
    ])
    df.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE, parse_dates=['start_date', 'end_date'])

def save_data(new_entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def train_and_predict(df):
    df = df.dropna(subset=['cycle_length'])
    if len(df) < 5:
        return None, None
    X = df[['cycle_length']].values
    y = df['duration'].values
    model = LinearRegression()
    model.fit(X, y)
    last_start = df.iloc[-1]['start_date']
    last_end = df.iloc[-1]['end_date']
    last_cycle = df.iloc[-1]['cycle_length']
    next_start = last_end + timedelta(days=last_cycle)
    predicted_duration = round(model.predict([[last_cycle]])[0])
    next_end = next_start + timedelta(days=predicted_duration - 1)
    return next_start.date(), next_end.date()

# Track new entry form display
if 'new_entry' not in st.session_state:
    st.session_state.new_entry = False

st.subheader("📆 Log Your Period")

if st.button("➕ New Period Entry"):
    st.session_state.new_entry = True

if st.session_state.new_entry:
    start_date = st.date_input("Start Date", format="DD-MM-YYYY")
    end_date = st.date_input("End Date", format="DD-MM-YYYY")

    if end_date < start_date:
        st.warning("End date must be after start date.")
        st.stop()

    flow = st.selectbox("Flow", ["low", "medium", "high"])
    pain = st.selectbox("Pain", ["none", "mild", "moderate", "severe"])
    clots = st.radio("Blood Clots?", ["yes", "no"])
    mood = st.selectbox("Mood", ["happy 😊", "sad 😢", "in pain 🤕", "irritated 😠"])

    if st.button("Log Period"):
        df = load_data()
        duration = (pd.Timestamp(end_date) - pd.Timestamp(start_date)).days + 1

        # Recalculate cycle_length based on previous start date
        if not df.empty:
            df_sorted = df.sort_values(by='start_date')
            last_start = df_sorted.iloc[-1]['start_date']
            cycle_length = (pd.Timestamp(start_date) - pd.Timestamp(last_start)).days
        else:
            cycle_length = None

        entry = {
            'start_date': pd.Timestamp(start_date),
            'end_date': pd.Timestamp(end_date),
            'duration': duration,
            'cycle_length': cycle_length,
            'flow': flow,
            'pain': pain,
            'clots': clots,
            'mood': mood
        }

        save_data(entry)
        st.session_state.new_entry = False
        st.success("✅ Period logged successfully!")

st.subheader("🧪 Analysis Options")

df = load_data()
df = df.sort_values(by='start_date')
recent_cycles = df.dropna(subset=['cycle_length']).tail(4)['cycle_length']

if st.button("✅ Check Period Regularity"):
    if len(recent_cycles) >= 4:
        if all(21 <= cl <= 35 for cl in recent_cycles):
            st.success("Your periods appear REGULAR 🟢")
        else:
            st.warning("Your periods appear IRREGULAR 🔴")
    else:
        st.info("ℹ️ At least 4 entries required to assess period regularity.")

if st.button("🔮 Predict Period"):
    if len(df.dropna(subset=['cycle_length'])) >= 5:
        next_start, next_end = train_and_predict(df)
        if next_start and next_end:
            st.subheader("Predicted Next Period")
            st.write(f"Next Start Date: `{next_start}`")
            st.write(f"Expected End Date: `{next_end}`")
    else:
        st.info("ℹ️ At least 5 entries required for prediction.")

st.subheader("📋 Recent Entries")
st.dataframe(df.tail(5).sort_values(by='start_date', ascending=False), use_container_width=True)

st.markdown("---")
st.caption("Made with ❤️ for women’s health support")
