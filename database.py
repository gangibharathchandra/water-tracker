import os

import mysql.connector
import pandas as pd
import streamlit as st
from dotenv import load_dotenv


load_dotenv()


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS complaints(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(20),
    issue VARCHAR(100),
    location VARCHAR(255),
    description TEXT,
    image TEXT,
    time VARCHAR(100),
    status VARCHAR(50),
    resolution TEXT,
    resolution_files TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


# ---------------- SECRET HANDLER ----------------
# Local system  -> .env
# Streamlit app -> Secrets


def get_secret(key, default=None):
    try:
        return st.secrets[key]

    except Exception:
        return os.getenv(
            key,
            default,
        )


# ---------------- DATABASE CONNECTION ----------------


def get_connection():
    return mysql.connector.connect(
        host=get_secret(
            "DB_HOST",
            "localhost",
        ),
        port=int(
            get_secret(
                "DB_PORT",
                3306,
            )
        ),
        user=get_secret(
            "DB_USER",
            "root",
        ),
        password=get_secret(
            "DB_PASSWORD",
            "",
        ),
        database=get_secret(
            "DB_NAME",
            "water_tracker",
        ),
        ssl_verify_identity=False,
        ssl_verify_cert=False,
    )


# ---------------- INITIALIZE DATABASE ----------------


def init_db():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        CREATE_TABLE_SQL
    )

    try:
        cursor.execute(
            """
            ALTER TABLE complaints
            ADD COLUMN resolution_files TEXT
            """
        )

    except Exception:
        pass

    conn.commit()

    cursor.close()

    conn.close()


# ---------------- ADD COMPLAINT ----------------


def add_complaint(data):
    init_db()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO complaints(
            name,
            phone,
            issue,
            location,
            description,
            image,
            time,
            status,
            resolution,
            resolution_files
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
            "",
            "",
        ),
    )

    conn.commit()

    cursor.close()

    conn.close()


# ---------------- FETCH COMPLAINTS ----------------


def get_all_complaints():
    init_db()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM complaints
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    columns = [
        col[0]
        for col in cursor.description
    ]

    cursor.close()

    conn.close()

    df = pd.DataFrame(
        rows,
        columns=columns,
    )

    df.rename(
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
            "resolution_files": "Resolution Files",
        },
        inplace=True,
    )

    return df


# ---------------- UPDATE STATUS ----------------


def update_status(
    index,
    status,
    resolution,
    resolution_files="",
):

    df = get_all_complaints()

    if (
        index < 0
        or index >= len(df)
    ):
        return False

    complaint_id = int(
        df.iloc[index]["ID"]
    )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE complaints
        SET
            status=%s,
            resolution=%s,
            resolution_files=%s
        WHERE id=%s
        """,
        (
            status,
            resolution,
            resolution_files,
            complaint_id,
        ),
    )

    conn.commit()

    cursor.close()

    conn.close()

    return True