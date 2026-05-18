from database.db import get_connection


def get_tours(filters=None):
    if filters is None:
        filters = {}

    query = """
        SELECT
            t.id_tour,
            t.tour_name,
            c.country_name,
            r.rest_type_name,
            t.start_date,
            t.end_date,
            t.price,
            t.image_path
        FROM tour t
        JOIN country c ON t.country_id = c.id_country
        JOIN rest_type r ON t.rest_type_id = r.id_rest_type
        JOIN meal_type m ON t.meal_type_id = m.id_meal_type
        JOIN hotel_level h ON t.hotel_level_id = h.id_hotel_level
        JOIN package_type p ON t.package_type_id = p.id_package_type
        WHERE 1=1
    """
    params = []

    if filters.get("country_id") is not None:
        query += " AND t.country_id = %s"
        params.append(filters["country_id"])

    if filters.get("rest_type_id") is not None:
        query += " AND t.rest_type_id = %s"
        params.append(filters["rest_type_id"])

    if filters.get("meal_type_id") is not None:
        query += " AND t.meal_type_id = %s"
        params.append(filters["meal_type_id"])

    if filters.get("hotel_level_id") is not None:
        query += " AND t.hotel_level_id = %s"
        params.append(filters["hotel_level_id"])

    if filters.get("package_type_id") is not None:
        query += " AND t.package_type_id = %s"
        params.append(filters["package_type_id"])

    query += " ORDER BY t.id_tour"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_tour_by_id(tour_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            t.id_tour,
            t.tour_name,
            c.country_name,
            r.rest_type_name,
            m.meal_type_name,
            h.hotel_level_name,
            p.package_type_name,
            t.start_date,
            t.end_date,
            t.price,
            b.bus_number,
            t.image_path
        FROM tour t
        JOIN country c ON t.country_id = c.id_country
        JOIN rest_type r ON t.rest_type_id = r.id_rest_type
        JOIN meal_type m ON t.meal_type_id = m.id_meal_type
        JOIN hotel_level h ON t.hotel_level_id = h.id_hotel_level
        JOIN package_type p ON t.package_type_id = p.id_package_type
        LEFT JOIN bus b ON t.bus_id = b.id_bus
        WHERE t.id_tour = %s
    """, (tour_id,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def create_tour(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tour (
            tour_name,
            country_id,
            rest_type_id,
            meal_type_id,
            hotel_level_id,
            package_type_id,
            start_date,
            end_date,
            price,
            bus_id,
            image_path
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["tour_name"],
        data["country_id"],
        data["rest_type_id"],
        data["meal_type_id"],
        data["hotel_level_id"],
        data["package_type_id"],
        data["start_date"],
        data["end_date"],
        data["price"],
        data["bus_id"],
        data["image_path"]
    ))

    conn.commit()
    cursor.close()
    conn.close()