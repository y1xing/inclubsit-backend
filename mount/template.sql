-- Ensure that UTF-8 is used
SET NAMES utf8mb4;

-- Setup the Database
DROP DATABASE IF EXISTS InClubSIT;
CREATE DATABASE IF NOT EXISTS InClubSIT;
USE InClubSIT;

-- Setup the Tables
CREATE TABLE IF NOT EXISTS Cluster (
    ClusterID INT NOT NULL AUTO_INCREMENT,
    ClusterName VARCHAR(127) NOT NULL UNIQUE,
    PRIMARY KEY (ClusterID)
);


CREATE TABLE IF NOT EXISTS CourseInformation (
    CourseID INT NOT NULL AUTO_INCREMENT,
    CourseName VARCHAR(127) NOT NULL UNIQUE,
    ClusterID INT NOT NULL,
    PRIMARY KEY (CourseID),
    FOREIGN KEY (ClusterID)
        REFERENCES Cluster(ClusterID)
);

CREATE TABLE IF NOT EXISTS Account (
    StudentID INT NOT NULL,
    Email VARCHAR(127) NOT NULL UNIQUE,
    FirstName VARCHAR(127) NOT NULL,
    LastName VARCHAR(127) NOT NULL,
    MatriculationYear INT NOT NULL,
    CourseID INT NOT NULL,
    Gender VARCHAR(127) NOT NULL,
    PRIMARY KEY (StudentID),
    FOREIGN KEY (CourseID)
        REFERENCES CourseInformation(CourseID)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AccountType (
    AccountTypeID INT NOT NULL AUTO_INCREMENT,
    TypeName VARCHAR(127) NOT NULL UNIQUE,
    PRIMARY KEY (AccountTypeID)
);

CREATE TABLE IF NOT EXISTS ClubCategory (
    ClubCategoryID INT NOT NULL AUTO_INCREMENT,
    ClubCategoryName VARCHAR(127) NOT NULL UNIQUE,
    PRIMARY KEY (ClubCategoryID)
);

CREATE TABLE IF NOT EXISTS Club (
    ClubID INT NOT NULL AUTO_INCREMENT,
    ClubName VARCHAR(127) NOT NULL UNIQUE,
    ClubCategoryID INT NOT NULL,
    ClubDescription LONGTEXT NOT NULL,
    ClubTrainingDates VARCHAR(127) NOT NULL,
    ClubTrainingLocations VARCHAR(127) NOT NULL,
    ClubEmail VARCHAR(127) NOT NULL UNIQUE,
    ClubInstagram VARCHAR(127) NOT NULL UNIQUE,
    PRIMARY KEY (ClubID),
    FOREIGN KEY (ClubCategoryID)
        REFERENCES ClubCategory(ClubCategoryID)
);

CREATE TABLE IF NOT EXISTS ClubCategoryInformation (
    ClubCategoryID INT NOT NULL,
    CategoryDescription LONGTEXT NOT NULL,
    PRIMARY KEY (ClubCategoryID),
    FOREIGN KEY (ClubCategoryID)
        REFERENCES ClubCategory(ClubCategoryID)
);


CREATE TABLE IF NOT EXISTS ClubMember (
    ClubMemberID INT NOT NULL AUTO_INCREMENT,
    ClubID INT NOT NULL,
    StudentID INT NOT NULL,
    AccountTypeID INT NOT NULL,
    PRIMARY KEY (ClubMemberID),
    FOREIGN KEY (ClubID)
        REFERENCES Club(ClubID),
    FOREIGN KEY (StudentID)
        REFERENCES Account(StudentID)
        ON DELETE CASCADE,
    FOREIGN KEY (AccountTypeID)
        REFERENCES AccountType(AccountTypeID),
    UNIQUE (ClubID, StudentID)
);

-- CREATE TABLE IF NOT EXISTS Interest (
--     InterestID INT NOT NULL AUTO_INCREMENT,
--     AccountID INT NOT NULL,
--     ClubID INT NOT NULL,
--     PRIMARY KEY (InterestID),
--     FOREIGN KEY (AccountID)
--         REFERENCES Account(AccountID)
--         ON DELETE CASCADE,
--     FOREIGN KEY (ClubID)
--         REFERENCES Club(ClubID)
--         ON DELETE CASCADE
-- );

-- Dummy Data

INSERT INTO AccountType (TypeName) VALUES ('Member');
INSERT INTO AccountType (TypeName) VALUES ('President');
INSERT INTO AccountType (TypeName) VALUES ('Vice President');
INSERT INTO AccountType (TypeName) VALUES ('Secretary');
