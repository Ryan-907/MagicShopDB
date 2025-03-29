import sqlite3 as sql

def run_queries():
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    print('\nAll locations and their sizes')
    cursor.execute("""
        SELECT LocationName, LocationSize
        FROM LOCATIONS
                   """)
    for row in cursor.fetchall():
        print(row)
        
    print("\nAll items, descriptions, and raritys")
    cursor.execute("""
            SELECT ItemName, Description, Rarity
            FROM ITEM
                   """)
    for row in cursor.fetchall():
        print(f'{row}\n')

    print("\nAll Shops and Their Locations:")
    cursor.execute("""
        SELECT s.ShopID, s.Owner || "'s " || s.ShopType AS ShopName, s.LocationName, l.LocationSize
        FROM SHOP s
        JOIN LOCATIONS l ON s.LocationName = l.LocationName
    """)
    for row in cursor.fetchall():
        print(row)

    print("\nShop Inventories (Joined with Item Info):")
    cursor.execute("""
        SELECT s.Owner || "'s " || s.ShopType AS ShopName, i.ItemName, i.Rarity, si.Quantity
        FROM SHOP_INVENTORY si
        JOIN SHOP s ON si.ShopID = s.ShopID
        JOIN ITEM i ON si.ItemID = i.ItemID
    """)
    for row in cursor.fetchall():
        print(row)

    print("\nTotal Value of Inventory per Shop:")
    cursor.execute("""
        SELECT s.Owner || "'s " || s.ShopType AS ShopName,
               SUM(si.Quantity * bp.BasePrice) AS TotalValue
        FROM SHOP s
        JOIN SHOP_INVENTORY si ON s.ShopID = si.ShopID
        JOIN ITEM i ON si.ItemID = i.ItemID
        JOIN BASE_PRICE bp ON i.Rarity = bp.Rarity
        GROUP BY s.ShopID
    """)
    for row in cursor.fetchall():
        print(row)

    print("\nLegendary Items and Which Shops Carry Them:")
    cursor.execute("""
        SELECT s.Owner || "'s " || s.ShopType AS ShopName, i.ItemName, si.Quantity
        FROM ITEM i
        JOIN SHOP_INVENTORY si ON i.ItemID = si.ItemID
        JOIN SHOP s ON si.ShopID = s.ShopID
        WHERE i.Rarity = 'Legendary'
    """)
    for row in cursor.fetchall():
        print(row)

    conn.close()

if __name__ == "__main__":
    run_queries()
