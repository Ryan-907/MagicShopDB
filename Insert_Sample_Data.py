import sqlite3 as sql
from TableClasess import DatabaseManager

def insert_sample_data():
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.executemany("""
        INSERT INTO LOCATIONS (LocationName, LocationSize)
        VALUES (?, ?)
    """, [
        ("Myrkwood", 1),
        ("Plethora", 2),
        ("Reasonable", 3)
    ])

   
    cursor.executemany("""
        INSERT INTO OWNER (Owner, CharityValue)
        VALUES (?, ?)
    """, [
        ("Edd E Kurrent", 0),
        ("Misaliti", 1),
        ("Horns", 2)
    ])

  
    cursor.executemany("""
        INSERT INTO BASE_PRICE (Rarity, BasePrice)
        VALUES (?, ?)
    """, [
        ("Common", 10),
        ("Uncommon", 25),
        ("Rare", 100),
        ("Legendary", 500)
    ])

    cursor.executemany("""
        INSERT INTO ITEM (ItemID, ItemName, Description, Rarity, Category, Universal)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, "Health Potion", "Restores 50 HP", "Common", "Potion", 1),        
        (2, "Steel Sword", "A sturdy weapon", "Uncommon", "Weapon", 0),
        (3, "Dragonbone Bow", "Extremely powerful bow", "Rare", "Weapon", 0),
        (4, "Crown of Fire", "A legendary artifact", "Legendary", "Magic", 0),
        (5, "Map of Wonders", "Reveals hidden paths", "Rare", "Scroll", 1),   
        (6, "Spell Tome", "Grants knowledge of a spell", "Uncommon", "Book", 0)
    ])

    
    cursor.executemany("""
        INSERT INTO SHOP (ShopID, Owner, LocationName, ShopType, Gold)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, "Edd E Kurrent", "Myrkwood", "Blacksmith", 100),       
        (2, "Misaliti", "Plethora", "General Store", 200),         
        (3, "Horns", "Reasonable", "Magic Shop", 300)              
    ])

   
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

  
    cursor.executemany("""
        INSERT INTO SHOP_INVENTORY (InventoryID, ShopID, ItemID, Quantity)
        VALUES (?, ?, ?, ?)
    """, [
        (1, 1, 1, 10),  
        (2, 1, 2, 2),   
        (3, 2, 1, 5),   
        (4, 3, 4, 1),   
        (5, 3, 3, 3),   
        (6, 2, 5, 2),   
        (7, 3, 5, 1)   
    ])

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()
    db = DatabaseManager("shop_inventory.db")
    db.print_all_tables()
