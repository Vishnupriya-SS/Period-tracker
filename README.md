# 🩸 Period Tracker & Mood Logger

A lightweight **Streamlit app** that allows users to log period data, track mood and symptoms, and predict their next period using **Linear Regression**. The app also checks for **menstrual regularity** and stores all entries for reference.
To run use Period_Tracker_Predictor.py script , the other script is the console script
---

## 📌 Features

- Log **start and end dates** of periods.
- Record **flow**, **pain level**, **clots**, and **mood** (with emojis).
- Automatically calculate:
  - **Period duration** (end date − start date + 1)
  - **Cycle length** (current start date − previous start date)
- Predict the **next period** using Linear Regression after 5 entries.
- Check if periods are **regular** based on cycle length (21–35 days) using the last 4 entries.
- Data is stored in a local CSV file (`period_data.csv`).

---

## 🛠️ Requirements

- Python 3.7+
- Libraries:
  ```bash
  pip install streamlit pandas scikit-learn
  ```

---

## ▶️ How to Run

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the following command:
   ```bash
   streamlit run app.py
   ```
4. A new browser window will open with the app running locally.

---

## 📁 Data Handling

All user data is saved in `period_data.csv` with the following columns:

| Column        | Description                                         |
|---------------|-----------------------------------------------------|
| `start_date`  | Period start date (`dd-mm-yyyy`)                   |
| `end_date`    | Period end date                                     |
| `duration`    | Number of days between start and end date          |
| `cycle_length`| Days between current start date and last start date|
| `flow`        | Flow intensity: `low`, `medium`, `high`            |
| `pain`        | Pain level: `none`, `mild`, `moderate`, `severe`   |
| `clots`       | Whether clots were passed: `yes` / `no`            |
| `mood`        | Mood of the user, selected from emoji-based list   |

---

## 📅 Definitions

- **Period Duration**:  
  ```
  duration = (end_date - start_date) + 1
  ```

- **Cycle Length**:  
  ```
  cycle_length = start_date (current entry) - start_date (previous entry)
  ```

- **Regularity Criteria**:  
  - A period is **regular** if the **last 4 cycle lengths** are each between **21 and 35 days**.
  - Otherwise, it's considered **irregular**.

- **Prediction Criteria**:
  - At least **5 period entries** with valid cycle lengths must exist before prediction can occur.

---

## 🤖 Prediction Logic

- A **Linear Regression model** is trained on:
  - `X = cycle_length`
  - `y = duration`
- The **next period start date** is estimated as:
  ```
  next_start = last_end_date + last_cycle_length
  ```
- The **predicted period end date** is:
  ```
  next_end = next_start + predicted_duration - 1
  ```

---

## 🚨 Validation & Warnings

- If the **end date is before the start date**, the entry is blocked.
- If the **number of entries** is below the threshold (4 for regularity, 5 for prediction), users are notified with an informative message.
- Users can enter a new log by clicking **"➕ New Period Entry"**.

---

## 🧠 Mood & Symptoms Tracking

Users can select:

- **Flow**: `low`, `medium`, `high`
- **Pain**: `none`, `mild`, `moderate`, `severe`
- **Clots**: `yes`, `no`
- **Mood**:
  - 😊 Happy
  - 😢 Sad
  - 🤕 In Pain
  - 😠 Irritated

These logs are stored alongside period data for health tracking.

---

## 🧪 Example Workflow

1. Click **"➕ New Period Entry"**
2. Select **start** and **end** date from the calendar popup
3. Choose **flow**, **pain**, **clots**, and **mood**
4. Click **"Log Period"**
5. After 4 entries → use **"Check Period Regularity"**
6. After 5 entries → use **"Predict Period"**

---

## 🛡️ Notes

- All data is stored **locally** in `period_data.csv`.
- No user login system is implemented (can be integrated via external web platform).
- Make sure to **back up** data periodically if used long-term.
