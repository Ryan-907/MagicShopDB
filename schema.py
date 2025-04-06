import sqlite3 as sql

def create_tables():
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # LOCATIONS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS LOCATIONS (
            LocationName TEXT PRIMARY KEY,
            LocationSize INTEGER
        )
    """)

    # OWNER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OWNER (
            Owner TEXT PRIMARY KEY,
            CharityValue INTEGER
        )
    """)

    # BASE_PRICE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BASE_PRICE (
            Rarity TEXT PRIMARY KEY,
            BasePrice INTEGER
        )
    """)

    # ITEM with Category + Universal flag
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ITEM (
            ItemID INTEGER PRIMARY KEY,
            ItemName TEXT NOT NULL,
            Description TEXT,
            Rarity TEXT,
            Category TEXT,
            Universal INTEGER DEFAULT 0,
            FOREIGN KEY (Rarity) REFERENCES BASE_PRICE(Rarity)
                ON UPDATE CASCADE ON DELETE SET NULL
        )
    """)

    # SHOP with Gold column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SHOP (
            ShopID INTEGER PRIMARY KEY,
            Owner TEXT,
            LocationName TEXT,
            ShopType TEXT,
            Gold INTEGER,
            FOREIGN KEY (Owner) REFERENCES OWNER(Owner)
                ON UPDATE CASCADE ON DELETE SET NULL,
            FOREIGN KEY (LocationName) REFERENCES LOCATIONS(LocationName)
                ON UPDATE CASCADE ON DELETE SET NULL
        )
    """)

    # SHOP_TYPE_ALLOWED_CATEGORIES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SHOP_TYPE_ALLOWED_CATEGORIES (
            ShopType TEXT,
            Category TEXT,
            PRIMARY KEY (ShopType, Category)
        )
    """)

    # SHOP_INVENTORY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SHOP_INVENTORY (
            InventoryID INTEGER PRIMARY KEY,
            ShopID INTEGER,
            ItemID INTEGER,
            Quantity INTEGER,
            FOREIGN KEY (ShopID) REFERENCES SHOP(ShopID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
