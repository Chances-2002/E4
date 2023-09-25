-- Create database
CREATE DATABASE IF NOT EXISTS library;

-- Use the library database
USE library;

-- Create tables
CREATE TABLE IF NOT EXISTS Books (
  BookID INT AUTO_INCREMENT PRIMARY KEY,
  Title VARCHAR(255) NOT NULL,
  Author VARCHAR(255) NOT NULL,
  ISBN VARCHAR(255) NOT NULL,
  Status VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
  UserID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255) NOT NULL,
  Email VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Reservations (
  ReservationID INT AUTO_INCREMENT PRIMARY KEY,
  BookID INT NOT NULL,
  UserID INT NOT NULL,
  ReservationDate DATE,
  FOREIGN KEY (BookID) REFERENCES Books(BookID),
  FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Insert sample data
INSERT INTO Books (Title, Author, ISBN, Status)
VALUES ('Book 1', 'Author 1', 'ISBN001', 'Available'),
       ('Book 2', 'Author 2', 'ISBN002', 'Reserved'),
       ('Book 3', 'Author 3', 'ISBN003', 'Available'),
       ('Book 4', 'Author 4', 'ISBN004', 'Reserved'),
       ('Book 5', 'Author 5', 'ISBN005', 'Available');

INSERT INTO Users (Name, Email)
VALUES ('User 1', 'user1@example.com'),
       ('User 2', 'user2@example.com'),
       ('User 3', 'user3@example.com'),
       ('User 4', 'user4@example.com'),
       ('User 5', 'user5@example.com');

INSERT INTO Reservations (BookID, UserID, ReservationDate)
VALUES (2, 1, '2023-09-01'),
       (4, 3, '2023-09-05');