INSERT INTO roles (RoleName) VALUES
('Admin'),
('Warehouse Officer'),
('Department Manager'),
('Employee');

INSERT INTO categories (CategoryName) VALUES
('Laptop'),
('Monitor'),
('Keyboard'),
('Mouse'),
('Phone');

INSERT INTO departments (DepartmentName) VALUES
('IT'),
('Human Resources'),
('Finance'),
('Sales'),
('Operations');

INSERT INTO locations (LocationName) VALUES
('Head Office'),
('Main Warehouse'),
('Ankara Branch');

INSERT INTO assets
(AssetName, CategoryID, LocationID, SerialNumber, Quantity, AssetType, Status, PurchaseDate)
VALUES
('Dell Latitude 5420', 1, 1, 'LT001', 1, 'Individual', 'Available', '2025-01-10'),
('HP ProBook 450', 1, 2, 'LT002', 1, 'Individual', 'Available', '2025-01-15'),
('Lenovo ThinkPad E14', 1, 3, 'LT003', 1, 'Individual', 'Assigned', '2025-02-01'),
('Acer Aspire 5', 1, 1, 'LT004', 1, 'Individual', 'Maintenance', '2025-02-10'),

('Dell P2422H', 2, 2, 'MN001', 1, 'Individual', 'Available', '2025-01-20'),
('LG UltraFine', 2, 3, 'MN002', 1, 'Individual', 'Assigned', '2025-02-12'),
('Samsung S24R', 2, 1, 'MN003', 1, 'Individual', 'Available', '2025-03-05'),
('AOC 24G2', 2, 2, 'MN004', 1, 'Individual', 'Faulty', '2025-03-15'),

('Logitech K120', 3, 3, 'KB001', 10, 'Consumable', 'Available', '2025-01-08'),
('Logitech K380', 3, 1, 'KB002', 1, 'Individual', 'Assigned', '2025-01-18'),
('HP Keyboard', 3, 2, 'KB003', 1, 'Individual', 'Available', '2025-02-22'),
('Dell Keyboard', 3, 3, 'KB004', 1, 'Individual', 'Available', '2025-03-12'),

('Logitech M185', 4, 1, 'MS001', 20, 'Consumable', 'Available', '2025-01-11'),
('Logitech MX Master 3', 4, 2, 'MS002', 1, 'Individual', 'Assigned', '2025-02-08'),
('HP Mouse', 4, 3, 'MS003', 1, 'Individual', 'Available', '2025-02-28'),
('Dell Mouse', 4, 1, 'MS004', 1, 'Individual', 'Faulty', '2025-03-20'),

('iPhone 13', 5, 2, 'PH001', 1, 'Individual', 'Available', '2025-01-25'),
('Samsung Galaxy S23', 5, 3, 'PH002', 1, 'Individual', 'Assigned', '2025-02-14'),
('Xiaomi 14', 5, 1, 'PH003', 1, 'Individual', 'Available', '2025-03-02'),
('Google Pixel 8', 5, 2, 'PH004', 1, 'Individual', 'Maintenance', '2025-03-18');

INSERT INTO users
(Name, Email, Password, RoleID, DepartmentID)
VALUES
('Admin User', 'admin@aats.com', '$2b$12$8tJC/X3Q679E/QMAPPx3Ze.PPLzyJEz8pMEE5QyhSI73PgtQUNlGW', 1, 1),
('Ayla Ozturk', 'ayla@aats.com', '$2b$12$d7Z08.opw.lZMFuRljRjgu4Hn5KZRvdfdpIjl6n.jbbkcaVrKF8Gm', 2, 5),
('Ayşe Demir', 'ayse@aats.com', '$2b$12$tBgosoHMzH5LT832P47opO6nDdcjrA28qqTD53w0pDzyujuu2lo/e', 4, 5);
