-- ==============================================================================
-- Створення бази даних (ідемпотентний підхід)
-- ==============================================================================
CREATE DATABASE IF NOT EXISTS skyscanner_db;
USE skyscanner_db;

-- ==============================================================================
-- Видалення існуючих таблиць (з ігноруванням старих конфліктів)
-- ==============================================================================

DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS connected_flights;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS baggage_rules;
DROP TABLE IF EXISTS airlines;
DROP TABLE IF EXISTS airports;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS booking_statuses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS baggage_policies; -- Видаляємо ваш старий хвіст, який викликав помилку

SET FOREIGN_KEY_CHECKS = 1; -- Вмикаємо перевірку ключів назад

-- ==============================================================================
-- Створення таблиць (Нормалізація 3НФ, PRIMARY KEY, FOREIGN KEY, ENGINE=InnoDB)
-- ==============================================================================

-- 1. Таблиця країн
CREATE TABLE countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE = INNODB;

-- 2. Таблиця міст
CREATE TABLE cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT fk_cities_country FOREIGN KEY (country_id) REFERENCES countries (id) ON DELETE RESTRICT
) ENGINE = INNODB;

-- 3. Таблиця аеропортів (базові аеропорти)
CREATE TABLE airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    iata_code VARCHAR(3) NOT NULL UNIQUE, -- Вторинний ключ
    name VARCHAR(150) NOT NULL,
    CONSTRAINT fk_airports_city FOREIGN KEY (city_id) REFERENCES cities (id) ON DELETE RESTRICT
) ENGINE = INNODB;

-- 4. Таблиця авіакомпаній
CREATE TABLE airlines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    base_airport_id INT NOT NULL,
    contact_email VARCHAR(100),
    CONSTRAINT fk_airlines_airport FOREIGN KEY (base_airport_id) REFERENCES airports (id) ON DELETE RESTRICT
) ENGINE = INNODB;

-- 5. Таблиця правил багажу для кожної авіакомпанії
CREATE TABLE baggage_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airline_id INT NOT NULL,
    tier_name VARCHAR(50) NOT NULL,
    weight_limit_kg INT NOT NULL,
    CONSTRAINT fk_baggage_airline FOREIGN KEY (airline_id) REFERENCES airlines (id) ON DELETE CASCADE
) ENGINE = INNODB;

-- 6. Профіль користувача
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE, -- Вторинний ключ
    phone VARCHAR(20)
) ENGINE = INNODB;

-- 7. Статуси бронювань (довідник)
CREATE TABLE booking_statuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
) ENGINE = INNODB;

-- 8. Бронювання (Історія купівлі квитків користувачем)
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status_id INT NOT NULL,
    booking_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_bookings_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_bookings_status FOREIGN KEY (status_id) REFERENCES booking_statuses (id) ON DELETE RESTRICT
) ENGINE = INNODB;

-- 9. Таблиця авіарейсів
CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airline_id INT NOT NULL,
    dep_airport_id INT NOT NULL,
    arr_airport_id INT NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    base_price DECIMAL(10, 2) NOT NULL,
    baggage_rule_id INT NOT NULL,
    CONSTRAINT fk_flights_airline FOREIGN KEY (airline_id) REFERENCES airlines (id),
    CONSTRAINT fk_flights_dep_airport FOREIGN KEY (dep_airport_id) REFERENCES airports (id),
    CONSTRAINT fk_flights_arr_airport FOREIGN KEY (arr_airport_id) REFERENCES airports (id),
    CONSTRAINT fk_flights_baggage FOREIGN KEY (baggage_rule_id) REFERENCES baggage_rules (id)
) ENGINE = INNODB;

-- 10. Connected flights (Зв'язані рейси з пересадкою)
CREATE TABLE connected_flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_1_id INT NOT NULL,
    flight_2_id INT NOT NULL,
    layover_duration_mins INT NOT NULL,
    CONSTRAINT fk_conn_flight1 FOREIGN KEY (flight_1_id) REFERENCES flights (id) ON DELETE CASCADE,
    CONSTRAINT fk_conn_flight2 FOREIGN KEY (flight_2_id) REFERENCES flights (id) ON DELETE CASCADE
) ENGINE = INNODB;

