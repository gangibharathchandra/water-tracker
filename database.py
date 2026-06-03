import pandas as pd
import os

FILE = "complaints.csv"

def init_db():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "Name",
            "Phone",
            "Issue",
            "Location",
            "Description",
            "Image",
            "Time",
            "Status",
            "Resolution"
        ])
        df.to_csv(FILE, index=False)


def add_complaint(data):
    init_db()
    df = pd.read_csv(FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(FILE, index=False)


def get_all_complaints():
    init_db()
    return pd.read_csv(FILE)


def update_status(index, status, resolution=""):
    df = pd.read_csv(FILE)

    if index < 0 or index >= len(df):
        return False

    df.loc[index, "Status"] = status
    df.loc[index, "Resolution"] = resolution

    df.to_csv(FILE, index=False)
    return True