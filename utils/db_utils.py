import sqlite3
from datetime import datetime
import pandas as pd

DB_NAME = "evaluations.db"

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table():
    """Create the evaluations table if it doesn't exist."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT NOT NULL,
                resume_filename TEXT NOT NULL,
                relevance_score INTEGER NOT NULL,
                verdict TEXT NOT NULL,
                missing_skills TEXT,
                feedback TEXT,
                evaluation_date TIMESTAMP NOT NULL
            );
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

def save_evaluation(job_title, filename, score, verdict, missing, feedback):
    """Save a new evaluation record to the database."""
    conn = create_connection()
    if conn is not None:
        try:
            sql = ''' INSERT INTO evaluations(job_title, resume_filename, relevance_score, verdict, missing_skills, feedback, evaluation_date)
                      VALUES(?,?,?,?,?,?,?) '''
            cursor = conn.cursor()
            
            # Convert list of missing skills to a comma-separated string
            missing_skills_str = ", ".join(missing)

            cursor.execute(sql, (job_title, filename, score, verdict, missing_skills_str, feedback, datetime.now()))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving evaluation: {e}")
        finally:
            conn.close()

def get_all_evaluations():
    """Fetch all evaluations from the database and return as a DataFrame."""
    conn = create_connection()
    if conn is not None:
        try:
            df = pd.read_sql_query("SELECT * FROM evaluations", conn)
            return df
        except Exception as e:
            print(f"Error fetching evaluations: {e}")
            return pd.DataFrame() # Return empty dataframe on error
        finally:
            conn.close()