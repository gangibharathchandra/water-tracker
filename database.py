import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

COMPLAINT_COLUMNS = [
    "Name",
    "Phone",
    "Issue",
    "Location",
    "Description",
    "Image",
    "Time",
    "Status",
    "Resolution",
]

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    issue VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,
    image VARCHAR(500),
    time VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Pending',
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "water_tracker"),
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()
    cursor.close()
    conn.close()


def _to_dataframe(rows, columns):
    if not rows:
        return pd.DataFrame(columns=COMPLAINT_COLUMNS)

    df = pd.DataFrame(rows, columns=columns)
    df = df.rename(
        columns={
            "id": "ID",
            "name": "Name",
            "phone": "Phone",
            "issue": "Issue",
            "location": "Location",
            "description": "Description",
            "image": "Image",
            "time": "Time",
            "status": "Status",
            "resolution": "Resolution",
            "created_at": "Created At",
        }
    )
    return df


def add_complaint(data):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO complaints
        (name, phone, issue, location, description, image, time, status, resolution)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["Name"],
            data["Phone"],
            data["Issue"],
            data["Location"],
            data["Description"],
            data["Image"],
            data["Time"],
            data["Status"],
            data.get("Resolution", ""),
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_complaints():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints ORDER BY id")
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    cursor.close()
    conn.close()
    return _to_dataframe(rows, columns)


def update_status(index, status, resolution=""):
    df = get_all_complaints()
    if index < 0 or index >= len(df):
        return False

    complaint_id = int(df.iloc[index]["ID"])
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE complaints SET status = %s, resolution = %s WHERE id = %s",
        (status, resolution, complaint_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return updated
