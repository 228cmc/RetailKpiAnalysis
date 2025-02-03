import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv


# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# Read variables from .env
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "127.0.0.1"
DB_PORT = "5433"


def connect_db():
    """Establish connection to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f" Error connecting to the database: {e}")
        return None

def execute_query(query):
    """Execute an SQL query"""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            print(" Query executed successfully.")
        except Exception as e:
            print(f" Error executing query: {e}")
        finally:
            conn.close()

def insert_data_from_csv(file_path, table_name):
    """
    Inserts data from a CSV file into a PostgreSQL table.
    Args:
        file_path (str): Path to the CSV file.
        table_name (str): Name of the PostgreSQL table.
    """
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            df = pd.read_csv(file_path)

            # Ensure correct column order
            df = df[['date', 'company', 'total_sales', 'web_traffic', 
                     'ad_spend', 'customer_reviews', 'social_media_mentions']]

            # Insert DataFrame into PostgreSQL
            for _, row in df.iterrows():
                cursor.execute(f"""
                    INSERT INTO {table_name} (sale_date, company_name, total_sales, web_traffic, 
                                              advertising_spend, customer_review_score, social_media_mentions)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, tuple(row))

            conn.commit()
            print(f" Data successfully inserted into table '{table_name}'.")
        except Exception as e:
            print(f" Error inserting data: {e}")
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # Create tables from SQL script
    sql_file_path = os.path.join(os.path.dirname(__file__), "..", "sql", "create_tables.sql")

    try:
        with open(sql_file_path, "r") as f:
            execute_query(f.read())
        print(" Tables created successfully.")
    except Exception as e:
        print(f" Error reading SQL file: {e}")
