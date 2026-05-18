from database.db import get_connection


def get_occupied_seat_ids(tour_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bus_seat_id
        FROM application
        WHERE tour_id = %s
          AND bus_seat_id IS NOT NULL
    """, (tour_id,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [row[0] for row in rows]


def create_application(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO application (
            client_id,
            tour_id,
            bus_seat_id,
            total_price,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["client_id"],
        data["tour_id"],
        data["bus_seat_id"],
        data["total_price"],
        data["status"]
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_applications():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            a.id_application,
            a.created_at,
            a.status,
            a.total_price,
            c.full_name,
            c.phone,
            c.email,
            t.tour_name,
            bs.seat_number
        FROM application a
        JOIN client c ON a.client_id = c.id_client
        JOIN tour t ON a.tour_id = t.id_tour
        LEFT JOIN bus_seat bs ON a.bus_seat_id = bs.id_bus_seat
        ORDER BY a.id_application DESC
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_application_by_id(application_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            a.id_application,
            a.created_at,
            a.status,
            a.total_price,

            c.id_client,
            c.full_name,
            c.phone,
            c.email,

            t.id_tour,
            t.tour_name,
            t.start_date,
            t.end_date,
            t.price,

            co.country_name,
            r.rest_type_name,
            m.meal_type_name,
            h.hotel_level_name,
            p.package_type_name,

            b.bus_number,
            bs.seat_number
        FROM application a
        JOIN client c ON a.client_id = c.id_client
        JOIN tour t ON a.tour_id = t.id_tour
        JOIN country co ON t.country_id = co.id_country
        JOIN rest_type r ON t.rest_type_id = r.id_rest_type
        JOIN meal_type m ON t.meal_type_id = m.id_meal_type
        JOIN hotel_level h ON t.hotel_level_id = h.id_hotel_level
        JOIN package_type p ON t.package_type_id = p.id_package_type
        LEFT JOIN bus_seat bs ON a.bus_seat_id = bs.id_bus_seat
        LEFT JOIN bus b ON bs.bus_id = b.id_bus
        WHERE a.id_application = %s
    """, (application_id,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def update_application_status(application_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE application
        SET status = %s
        WHERE id_application = %s
    """, (status, application_id))

    conn.commit()
    cursor.close()
    conn.close()