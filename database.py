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
    priority VARCHAR(50),
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
    priority TEXT,
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

    # update old tables automatically
    for alter_sql in [
        """
        ALTER TABLE complaints
        ADD COLUMN department VARCHAR(255)
        """,
        """
        ALTER TABLE complaints
        ADD COLUMN ai_status VARCHAR(100)
        """,
        """
        ALTER TABLE complaints
        ADD COLUMN progress_percentage INT
        """,
        """
        ALTER TABLE complaints
        ADD COLUMN estimated_completion VARCHAR(50)
        """,
        """
        ALTER TABLE complaints
        ADD COLUMN ai_updates TEXT
        """,
        """
        ALTER TABLE complaints
        ADD COLUMN admin_solution TEXT
        """,
        """
        ALTER TABLE complaints
        ADD COLUMN final_ai_report TEXT
        """,
        """
        ALTER TABLE complaints
        ADD COLUMN resolution_files TEXT
        """,
        """
        ALTER TABLE complaints
        ADD COLUMN department TEXT
        """,
        """
        ALTER TABLE complaints
        ADD COLUMN priority TEXT
        """,
    ]:
        try:
            cursor.execute(alter_sql)
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
        department,
        priority,
        description,
        image,
        time,
        status,
        ai_status,
        progress_percentage,
        estimated_completion,
        ai_updates,
        admin_solution,
        final_ai_report,
        resolution,
        resolution_files
        )
        VALUES
        ({params})
        """.format(params=PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE + "," + PARAM_STYLE),
        (
            data["Name"],
            data["Phone"],
            data["Issue"],
            data["Location"],
            data.get("Department", "") ,
            data.get("Priority", "Medium"),
            data["Description"],
            data["Image"],
            data["Time"],
            data["Status"],
            data.get("AI Status", "Complaint received and analyzed"),
            data.get("Progress", 0),
            data.get("Estimated Completion", ""),
            data.get("AI Updates", ""),
            data.get("Admin Solution", ""),
            data.get("Final AI Report", ""),
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
            "department": "Department",
            "priority": "Priority",
            "description": "Description",
            "image": "Image",
            "time": "Time",
            "status": "Status",
            "ai_status": "AI Status",
            "progress_percentage": "Progress",
            "estimated_completion": "Estimated Completion",
            "ai_updates": "AI Updates",
            "admin_solution": "Admin Solution",
            "final_ai_report": "Final AI Report",
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
    status=None,
    resolution=None,
    resolution_files=None,
    ai_status=None,
    progress_percentage=None,
    estimated_completion=None,
    ai_updates=None,
    admin_solution=None,
    final_ai_report=None,
):

    df = get_all_complaints()

    if index >= len(df):
        return False

    complaint_id = int(df.iloc[index]["ID"])

    updates = []
    params = []

    def add_update(column, value):
        if value is not None:
            updates.append(f"{column}={PARAM_STYLE}")
            params.append(value)

    add_update("status", status)
    add_update("resolution", resolution)
    add_update("resolution_files", resolution_files)
    add_update("ai_status", ai_status)
    add_update("progress_percentage", progress_percentage)
    add_update("estimated_completion", estimated_completion)
    add_update("ai_updates", ai_updates)
    add_update("admin_solution", admin_solution)
    add_update("final_ai_report", final_ai_report)

    if not updates:
        return False

    sql = f"UPDATE complaints SET {', '.join(updates)} WHERE id={PARAM_STYLE}"
    params.append(complaint_id)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, tuple(params))
    conn.commit()
    cursor.close()
    conn.close()

    return True