-- 11. Викуплені квитки (конкретні місця на рейсах у рамках бронювання)
CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    flight_id INT NOT NULL,
    passenger_name VARCHAR(100) NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    CONSTRAINT fk_tickets_booking FOREIGN KEY (booking_id) REFERENCES bookings (id) ON DELETE CASCADE,
    CONSTRAINT fk_tickets_flight FOREIGN KEY (flight_id) REFERENCES flights (id) ON DELETE RESTRICT
) ENGINE = INNODB;

-- ==============================================================================
-- Створення індексів (Мінімум 5 індексів за вимогами Лаб 1 та Лаб 3)
-- ==============================================================================
CREATE INDEX idx_flights_departure ON flights(departure_time);
CREATE INDEX idx_flights_airports ON flights(dep_airport_id, arr_airport_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_tickets_flight ON tickets(flight_id);

-- ==============================================================================
-- Наповнення даними (INSERT по 10 записів з правильним порядком FK)
-- ==============================================================================

INSERT INTO countries (id, name) VALUES 
(1, 'Україна'), (2, 'Польща'), (3, 'Німеччина'), (4, 'США'), (5, 'Велика Британія'),
(6, 'Франція'), (7, 'Італія'), (8, 'Іспанія'), (9, 'Туреччина'), (10, 'Нідерланди');

INSERT INTO cities (id, country_id, name) VALUES 
(1, 1, 'Київ'), (2, 2, 'Варшава'), (3, 3, 'Берлін'), (4, 4, 'Нью-Йорк'), (5, 5, 'Лондон'),
(6, 6, 'Париж'), (7, 7, 'Рим'), (8, 8, 'Мадрид'), (9, 9, 'Стамбул'), (10, 10, 'Амстердам');

INSERT INTO airports (id, city_id, iata_code, name) VALUES 
(1, 1, 'KBP', 'Бориспіль'), (2, 2, 'WAW', 'Аеропорт Шопена'), (3, 3, 'BER', 'Бранденбург'), 
(4, 4, 'JFK', 'Джона Кеннеді'), (5, 5, 'LHR', 'Хітроу'), (6, 6, 'CDG', 'Шарль-де-Голль'), 
(7, 7, 'FCO', 'Ф''юмічіно'), (8, 8, 'MAD', 'Барахас'), (9, 9, 'IST', 'Новий аеропорт'), 
(10, 10, 'AMS', 'Схіпгол');

INSERT INTO airlines (id, name, base_airport_id, contact_email) VALUES 
(1, 'Ukraine International', 1, 'info@flyuia.com'), (2, 'LOT Polish Airlines', 2, 'contact@lot.com'), 
(3, 'Lufthansa', 3, 'service@lufthansa.com'), (4, 'Delta Air Lines', 4, 'support@delta.com'), 
(5, 'British Airways', 5, 'help@ba.com'), (6, 'Air France', 6, 'contact@airfrance.com'), 
(7, 'ITA Airways', 7, 'info@ita.com'), (8, 'Iberia', 8, 'service@iberia.com'), 
(9, 'Turkish Airlines', 9, 'help@turkish.com'), (10, 'KLM Royal Dutch', 10, 'support@klm.com');

INSERT INTO baggage_rules (id, airline_id, tier_name, weight_limit_kg) VALUES 
(1, 1, 'Basic Cabin', 7), (2, 2, 'Standard Checked', 23), (3, 3, 'Premium Checked', 32), 
(4, 4, 'Economy Light', 10), (5, 5, 'Business Class', 64), (6, 6, 'Cabin Only', 8), 
(7, 7, 'Standard', 20), (8, 8, 'Plus', 25), (9, 9, 'Eco', 15), (10, 10, 'Max', 40);

INSERT INTO users (id, first_name, last_name, email, phone) VALUES 
(1, 'Іван', 'Симоненко', 'ivan.s@gmail.com', '+380501234567'), 
(2, 'Олена', 'Коваленко', 'olena.k@ukr.net', '+380671234567'), 
(3, 'Тарас', 'Шевченко', 'taras@gmail.com', '+380631234567'), 
(4, 'Юрій', 'Матвіїв', 'yurii.m@gmail.com', '+380991234567'), 
(5, 'Анна', 'Мельник', 'anna.m@gmail.com', '+380509876543'), 
(6, 'Дмитро', 'Ткаченко', 'dima.t@ukr.net', '+380679876543'), 
(7, 'Оксана', 'Бойко', 'oksana.b@gmail.com', '+380639876543'), 
(8, 'Максим', 'Лисенко', 'max.l@gmail.com', '+380999876543'), 
(9, 'Наталія', 'Кравчук', 'nata.k@gmail.com', '+380501112233'), 
(10, 'Андрій', 'Павленко', 'andriy.p@ukr.net', '+380671112233');

INSERT INTO booking_statuses (id, status_name) VALUES 
(1, 'Pending'), (2, 'Confirmed'), (3, 'Cancelled'), (4, 'Completed'), (5, 'Refunded'), 
(6, 'On Hold'), (7, 'Processing'), (8, 'Failed'), (9, 'Awaiting Payment'), (10, 'Rejected');

INSERT INTO bookings (id, user_id, status_id, total_price) VALUES 
(1, 1, 2, 450.00), (2, 2, 2, 1200.50), (3, 3, 3, 300.00), (4, 4, 4, 850.00), 
(5, 5, 1, 150.00), (6, 6, 2, 640.20), (7, 7, 5, 900.00), (8, 8, 4, 420.00), 
(9, 9, 2, 1100.00), (10, 10, 1, 250.00);

INSERT INTO flights (id, airline_id, dep_airport_id, arr_airport_id, departure_time, arrival_time, base_price, baggage_rule_id) VALUES 
(1, 1, 1, 2, '2026-11-01 10:00:00', '2026-11-01 11:30:00', 150.00, 1),
(2, 2, 2, 4, '2026-11-01 14:00:00', '2026-11-01 18:30:00', 600.00, 2),
(3, 3, 3, 5, '2026-11-02 09:00:00', '2026-11-02 10:45:00', 200.00, 3),
(4, 4, 4, 6, '2026-11-03 22:00:00', '2026-11-04 11:00:00', 800.00, 4),
(5, 5, 5, 7, '2026-11-04 13:00:00', '2026-11-04 15:30:00', 180.00, 5),
(6, 6, 6, 8, '2026-11-05 08:30:00', '2026-11-05 10:30:00', 120.00, 6),
(7, 7, 7, 9, '2026-11-06 16:00:00', '2026-11-06 19:30:00', 250.00, 7),
(8, 8, 8, 10, '2026-11-07 11:00:00', '2026-11-07 13:45:00', 190.00, 8),
(9, 9, 9, 1, '2026-11-08 07:00:00', '2026-11-08 09:00:00', 210.00, 9),
(10, 10, 10, 2, '2026-11-09 18:00:00', '2026-11-09 19:50:00', 170.00, 10);

INSERT INTO connected_flights (id, flight_1_id, flight_2_id, layover_duration_mins) VALUES 
(1, 1, 2, 150), (2, 3, 5, 135), (3, 6, 8, 30), (4, 7, 9, 210), (5, 8, 10, 180),
(6, 10, 2, 120), (7, 5, 7, 90), (8, 9, 1, 60), (9, 4, 6, 140), (10, 2, 4, 210);

INSERT INTO tickets (id, booking_id, flight_id, passenger_name, seat_number) VALUES 
(1, 1, 1, 'Іван Симоненко', '12A'), (2, 1, 2, 'Іван Симоненко', '14B'), 
(3, 2, 4, 'Олена Коваленко', '1A'), (4, 3, 3, 'Тарас Шевченко', '22C'), 
(5, 4, 5, 'Юрій Матвіїв', '15F'), (6, 4, 7, 'Юрій Матвіїв', '16F'), 
(7, 5, 6, 'Анна Мельник', '8D'), (8, 6, 8, 'Дмитро Ткаченко', '4A'), 
(9, 7, 9, 'Оксана Бойко', '30E'), (10, 8, 10, 'Максим Лисенко', '11C');