import os
import streamlit as st
import mysql.connector
import pandas as pd
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


def get_connection():

    return mysql.connector.connect(
        host=st.secrets.get(
            "DB_HOST",
            os.getenv("DB_HOST"),
        ),
        port=int(
            st.secrets.get(
                "DB_PORT",
                os.getenv("DB_PORT", 3306),
            )
        ),
        user=st.secrets.get(
            "DB_USER",
            os.getenv("DB_USER"),
        ),
        password=st.secrets.get(
            "DB_PASSWORD",
            os.getenv("DB_PASSWORD"),
        ),
        database=st.secrets.get(
            "DB_NAME",
            os.getenv("DB_NAME"),
        ),
        ssl_disabled=False,
    )

def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(CREATE_TABLE_SQL)

    # update old tables automatically

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


def add_complaint(data):

    init_db()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO complaints
        (
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
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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

    columns = [col[0] for col in cursor.description]

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

    cursor.close()

    conn.close()

    return df


def update_status(
    index,
    status,
    resolution,
    resolution_files="",
):

    df = get_all_complaints()

    if index >= len(df):
        return False

    complaint_id = int(df.iloc[index]["ID"])

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
