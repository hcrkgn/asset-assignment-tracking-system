CREATE TABLE roles (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE departments (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL UNIQUE
);



CREATE TABLE users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    RoleID INT NOT NULL,
    DepartmentID INT,
    FOREIGN KEY (RoleID) REFERENCES roles(RoleID),
    FOREIGN KEY (DepartmentID) REFERENCES departments(DepartmentID)
);


CREATE TABLE categories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE assets (
    AssetID INT AUTO_INCREMENT PRIMARY KEY,
    AssetName VARCHAR(100) NOT NULL,
    CategoryID INT NOT NULL,
    SerialNumber VARCHAR(100) UNIQUE,
    Quantity INT DEFAULT 1,
    AssetType VARCHAR(50),
    Status VARCHAR(50) NOT NULL,
    PurchaseDate DATE,
    FOREIGN KEY (CategoryID) REFERENCES categories(CategoryID)
);


CREATE TABLE assignments (
    AssignmentID INT AUTO_INCREMENT PRIMARY KEY,
    AssetID INT NOT NULL,
    UserID INT NOT NULL,
    AssignedDate DATE NOT NULL,
    ReturnedDate DATE,
    FOREIGN KEY (AssetID) REFERENCES assets(AssetID),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);


CREATE TABLE maintenance (
    MaintenanceID INT AUTO_INCREMENT PRIMARY KEY,
    AssetID INT NOT NULL,
    Description TEXT,
    MaintenanceDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (AssetID) REFERENCES assets(AssetID)
);


CREATE TABLE inventory (
    InventoryID INT AUTO_INCREMENT PRIMARY KEY,
    AssetID INT NOT NULL,
    CountedQuantity INT NOT NULL,
    CountDate DATE NOT NULL,
    FOREIGN KEY (AssetID) REFERENCES assets(AssetID)
);


CREATE TABLE requests (
    RequestID INT AUTO_INCREMENT PRIMARY KEY,
    RequesterID INT NOT NULL,
    CategoryID INT NOT NULL,
    RequestDate DATE NOT NULL,
    Quantity INT NOT NULL,
    Status VARCHAR(50),
    Description TEXT,
    FOREIGN KEY (RequesterID) REFERENCES users(UserID),
    FOREIGN KEY (CategoryID) REFERENCES categories(CategoryID)
);