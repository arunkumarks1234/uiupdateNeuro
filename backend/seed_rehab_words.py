import sqlite3
import json
from datetime import datetime, timedelta

DB_PATH = "patient_logs.db"

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Add extended clinical vocabulary words
    words = [
        "hello", "water", "breakfast", "hospital", 
        "medicine", "family", "emergency", "television"
    ]
    
    # Assuming clinician1 has ID 2
    for w in words:
        try:
            cursor.execute("INSERT INTO custom_words (word, added_by) VALUES (?, ?)", (w, 2))
        except sqlite3.IntegrityError:
            pass # Word already exists in DB
            
    # 2. Add fake historical assessments for patient1 (id: 1)
    # Simulating a recovery trend: Severe -> Moderate -> Moderate -> Mild -> Normal
    trend = [
        ("Severe", 0.8, {"f0_mean": 90, "f0_std": 20, "spectral_centroid": 1200, "zcr": 0.04}),
        ("Moderate", 1.2, {"f0_mean": 110, "f0_std": 15, "spectral_centroid": 1400, "zcr": 0.05}),
        ("Moderate", 1.5, {"f0_mean": 115, "f0_std": 12, "spectral_centroid": 1450, "zcr": 0.055}),
        ("Mild", 1.8, {"f0_mean": 130, "f0_std": 8, "spectral_centroid": 1600, "zcr": 0.07}),
        ("Normal", 2.2, {"f0_mean": 140, "f0_std": 5, "spectral_centroid": 1800, "zcr": 0.09}),
    ]
    
    # Only insert fake data if patient1 has no assessments yet
    cursor.execute("SELECT COUNT(*) FROM assessments WHERE patient_id = 1")
    if cursor.fetchone()[0] == 0:
        base_time = datetime.now() - timedelta(days=10) # Start 10 days ago
        for i, (sev, dur, metrics) in enumerate(trend):
            t = base_time + timedelta(days=i*2) # 1 session every 2 days
            cursor.execute(
                "INSERT INTO assessments (patient_id, severity, final_text, duration, metrics, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (1, sev, "this is a simulated historical transcript", dur, json.dumps(metrics), t.strftime("%Y-%m-%d %H:%M:%S"))
            )
            
    conn.commit()
    conn.close()
    print("✅ Database successfully seeded with baseline rehab words and historical acoustic trends!")

if __name__ == "__main__":
    seed_data()
