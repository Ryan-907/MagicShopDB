import sqlite3 as sql

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
        INSERT INTO LOCATION_DATA (LocationSize, MaxGold, MaxWares)
        VALUES (?, ?, ?)
    """, [
        (1, 500, 10),
        (2, 1000, 20),
        (3, 2000, 40)
    ])


    cursor.executemany("""
        INSERT INTO OWNER_CHARITY (Owner, CharityValue)
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
        INSERT INTO ITEM (ItemID, ItemName, Description, Rarity)
        VALUES (?, ?, ?, ?)
    """, [
        (1, "Health Potion", "Restores 50 HP", "Common"),
        (2, "Steel Sword", "A sturdy weapon", "Uncommon"),
        (3, "Dragonbone Bow", "Extremely powerful bow", "Rare"),
        (4, "Crown of Fire", "A legendary artifact", "Legendary")
    ])


    cursor.executemany("""
        INSERT INTO SHOP (ShopID, Owner, LocationName, ShopType)
        VALUES (?, ?, ?, ?)
    """, [
        (1, "Edd E Kurrent", "Myrkwood", "Blacksmith"),
        (2, "Misaliti", "Plethora", "General Store"),
        (3, "Horns", "Reasonable", "Magic Shop")
    ])


    cursor.executemany("""
        INSERT INTO SHOP_INVENTORY (InventoryID, ShopID, ItemID, Quantity)
        VALUES (?, ?, ?, ?)
    """, [
        (1, 1, 1, 10), 
        (2, 1, 2, 2),  
        (3, 2, 1, 5),  
        (4, 3, 4, 1),   
        (5, 3, 3, 3)   
    ])

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()
