import streamlit as st
import psycopg2
# PostgreSQL Database Connection
DATABASE_URL = "postgresql://postgres.lxkfxndaabhtrpvazszt:BlockedIn4Ever!@aws-0-ca-central-1.pooler.supabase.com:6543/postgres"

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

def add_friend(user_id, friend_id):
    """Add a friend to the database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if both users exist
        cur.execute("SELECT COUNT(*) FROM users WHERE id IN (%s, %s);", (user_id, friend_id))
        if cur.fetchone()[0] != 2:
            raise ValueError("One or both user IDs do not exist.")
        
        # Add friendship in both directions
        cur.execute("""
            INSERT INTO friends (user_id, friend_id)
            VALUES (%s, %s), (%s, %s) ON CONFLICT DO NOTHING;
        """, (user_id, friend_id, friend_id, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
        return None
    
def check_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id, password_hash FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()

    if user and user[1] == password :  # Тут краще використовувати хешування
        return user[0]  # Повертаємо user_id
    else:
        raise ValueError("Incorrect Password")
    return None


def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = "SELECT id, username FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        
        # Check if the user exists
        if user is None:
            raise ValueError(f"User with id {user_id} does not exist.")
        
        # Format the result as a dictionary
        user_data = {
            "id": user[0],
            "username": user[1]
        }
        
        return user_data
    except Exception as e:
        raise e
    finally:
        cur.close()
        conn.close()
        