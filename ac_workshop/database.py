import sqlite3
from contextlib import closing
import logging

DB_FILE = "ac_workshop.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    with closing(get_connection()) as conn, conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                phone TEXT,
                job_date TEXT,
                is_service INTEGER,
                is_repair INTEGER,
                service_by TEXT,
                repair_by TEXT,
                next_service_date TEXT,
                notes TEXT,
                job_type TEXT,
                plate TEXT,
                make TEXT,
                model TEXT,
                total_amount INTEGER
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("Fidel", "admin"))
    logging.info("Database initialized")

def validate_user(username, password):
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return c.fetchone()

def insert_job(job):
    """Accepts a Job dataclass."""
    with closing(get_connection()) as conn, conn:
        conn.execute('''
            INSERT INTO jobs (
                client_name, phone, job_date, is_service, is_repair,
                service_by, repair_by, next_service_date, notes, job_type,
                plate, make, model, total_amount
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job.client_name, job.phone, job.job_date, job.is_service, job.is_repair,
            job.service_by, job.repair_by, job.next_service_date, job.notes,
            job.job_type, job.plate, job.make, job.model, job.total_amount
        ))
    logging.info(f"Inserted job for {job.client_name}")

from datetime import datetime, timedelta

PERIODS = {
    "Week": 7,
    "Month": 30,
    "Three Months": 92,
    "Year": 365
}

def get_upcoming_services(filter_type="All", days="Week"):
    today = datetime.today()
    end_date = today + timedelta(days=PERIODS.get(days, 7))
    with closing(get_connection()) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT client_name, phone, job_type, next_service_date, plate, make, model
            FROM jobs
            WHERE next_service_date IS NOT NULL AND next_service_date != ''
        ''')
        rows = c.fetchall()
    
    print(rows)
    results = []
    for row in rows:
        try:
            ns_date = datetime.strptime(row[3], "%Y-%m-%d")
        except ValueError:
            continue
        if today <= ns_date <= end_date:
            if filter_type == "All" or row[2] == filter_type:
                results.append(row)
    return results
