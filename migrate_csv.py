"""One-time script to move existing complaints.csv data into MySQL."""

import os

import pandas as pd

from database import add_complaint, get_all_complaints, init_db

CSV_FILE = "complaints.csv"


def migrate():
    if not os.path.exists(CSV_FILE):
        print(f"No {CSV_FILE} found. Nothing to migrate.")
        return

    init_db()
    existing = len(get_all_complaints())
    if existing > 0:
        print(f"MySQL already has {existing} complaint(s). Skipping migration.")
        return

    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print(f"{CSV_FILE} is empty. Nothing to migrate.")
        return

    for _, row in df.iterrows():
        add_complaint(
            {
                "Name": row["Name"],
                "Phone": row["Phone"],
                "Issue": row["Issue"],
                "Location": row["Location"],
                "Description": row.get("Description", ""),
                "Image": row.get("Image", ""),
                "Time": row["Time"],
                "Status": row.get("Status", "Pending"),
                "Resolution": row.get("Resolution", ""),
            }
        )

    print(f"Migrated {len(df)} complaint(s) from {CSV_FILE} to MySQL.")


if __name__ == "__main__":
    migrate()
