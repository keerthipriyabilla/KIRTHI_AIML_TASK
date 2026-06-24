import sqlite3

def create_table():

    conn = sqlite3.connect(
        "patients.db"
    )

    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        dob TEXT,
        email TEXT,
        glucose REAL,
        haemoglobin REAL,
        cholesterol REAL,
        remarks TEXT
    )
    ''')

    conn.commit()
    conn.close()


def add_patient(data):

    conn = sqlite3.connect(
        "patients.db"
    )

    cur = conn.cursor()

    cur.execute('''
    INSERT INTO patients(
        fullname,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        remarks
    )
    VALUES(?,?,?,?,?,?,?)
    ''',data)

    conn.commit()
    conn.close()


def get_patients():

    conn = sqlite3.connect(
        "patients.db"
    )

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM patients"
    )

    rows = cur.fetchall()

    conn.close()

    return rows


def update_patient(data):

    conn = sqlite3.connect(
        "patients.db"
    )

    cur = conn.cursor()

    cur.execute('''
    UPDATE patients
    SET
        fullname=?,
        dob=?,
        email=?,
        glucose=?,
        haemoglobin=?,
        cholesterol=?,
        remarks=?
    WHERE id=?
    ''',data)

    conn.commit()
    conn.close()


def delete_patient(pid):

    conn = sqlite3.connect(
        "patients.db"
    )

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM patients WHERE id=?",
        (pid,)
    )

    conn.commit()
    conn.close()