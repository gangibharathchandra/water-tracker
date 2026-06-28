CREATE DATABASE IF NOT EXISTS water_tracker
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE water_tracker;

CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    issue VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,
    image VARCHAR(500),
    time VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Pending',
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
