CREATE TABLE roles (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE departments (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE locations (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    LocationName VARCHAR(100) NOT NULL UNIQUE
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

CREATE TABLE brands (
    BrandID INT AUTO_INCREMENT PRIMARY KEY,
    BrandName VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE models (
    ModelID INT AUTO_INCREMENT PRIMARY KEY,
    ModelName VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE assets (
    AssetID INT AUTO_INCREMENT PRIMARY KEY,
    Code VARCHAR(50) NOT NULL UNIQUE,
    AssetName VARCHAR(100) NOT NULL,
    CategoryID INT NOT NULL,
    BrandID INT,
    ModelID INT,
    LocationID INT NOT NULL,
    SerialNumber VARCHAR(100) UNIQUE,
    Quantity INT DEFAULT 1,
    AssetType VARCHAR(50) NOT NULL,
    Status VARCHAR(50) NOT NULL,
    PurchaseDate DATE,
    PurchasePrice DECIMAL(10,2),
    WarrantyEnd DATE,
    Notes TEXT,
    FOREIGN KEY (CategoryID) REFERENCES categories(CategoryID),
    FOREIGN KEY (BrandID) REFERENCES brands(BrandID),
    FOREIGN KEY (ModelID) REFERENCES models(ModelID),
    FOREIGN KEY (LocationID) REFERENCES locations(LocationID)
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

CREATE TABLE login_attempts (
    Email VARCHAR(100) PRIMARY KEY,
    FailedAttempts INT NOT NULL DEFAULT 0,
    LockedUntil DATETIME NULL,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);