import sqlite3 as sql

def insert_sample_data():
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    # LOCATIONS
    cursor.executemany("""
        INSERT INTO LOCATIONS (LocationName, LocationSize)
        VALUES (?, ?)
    """, [
        ("Myrkwood", 1),
        ("Plethora", 2),
        ("Reasonable", 3)
    ])

    # OWNER
    cursor.executemany("""
        INSERT INTO OWNER (Owner, CharityValue)
        VALUES (?, ?)
    """, [
        ("Edd E Kurrent", 0),
        ("Misaliti", 1),
        ("Horns", 2)
    ])

    # BASE_PRICE
    cursor.executemany("""
        INSERT INTO BASE_PRICE (Rarity, BasePrice)
        VALUES (?, ?)
    """, [
        ("Common", 10),
        ("Uncommon", 25),
        ("Rare", 100),
        ("Legendary", 500)
    ])

    # ITEM — now includes Category and Universal
    cursor.executemany("""
        INSERT INTO ITEM (ItemID, ItemName, Description, Rarity, Category, Universal)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, "Health Potion", "Restores 50 HP", "Common", "Potion", 1),        # Universal
        (2, "Steel Sword", "A sturdy weapon", "Uncommon", "Weapon", 0),
        (3, "Dragonbone Bow", "Extremely powerful bow", "Rare", "Weapon", 0),
        (4, "Crown of Fire", "A legendary artifact", "Legendary", "Magic", 0),
        (5, "Map of Wonders", "Reveals hidden paths", "Rare", "Scroll", 1),   # Universal
        (6, "Spell Tome", "Grants knowledge of a spell", "Uncommon", "Book", 0)
    ])

    # SHOP — now includes Gold based on location size * 100
    cursor.executemany("""
        INSERT INTO SHOP (ShopID, Owner, LocationName, ShopType, Gold)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, "Edd E Kurrent", "Myrkwood", "Blacksmith", 100),       # Small (1) → 100g
        (2, "Misaliti", "Plethora", "General Store", 200),         # Medium (2) → 200g
        (3, "Horns", "Reasonable", "Magic Shop", 300)              # Large (3) → 300g
    ])

    # SHOP_TYPE_ALLOWED_CATEGORIES
    cursor.executemany("""
        INSERT INTO SHOP_TYPE_ALLOWED_CATEGORIES (ShopType, Category)
        VALUES (?, ?)
    """, [
        ("Blacksmith", "Weapon"),
        ("General Store", "Potion"),
        ("General Store", "Scroll"),
        ("Magic Shop", "Magic"),
        ("Magic Shop", "Scroll"),
        ("Library", "Book")
    ])

    # SHOP_INVENTORY
    cursor.executemany("""
        INSERT INTO SHOP_INVENTORY (InventoryID, ShopID, ItemID, Quantity)
        VALUES (?, ?, ?, ?)
    """, [
        (1, 1, 1, 10),  # Health Potion in Blacksmith (allowed by universal flag)
        (2, 1, 2, 2),   # Steel Sword in Blacksmith
        (3, 2, 1, 5),   # Health Potion in General Store
        (4, 3, 4, 1),   # Crown of Fire in Magic Shop
        (5, 3, 3, 3),   # Dragonbone Bow in Magic Shop (assumed okay for now)
        (6, 2, 5, 2),   # Map of Wonders (universal) in General Store
        (7, 3, 5, 1)    # Map of Wonders (universal) in Magic Shop
    ])

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()
