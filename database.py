import os
import sqlite3

try:
    import mysql.connector
except ModuleNotFoundError:
    mysql = None

import pandas as pd

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*args, **kwargs):
        return False


load_dotenv()

USE_SQLITE = os.getenv("DB_USE_SQLITE", "true").lower() in (
    "1",
    "true",
    "yes",
)

MYSQL_CREATE_TABLE_SQL = """
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

SQLITE_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS complaints(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    issue TEXT,
    location TEXT,
    description TEXT,
    image TEXT,
    time TEXT,
    status TEXT,
    resolution TEXT,
    resolution_files TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

PARAM_STYLE = "%s"

if USE_SQLITE or mysql is None:
    PARAM_STYLE = "?"


def get_connection():

    if USE_SQLITE or mysql is None:
        db_path = os.getenv(
            "SQLITE_DB_PATH",
            "./water_tracker.db",
        )
        return sqlite3.connect(db_path)

    return mysql.connector.connect(
        host=os.getenv(
            "DB_HOST",
            "localhost",
        ),
        user=os.getenv(
            "DB_USER",
            "root",
        ),
        password=os.getenv(
            "DB_PASSWORD",
            "root@123",
        ),
        database=os.getenv(
            "DB_NAME",
            "water_tracker",
        ),
    )


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    create_sql = SQLITE_CREATE_TABLE_SQL if USE_SQLITE or mysql is None else MYSQL_CREATE_TABLE_SQL

    cursor.execute(create_sql)

    if not USE_SQLITE and mysql is not None:
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
        ({params})
        """.format(params=PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE),
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
        status={p},
        resolution={p},
        resolution_files={p}
        WHERE id={p}
        """.format(p=PARAM_STYLE),
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
