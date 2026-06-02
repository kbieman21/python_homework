# Task 1: Create a New SQLite Database
# Task 2: Define Database Structure

import os
import sqlite3

# Define the database path
db_path = '../db/magazines.db'


os.makedirs(os.path.dirname(db_path), exist_ok=True)


# Task 3: Populate Tables with Data

# Insert functions for all tables with no duplicates
def insert_publisher(cursor, name):
    try:
        # check if publisher name already exists, if not insert and return id, else return existing id
        cursor.execute("SELECT id FROM publishers WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"Publisher '{name}' already exists. Skipping.")
            return
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        print(f"Publisher '{name}' added successfully.")
    except sqlite3.Error:
        print(f"Error inserting publisher '{name}' into the database.")

def insert_magazine(cursor, title, publisher_name):
    try:
        # Get the publisher's ID based on their name
        cursor.execute(
            "SELECT id FROM publishers WHERE name = ?", (publisher_name,)
        )
        pub_row = cursor.fetchone()

        if not pub_row:
            print(
                f"Cannot add magazine '{title}': Publisher '{publisher_name}' not found."
            )
            return

        pub_id = pub_row[0]

        # Check if magazine title already exists
        cursor.execute("SELECT id FROM magazines WHERE title = ?", (title,))
        if cursor.fetchone():
            print(f"Magazine '{title}' already exists. Skipping.")
            return

        cursor.execute(
            "INSERT INTO magazines (title, publisher_id) VALUES (?, ?)",
            (title, pub_id),
        )
        print(f"Magazine '{title}' added successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting magazine '{title}': {e}")


def insert_subscriber(cursor, name, address):
    try:
        # Check if subscriber already exists based on name and address
        cursor.execute(
            "SELECT id FROM subscribers WHERE name = ? AND address = ?", (name, address)
        )
        if cursor.fetchone():
            print(f"Subscriber '{name}' at '{address}' already exists. Skipping.")
            return

        cursor.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address)
        )
        print(f"Subscriber '{name}' added successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting subscriber '{name}': {e}")


def insert_subscription(cursor, subscriber_name, magazine_title, expiration_date):
    try:
        # Get subscriber ID
        cursor.execute(
            "SELECT id FROM subscribers WHERE name = ?", (subscriber_name,)
        )
        sub_row = cursor.fetchone()
        if not sub_row:
            print(
                f"Cannot add subscription: Subscriber '{subscriber_name}' not found."
            )
            return
        subscriber_id = sub_row[0]

        # Get magazine ID
        cursor.execute("SELECT id FROM magazines WHERE title = ?", (magazine_title,))
        mag_row = cursor.fetchone()
        if not mag_row:
            print(f"Cannot add subscription: Magazine '{magazine_title}' not found.")
            return
        magazine_id = mag_row[0]

        # Check for existing subscription to the same magazine by the same subscriber
        cursor.execute(
            "SELECT id FROM subscriptions WHERE subscriber_id = ? AND magazine_id = ?",
            (subscriber_id, magazine_id),
        )
        if cursor.fetchone():
            print(
                f"Subscription already exists for subscriber '{subscriber_name}' to magazine '{magazine_title}'. Skipping."
            )
            return

        cursor.execute(
            "INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)",
            (subscriber_id, magazine_id, expiration_date),
        )
        print(
            f"Subscription for '{subscriber_name}' to '{magazine_title}' added successfully."
        )
    except sqlite3.Error as e:
        print(f"Error inserting subscription for '{subscriber_name}': {e}")

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    #cursor = conn.cursor()
    print(f"Successfully connected to the database at {db_path}")


    # Enforce Foreign Key constraints in SQLite (it was Off by default) USE ONE OF THE BELOW LINES OF CODE
    conn.execute("PRAGMA foreign_keys = 1")
    #cursor.execute("PRAGMA foreign_keys = ON;")


    cursor = conn.cursor()

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

    print("\n--- Populating Data ---")

     # 1. Populate Publishers (3 entries)
    insert_publisher(cursor, "Condé Nast")
    insert_publisher(cursor, "Hearst Communications")
    insert_publisher(cursor, "Dotdash Meredith")

    # 2. Populate Magazines (3 entries linked to publishers)
    insert_magazine(cursor, "Vogue", "Condé Nast")
    insert_magazine(cursor, "Cosmopolitan", "Hearst Communications")
    insert_magazine(cursor, "Better Homes & Gardens", "Dotdash Meredith")

    # 3. Populate Subscribers (3 entries)
    insert_subscriber(cursor, "Alice Smith", "123 Maple St")
    insert_subscriber(cursor, "Bob Jones", "456 Oak Ave")
    insert_subscriber(cursor, "Alice Smith", "789 Pine Rd")  # Same name, different address allowed!

    # 4. Populate Subscriptions (3 entries)
    insert_subscription(cursor, "Alice Smith", "Vogue", "2027-12-31")
    insert_subscription(cursor, "Bob Jones", "Cosmopolitan", "2026-08-15")
    insert_subscription(
        cursor, "Alice Smith", "Better Homes & Gardens", "2028-01-01"
    )
    conn.commit()
    print("Tables created successfully and data populated successfully.")


    # Task 4: Write SQL Queries

    # Retrieve all information from the subscribers table
    cursor.execute("SELECT * FROM subscribers")
    subscribers = cursor.fetchall()
    print("\n--- All Subscribers ---")
    for subscriber in subscribers:
        print(subscriber)   


    # Retrieve all magazines sorted by name
    cursor.execute("SELECT * FROM magazines ORDER BY title")
    magazines = cursor.fetchall()
    print("\n--- All Magazines ---")
    for magazine in magazines:
        print(magazine)   


    # Find magazines for a particular publisher using a JOIN
    cursor.execute("SELECT magazines.id, magazines.title, publishers.name FROM magazines JOIN publishers ON magazines.publisher_id = publishers.id WHERE publishers.name = ?", ("Condé Nast",))
    publisher_mags = cursor.fetchall()
    print("\n--- Magazines Published by Condé Nast ---")
    for mag in publisher_mags:
        print(mag)


except sqlite3.Error as e:
    # Catch and handle any SQL exceptions
    print(f"A database error occurred: {e}")

finally:
    # Explicitly close the connection as requested
    if 'conn' in locals():
        conn.close()
        print("Database connection closed.")




