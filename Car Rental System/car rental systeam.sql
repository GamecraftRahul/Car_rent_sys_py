-- -----------------------------------------------------------
-- DROP OLD DATABASE COMPLETELY (if exists)
-- -----------------------------------------------------------
DROP DATABASE IF EXISTS car_rental_system;

-- -----------------------------------------------------------
-- CREATE NEW DATABASE
-- -----------------------------------------------------------
CREATE DATABASE car_rental_system;
USE car_rental_system;

-- -----------------------------------------------------------
-- TABLE: customers
-- -----------------------------------------------------------
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    address VARCHAR(255)
);

-- -----------------------------------------------------------
-- TABLE: cars
-- -----------------------------------------------------------
CREATE TABLE cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    car_name VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    model_year INT,
    price_per_day DECIMAL(10,2),
    status ENUM('Available', 'Rented') DEFAULT 'Available',
    fuel_type VARCHAR(50),
    seating_capacity INT,
    car_number VARCHAR(50) UNIQUE
);

-- -----------------------------------------------------------
-- TABLE: rentals
-- -----------------------------------------------------------
CREATE TABLE rentals (
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    car_id INT,
    rent_date DATE,
    return_date DATE,
    total_amount DECIMAL(10,2),
    status ENUM('Ongoing','Returned') DEFAULT 'Ongoing',

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (car_id) REFERENCES cars(car_id)
);

-- -----------------------------------------------------------
-- SAMPLE DATA — customers
-- -----------------------------------------------------------
INSERT INTO customers (name, phone, email, address) VALUES
('Rahul Sharma', '9876543210', 'rahul@example.com', 'Mumbai'),
('Amit Verma', '9988776655', 'amit@example.com', 'Delhi'),
('Neha Patel', '9090909090', 'neha@example.com', 'Ahmedabad'),
('Sanjay Mehta', '9988001122', 'sanjay@example.com', 'Surat');

-- -----------------------------------------------------------
-- SAMPLE DATA — cars
-- -----------------------------------------------------------
INSERT INTO cars (car_name, brand, model_year, price_per_day, status, fuel_type, seating_capacity, car_number) VALUES
('Swift Dzire', 'Maruti Suzuki', 2020, 1200.00, 'Available', 'Petrol', 5, 'MH14AB1234'),
('i20 Sportz', 'Hyundai', 2021, 1500.00, 'Rented', 'Diesel', 5, 'DL01CD5678'),
('Innova Crysta', 'Toyota', 2019, 2500.00, 'Available', 'Diesel', 7, 'GJ18PQ9090'),
('Honda City', 'Honda', 2022, 1800.00, 'Rented', 'Petrol', 5, 'MH12XY4567'),
('Ertiga', 'Maruti Suzuki', 2021, 2200.00, 'Available', 'Petrol', 7, 'RJ07HG8899');

-- -----------------------------------------------------------
-- SAMPLE DATA — rentals
-- -----------------------------------------------------------
INSERT INTO rentals (customer_id, car_id, rent_date, return_date, total_amount, status) VALUES
(1, 2, '2025-01-10', '2025-01-13', 4500.00, 'Returned'),
(2, 4, '2025-01-18', '2025-01-22', 7200.00, 'Ongoing');
