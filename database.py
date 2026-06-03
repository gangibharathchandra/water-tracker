import pandas as pd
import os

FILE = "complaints.csv"

# Create DB file if not exists
def init_db():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "Name", "Phone", "Issue",
            "Location", "Description",
            "Time", "Status"
        ])
        df.to_csv(FILE, index=False)


# ADD complaint
def add_complaint(data):
    init_db()
    df = pd.read_csv(FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(FILE, index=False)


# GET all complaints
def get_all_complaints():
    init_db()
    return pd.read_csv(FILE)


# UPDATE status
def update_status(index, status):
    df = pd.read_csv(FILE)

    if index < 0 or index >= len(df):
        return False

    df.loc[index, "Status"] = status
    df.to_csv(FILE, index=False)
    return True