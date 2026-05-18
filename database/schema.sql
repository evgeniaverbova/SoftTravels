CREATE DATABASE IF NOT EXISTS travel_agency_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE travel_agency_db;

DROP TABLE IF EXISTS application;
DROP TABLE IF EXISTS tour;
DROP TABLE IF EXISTS bus_seat;
DROP TABLE IF EXISTS bus;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS rest_type;
DROP TABLE IF EXISTS meal_type;
DROP TABLE IF EXISTS hotel_level;
DROP TABLE IF EXISTS package_type;

CREATE TABLE roles (
    id_role INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id_role)
);

CREATE TABLE client (
    id_client INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE country (
    id_country INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE rest_type (
    id_rest_type INT AUTO_INCREMENT PRIMARY KEY,
    rest_type_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE meal_type (
    id_meal_type INT AUTO_INCREMENT PRIMARY KEY,
    meal_type_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE hotel_level (
    id_hotel_level INT AUTO_INCREMENT PRIMARY KEY,
    hotel_level_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE package_type (
    id_package_type INT AUTO_INCREMENT PRIMARY KEY,
    package_type_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE bus (
    id_bus INT AUTO_INCREMENT PRIMARY KEY,
    bus_number VARCHAR(50) NOT NULL UNIQUE,
    seats_count INT NOT NULL
);

CREATE TABLE bus_seat (
    id_bus_seat INT AUTO_INCREMENT PRIMARY KEY,
    bus_id INT NOT NULL,
    seat_number VARCHAR(20) NOT NULL,
    FOREIGN KEY (bus_id) REFERENCES bus(id_bus) ON DELETE CASCADE,
    UNIQUE (bus_id, seat_number)
);

CREATE TABLE tour (
    id_tour INT AUTO_INCREMENT PRIMARY KEY,
    tour_name VARCHAR(255) NOT NULL,
    country_id INT NOT NULL,
    rest_type_id INT NOT NULL,
    meal_type_id INT NOT NULL,
    hotel_level_id INT NOT NULL,
    package_type_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    bus_id INT,
    image_path VARCHAR(500),
    FOREIGN KEY (country_id) REFERENCES country(id_country),
    FOREIGN KEY (rest_type_id) REFERENCES rest_type(id_rest_type),
    FOREIGN KEY (meal_type_id) REFERENCES meal_type(id_meal_type),
    FOREIGN KEY (hotel_level_id) REFERENCES hotel_level(id_hotel_level),
    FOREIGN KEY (package_type_id) REFERENCES package_type(id_package_type),
    FOREIGN KEY (bus_id) REFERENCES bus(id_bus)
);

CREATE TABLE application (
    id_application INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    tour_id INT NOT NULL,
    bus_seat_id INT,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES client(id_client),
    FOREIGN KEY (tour_id) REFERENCES tour(id_tour),
    FOREIGN KEY (bus_seat_id) REFERENCES bus_seat(id_bus_seat)
);

INSERT INTO roles (role_name) VALUES ('admin') ON DUPLICATE KEY UPDATE role_name = role_name;
INSERT INTO users (full_name, username, password_hash, role_id)
SELECT 'Administrator', 'admin', 'admin', id_role FROM roles WHERE role_name = 'admin'
ON DUPLICATE KEY UPDATE username = username;

INSERT INTO country (country_name) VALUES ('Turkey'), ('Montenegro'), ('Ukraine')
ON DUPLICATE KEY UPDATE country_name = country_name;
INSERT INTO rest_type (rest_type_name) VALUES ('Sea'), ('Mountain'), ('Excursion')
ON DUPLICATE KEY UPDATE rest_type_name = rest_type_name;
INSERT INTO meal_type (meal_type_name) VALUES ('All inclusive'), ('Breakfast'), ('No meals')
ON DUPLICATE KEY UPDATE meal_type_name = meal_type_name;
INSERT INTO hotel_level (hotel_level_name) VALUES ('3 stars'), ('4 stars'), ('5 stars')
ON DUPLICATE KEY UPDATE hotel_level_name = hotel_level_name;
INSERT INTO package_type (package_type_name) VALUES ('Standard'), ('Comfort'), ('Premium')
ON DUPLICATE KEY UPDATE package_type_name = package_type_name;

INSERT INTO bus (bus_number, seats_count) VALUES ('BUS-001', 20)
ON DUPLICATE KEY UPDATE bus_number = bus_number;

INSERT INTO bus_seat (bus_id, seat_number)
SELECT b.id_bus, n.seat_number
FROM bus b
JOIN (
    SELECT '1' seat_number UNION SELECT '2' UNION SELECT '3' UNION SELECT '4' UNION SELECT '5'
    UNION SELECT '6' UNION SELECT '7' UNION SELECT '8' UNION SELECT '9' UNION SELECT '10'
    UNION SELECT '11' UNION SELECT '12' UNION SELECT '13' UNION SELECT '14' UNION SELECT '15'
    UNION SELECT '16' UNION SELECT '17' UNION SELECT '18' UNION SELECT '19' UNION SELECT '20'
) n
WHERE b.bus_number = 'BUS-001'
ON DUPLICATE KEY UPDATE seat_number = seat_number;
