import psycopg2
import streamlit as st

# PostgreSQL Database Connection
DATABASE_URL = "postgresql://postgres.lxkfxndaabhtrpvazszt:BlockedIn4Ever%21@aws-0-ca-central-1.pooler.supabase.com:6543/postgres"

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(DATABASE_URL)

def create_user(username, email, password_hash):
    """Insert a new user into the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s) RETURNING id;
    """, (username, email, password_hash))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

