# backend/setup_database.py
import json
import mysql.connector
from mysql.connector import Error

def setup_mysql_database():
    """
    Sets up MySQL database and populates it with sample data.
    """
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",       # change if needed
            user="root",            # your MySQL username
            password="your_password", # your MySQL password
            database="internship_db"  # will create if not exists
        )

        cursor = connection.cursor()


    except Error as e:
        print(f"An error occurred during MySQL setup: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == '__main__':
    print("Starting MySQL setup...")
    setup_mysql_database()
    print("MySQL setup complete.")
