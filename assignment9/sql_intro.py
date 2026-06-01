# Task 1: Create a New SQLite Database
# Task 2: Define Database Structure

import os
import sqlite3

# Define the database path
db_path = '../db/magazines.db'


os.makedirs(os.path.dirname(db_path), exist_ok=True)

try:
    # 1. Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"Successfully connected to the database at {db_path}")


    # Enforce Foreign Key constraints in SQLite (it was Off by default)
    cursor.execute("PRAGMA foreign_keys = ON;")


    # Create Publishers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publishers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # Create Magazines Table (One-to-Many with Publishers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(id)
        )
    ''')

    # Create Subscribers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')

    # Create Subscriptions Join Table (Many-to-Many)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )
    ''')
    conn.commit()
    print("Tables 'publishers', 'magazines', 'subscribers', and 'subscriptions' created successfully.")

except sqlite3.Error as e:
    # 3. Catch and handle any SQL exceptions
    print(f"A database error occurred: {e}")

finally:
    # 4. Explicitly close the connection as requested
    if 'conn' in locals():
        conn.close()
        print("Database connection closed.")



