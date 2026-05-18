from database.db import get_connection


def get_tour_bus_info(tour_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            t.id_tour,
            t.tour_name,
            t.price,
            t.bus_id,
            b.bus_number,
            b.seats_count
        FROM tour t
        LEFT JOIN bus b ON t.bus_id = b.id_bus
        WHERE t.id_tour = %s
    """, (tour_id,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_bus_seats_by_tour(tour_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            bs.id_bus_seat,
            bs.bus_id,
            bs.seat_number
        FROM tour t
        JOIN bus_seat bs ON t.bus_id = bs.bus_id
        WHERE t.id_tour = %s
        ORDER BY CAST(bs.seat_number AS UNSIGNED), bs.seat_number
    """, (tour_id,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows