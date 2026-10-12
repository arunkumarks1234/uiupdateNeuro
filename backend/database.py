import sqlite3
import json
from datetime import datetime
import os

DB_PATH = "patient_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table (Patients and Clinicians)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT -- 'patient' or 'clinician'
        )
    ''')
    
    # Assessments/Analyses table (Progress Tracking)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            severity TEXT,
            final_text TEXT,
            duration REAL,
            metrics TEXT, -- JSON string
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES users (id)
        )
    ''')
    
    # Custom Words / Rehab table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS custom_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            added_by INTEGER,
            FOREIGN KEY (added_by) REFERENCES users (id)
        )
    ''')

    # Rehab Progress table (Patient mastery of specific words)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rehab_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            word_id INTEGER,
            score INTEGER, -- e.g., 0-100 or 1-4 scale
            attempts INTEGER DEFAULT 1,
            last_practiced DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES users (id),
            FOREIGN KEY (word_id) REFERENCES custom_words (id),
            UNIQUE(patient_id, word_id)
        )
    ''')
    
    # Insert default users if none exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("patient1", "pass123", "patient"))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("clinician1", "admin123", "clinician"))
        
        # Add a default rehab words
        cursor.execute("INSERT INTO custom_words (word, added_by) VALUES (?, ?)", ("hello", 2))
        cursor.execute("INSERT INTO custom_words (word, added_by) VALUES (?, ?)", ("water", 2))
        cursor.execute("INSERT INTO custom_words (word, added_by) VALUES (?, ?)", ("breakfast", 2))

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB on import
init_db()
