## Table: User

-UserID (PK)
-Name
-Email
-Password
-RoleID (FK)
-DepartmentID (FK)

## Table: Role

-RoleID(PK)
-RoleName

## Table: Department

-DepartmentID(PK)
-DepartmentName

## Table: Assets

-AssetID (PK)
-AssetName
-CategoryID (FK)
-SerialNumber
-Quantity
-AssetType
-Status

## Table: Category

-CategoryID (PK)
-CategoryName

## Table: Assignment

-AssignmentID (PK)
-AssetID (FK)
-UserID (FK)
-AssignDate
-ReturnDate

## Table: Maintenance

-MeintenanceID (PK)
-AssetID(FK)
-Description
-MaintenanceDate
-Status

## Table: Inventory

-InventoryID (PK)
-AssetID (FK)
-CountedQuantity
-CountDate

## Table: Request

-RequestID (PK)
-UserID (FK)
-CategoryID (FK)
-RequestDate
-Quantity
-Status
-Purpose

## Relationships

- User → Role (Many-to-One)
- User → Department (Many-to-One)
- Assignment → User (Many-to-One)
- Assignment → Asset (Many-to-One)
- Asset → Category (Many-to-One)
- Maintenance → Asset (Many-to-One)
- Inventory → Asset (Many-to-One)
- Request → User (Many-to-One)
- Request → Category (Many-to-One)
