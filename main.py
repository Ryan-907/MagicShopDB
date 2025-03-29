import sqlite3 as sql
import pyinputplus as pyip

SIZES = {'Small':1, 'Medium':2, 'Large':3}
CHARITABILITY = {'Cheap':1, 'Average':2, 'Charitable':3}
RARITIES = ['Common', 'Uncommon', 'Rare', 'Legendary']
OPTIONS = ['Insert Location', 'Generate New Owner', 'Insert New Item', 'Query Table', 'Create Shop']
COLUMNS = ['LocationName', 'Owner'] #May be good idea to change into a dictionary
SHOP_TYPES = ['Potions', 'Weapons & Armor', 'Magic Itmes', 'General Store']
def generate_location(location, size) -> None:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        INSERT INTO LOCATIONS (LocationName, LocationSize)
        VALUES (?, ?)
    """, (location, size))

    conn.commit()
    conn.close()

def get_list(column, table) -> list:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT {column}
        FROM {table}
    """)

    return [value[0] for value in cursor.fetchall()]

def generate_owner(owner, charity) -> None:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        INSERT INTO OWNER_CHARITY (Owner, CharityValue)
        VALUES (?, ?)
    """, (owner, charity))

    conn.commit()
    conn.close()

def insert_item(ItemName, Description, Rarity) -> None:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        INSERT INTO ITEM (ItemName, Description, Rarity)
        VALUES (?, ?, ?)
        """, (ItemName, Description, Rarity))

    conn.commit()
    conn.close()    

def generate_shop(Owner, LocationName, ShopType) -> None:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.executemany("""
        INSERT INTO SHOP (Owner, LocationName, ShopType)
        VALUES (?, ?, ?)
    """, (Owner, LocationName, ShopType))
    conn.commit()
    conn.close()

if __name__=='__main__':
    action = pyip.inputMenu(OPTIONS, 'Select action\n', numbered=True)
    if action == OPTIONS[0]:
        name = pyip.inputStr('Enter location name: ', blank= False)
        size = pyip.inputMenu([size for size in SIZES.keys()], numbered= True)
        size = SIZES[size]
        generate_location(name, size)

    elif action == OPTIONS[1]:
        owner = pyip.inputStr('Enter Owner Name', blank=False)
        charity = pyip.inputMenu([char for char in CHARITABILITY.keys()], numbered=True)
        charity = CHARITABILITY[charity]
        generate_owner(owner, charity)

    elif action == OPTIONS[2]:
        item_name = pyip.inputStr("Enter item name: ")
        desc = pyip.inputStr("Enter the item description: ")
        rarity = pyip.inputMenu(RARITIES, numbered=True)
        insert_item(item_name, desc, rarity)

    elif action == OPTIONS[3]:
        column = pyip.inputMenu(COLUMNS, numbered=True)
        if column == COLUMNS[0]:
            table = 'LOCATIONS'
        elif column == COLUMNS[1]:
            table = 'OWNER_CHARITY'
        print(get_list(column, table))
    elif action == OPTIONS[4]:
        owner = pyip.inputMenu(get_list('Owner', 'OWNER_CHARITY'), 'Select Owner\n', numbered=True)
        location = pyip.inputMenu(get_list('LocationName', 'LOCATIONS'), 'Select shop location\n', numbered=True)
        s_type = pyip.inputMenu(SHOP_TYPES, 'Select shop type\n', numbered=True)
        print(f'If this function inserted you would have a {s_type} owned by {owner} in {location}. But it does not do anything!')



