import sqlite3


def setup_database():
    conn = sqlite3.connect("agentReg.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS counter_table (
        id INTEGER PRIMARY KEY,
        counter INTEGER NOT NULL
    )
    """
    )
    cursor.execute("SELECT COUNT(*) FROM counter_table")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO counter_table (counter) VALUES (1)")
        conn.commit()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS audit_table (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        counter INTEGER,
        otp TEXT
    )
    """
    )
    conn.close()


def setup_database_broker():
    conn = sqlite3.connect("brokerReg.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS counter_table (
        id INTEGER PRIMARY KEY,
        counter INTEGER NOT NULL
    )
    """
    )
    cursor.execute("SELECT COUNT(*) FROM counter_table")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO counter_table (counter) VALUES (1)")
        conn.commit()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS audit_table (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        counter INTEGER,
        otp TEXT
    )
    """
    )
    conn.close()
