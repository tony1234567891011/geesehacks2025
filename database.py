import streamlit as st
import psycopg2
# PostgreSQL Database Connection
DATABASE_URL = "postgresql://postgres:BlockedIn4Ever%21@db.lxkfxndaabhtrpvazszt.supabase.co:5432/postgres"

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
    
def add_block(user_id, block_color):
    """Add a block to the user's tower."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Retrieve the current tower colors
        cur.execute("SELECT colors FROM towers WHERE user_id = %s;", (user_id,))
        result = cur.fetchone()
        
        if not result:
            raise ValueError(f"Tower for user_id {user_id} does not exist.")
        
        current_colours = result[0] or ""  # Default to an empty string if colours is NULL

        # Append the new block color
        new_colours = current_colours + block_color
        cur.execute("UPDATE towers SET colors = %s WHERE user_id = %s;", (new_colours, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_tower(user_id):
    """Retrieve the tower's colors for a user."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT colors FROM towers WHERE user_id = %s;", (user_id,))
        result = cur.fetchone()
        if not result:
            raise ValueError(f"Tower for user_id {user_id} does not exist.")
        return result[0] or ""  # Return an empty string if colours is NULL
    finally:
        cur.close()
        conn.close()

def set_tower(user_id, new_colours):
    """Set a new tower for the user."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Check if the tower exists
        cur.execute("SELECT id FROM towers WHERE user_id = %s;", (user_id,))
        result = cur.fetchone()

        if result:
            # Update existing tower
            cur.execute("UPDATE towers SET colors = %s WHERE user_id = %s;", (new_colours, user_id))
        else:
            # Create a new tower if one doesn't exist
            cur.execute("INSERT INTO towers (user_id, colors) VALUES (%s, %s);", (user_id, new_colours))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def remove_blocks(user_id, number_of_blocks):
    """Remove a specified number of blocks from the end of the user's tower."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Retrieve the current tower colors
        cur.execute("SELECT colors FROM towers WHERE user_id = %s;", (user_id,))
        result = cur.fetchone()
        
        if not result:
            raise ValueError(f"Tower for user_id {user_id} does not exist.")
        
        current_colours = result[0] or ""  # Default to an empty string if colours is NULL

        # Ensure the number of blocks to remove is not greater than the tower length
        if number_of_blocks > len(current_colours):
            raise ValueError(f"Cannot remove {number_of_blocks} blocks. Tower only has {len(current_colours)} blocks.")
        
        # Remove the specified number of blocks from the tail
        new_colours = current_colours[:-number_of_blocks]

        # Update the tower in the database
        cur.execute("UPDATE towers SET colors = %s WHERE user_id = %s;", (new_colours, user_id))
        conn.commit()

        return new_colours  # Return the updated tower string for confirmation
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
