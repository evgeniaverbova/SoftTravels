from database.db import get_connection


def get_countries():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_country, country_name FROM country ORDER BY country_name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_rest_types():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_rest_type, rest_type_name FROM rest_type ORDER BY rest_type_name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_meal_types():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_meal_type, meal_type_name FROM meal_type ORDER BY meal_type_name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_hotel_levels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_hotel_level, hotel_level_name FROM hotel_level ORDER BY hotel_level_name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_package_types():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_package_type, package_type_name FROM package_type ORDER BY package_type_name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_buses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_bus, bus_number FROM bus ORDER BY bus_number")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows