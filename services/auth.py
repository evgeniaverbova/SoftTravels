from database.db import get_connection

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            u.id_user,
            u.full_name,
            u.username,
            u.password_hash,
            r.role_name
        FROM users u
        JOIN roles r ON u.role_id = r.id_role
        WHERE u.username = %s AND u.password_hash = %s
    """, (username, password))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user