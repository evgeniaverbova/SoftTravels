from database.db import get_connection


def get_clients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_client,
            full_name,
            phone,
            email
        FROM client
        ORDER BY id_client DESC
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def create_client(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO client (
            full_name,
            phone,
            email,
            password_hash
        )
        VALUES (%s, %s, %s, %s)
    """, (
        data["full_name"],
        data["phone"],
        data["email"],
        data["password_hash"]
    ))

    conn.commit()
    cursor.close()
    conn.close()