# Design Decisions

## 1. Single Asset and Quantity-Based Asset

The system supports both single assets and quantity-based assets in the same Asset table.

- Single assets have a unique serial number and a quantity of 1.
- Quantity-based assets do not require a serial number and can have a quantity greater than 1.

The **AssetType** field is used to distinguish between these two asset types.

---

## 2. Primary Keys, Foreign Keys, and Uniqueness

Every table has a primary key.

Relationships between tables are created using foreign keys.

Uniqueness constraints are applied where necessary, such as the Email field in the User table and the SerialNumber field in the Asset table.

---

## 3. Serial Number Uniqueness

Serial numbers must be unique.

Assets without a serial number are allowed only for quantity-based assets.

Empty serial numbers should not violate the uniqueness constraint.

---

## 4. Deletion Policy

The project uses **Soft Delete**.

Records that are already used by other tables should not be permanently removed from the database.

Instead, they should be marked as inactive to preserve historical data and maintain database integrity.

## Mentor Question

**Question:**
What happens if I enter the same serial number twice? Is that prevented by the database or by the application? What if neither does it?

**Answer:**

The application checks the serial number before creating a new asset. If the serial number already exists, it shows an error message.

The database also uses a UNIQUE constraint for the SerialNumber field. This prevents duplicate serial numbers from being stored.

If neither the application nor the database checks the serial number, duplicate records can be created. This can cause incorrect asset tracking and data inconsistency.
