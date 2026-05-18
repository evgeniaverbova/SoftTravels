from database.db import get_connection


def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tour")
    tours_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM client")
    clients_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM application")
    applications_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "tours_count": tours_count,
        "clients_count": clients_count,
        "applications_count": applications_count
    }