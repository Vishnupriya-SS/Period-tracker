import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import os

DATA_FILE = 'period_data.csv'

# Initialize CSV if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        'start_date', 'end_date', 'duration', 'cycle_length', 'flow', 'pain', 'clots', 'mood'
    ])
    df.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE, parse_dates=['start_date', 'end_date'])

def save_data(entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def log_period():
    start_input = input("Enter start date (dd-mm-yyyy): ")
    end_input = input("Enter end date (dd-mm-yyyy): ")
    start_date = datetime.strptime(start_input, "%d-%m-%Y")
    end_date = datetime.strptime(end_input, "%d-%m-%Y")

    if end_date < start_date:
        print("⚠️ End date must be after start date.")
        return

    flow = input("Flow (low/medium/high): ").strip().lower()
    pain = input("Pain (none/mild/moderate/severe): ").strip().lower()
    clots = input("Blood clots? (yes/no): ").strip().lower()
    mood = input("Mood (happy/sad/in pain/angry): ").strip().lower()
    mood_emojis = {
        'happy': '😊', 'sad': '😢', 'in pain': '🤕', 'angry': '😠'
    }

    df = load_data()
    duration = (end_date - start_date).days + 1

    # Calculate cycle length
    if not df.empty:
        df = df.sort_values(by='start_date')
        last_start = df.iloc[-1]['start_date']
        cycle_length = (start_date - last_start).days
    else:
        cycle_length = None

    entry = {
        'start_date': start_date,
        'end_date': end_date,
        'duration': duration,
        'cycle_length': cycle_length,
        'flow': flow,
        'pain': pain,
        'clots': clots,
        'mood': f"{mood} {mood_emojis.get(mood, '')}"
    }

    save_data(entry)
    print("✅ Period logged successfully.")

def check_regularity():
    df = load_data()
    recent_cycles = df.dropna(subset=['cycle_length']).tail(4)['cycle_length']
    if len(recent_cycles) < 4:
        print("ℹ️ At least 4 entries are required to check regularity.")
    elif all(21 <= cl <= 35 for cl in recent_cycles):
        print("🟢 Periods appear REGULAR.")
    else:
        print("🔴 Periods appear IRREGULAR.")

def predict_next_period():
    df = load_data().dropna(subset=['cycle_length'])
    if len(df) < 5:
        print("ℹ️ At least 5 entries required to predict next period.")
        return

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

    print(f"🔮 Predicted Start Date: {next_start.date()}")
    print(f"🔮 Expected End Date: {next_end.date()}")

def main():
    print("\n=== Period Tracker & Mood Logger ===")
    print("1. Log New Period")
    print("2. Check Period Regularity")
    print("3. Predict Next Period")
    print("4. View Last 5 Logs")
    print("5. Exit")

    while True:
        choice = input("\nChoose an option (1-5): ")

        if choice == '1':
            log_period()
        elif choice == '2':
            check_regularity()
        elif choice == '3':
            predict_next_period()
        elif choice == '4':
            df = load_data().sort_values(by='start_date', ascending=False).head(5)
            print(df[['start_date', 'end_date', 'duration', 'cycle_length', 'mood']])
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()
