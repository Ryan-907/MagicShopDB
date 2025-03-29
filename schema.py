import sqlite3 as sql

def create_tables():
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()

    # Enable fk constraints
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS LOCATIONS (
            LocationName TEXT PRIMARY KEY,
            LocationSize INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS LOCATION_DATA (
            LocationSize INTEGER PRIMARY KEY,
            MaxGold INTEGER,
            MaxWares INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OWNER_CHARITY (
            Owner TEXT PRIMARY KEY,
            CharityValue INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BASE_PRICE (
            Rarity TEXT PRIMARY KEY,
            BasePrice INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ITEM (
            ItemID INTEGER PRIMARY KEY,
            ItemName TEXT NOT NULL,
            Description TEXT,
            Rarity TEXT,
            FOREIGN KEY (Rarity) REFERENCES BASE_PRICE(Rarity)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SHOP (
            ShopID INTEGER PRIMARY KEY,
            Owner TEXT,
            LocationName TEXT,
            ShopType TEXT,
            FOREIGN KEY (Owner) REFERENCES OWNER_CHARITY(Owner),
            FOREIGN KEY (LocationName) REFERENCES LOCATIONS(LocationName)
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SHOP_INVENTORY (
            InventoryID INTEGER PRIMARY KEY,
            ShopID INTEGER,
            ItemID INTEGER,
            Quantity INTEGER,
            FOREIGN KEY (ShopID) REFERENCES SHOP(ShopID),
            FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
