# CodeGen for dummy data
This allows us to quickly initialise data to the tables.

# Requirements
- MySQL
- A `ClubsData - ClubsInfo.csv` file exported from Google Sheets.
> [!NOTE]
> If using a Docker container for MySQL, mount this directory into the container to access the `initialise.sql` script.

# Usage
## SQL Generation
```bash
python codegen.py
```
This outputs a `output.txt` file which contains the data for insertion. 

## SQL script
```sql
source <path_to_initalise.sql>
```
> [!NOTE]
> The output from `codegen.py` should be appended to the bottom of this SQL script.

```sql
-- Ensure that UTF-8 is used
SET NAMES utf8mb4;

-- Setup the Database
CREATE DATABASE IF NOT EXISTS InClubSIT;
USE InClubSIT;

-- Setup the Tables
CREATE TABLE IF NOT EXISTS Account (
    AccountID INT NOT NULL AUTO_INCREMENT,
    Username VARCHAR(127) NOT NULL UNIQUE,
    Email VARCHAR(127) NOT NULL UNIQUE,
    Password BINARY(60) NOT NULL,
    PRIMARY KEY (AccountID),
    UNIQUE (Username, Email)
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
    PRIMARY KEY (ClubID),
    FOREIGN KEY (ClubCategoryID)
        REFERENCES ClubCategory(ClubCategoryID)
);

CREATE TABLE IF NOT EXISTS ClubCategoryInformation (
    ClubCategoryInfoID INT NOT NULL AUTO_INCREMENT,
    ClubCategoryID INT NOT NULL,
    CategoryDescription LONGTEXT NOT NULL,
    ImageURL VARCHAR(511) NOT NULL,
    OtherDetails LONGTEXT,
    PRIMARY KEY (ClubCategoryInfoID),
    FOREIGN KEY (ClubCategoryID)
        REFERENCES ClubCategory(ClubCategoryID)
);


CREATE TABLE IF NOT EXISTS ClubMember (
    ClubMemberID INT NOT NULL AUTO_INCREMENT,
    ClubID INT NOT NULL,
    AccountID INT NOT NULL,
    AccountTypeID INT NOT NULL,
    PRIMARY KEY (ClubMemberID),
    FOREIGN KEY (ClubID)
        REFERENCES Club(ClubID),
    FOREIGN KEY (AccountID)
        REFERENCES Account(AccountID)
        ON DELETE CASCADE,
    FOREIGN KEY (AccountTypeID)
        REFERENCES AccountType(AccountTypeID),
    UNIQUE (ClubID, AccountID)
);

CREATE TABLE IF NOT EXISTS Interest (
    InterestID INT NOT NULL AUTO_INCREMENT,
    AccountID INT NOT NULL,
    ClubID INT NOT NULL,
    PRIMARY KEY (InterestID),
    FOREIGN KEY (AccountID)
        REFERENCES Account(AccountID)
        ON DELETE CASCADE,
    FOREIGN KEY (ClubID)
        REFERENCES Club(ClubID)
        ON DELETE CASCADE
);
```