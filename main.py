import sqlite3 as sql
import pyinputplus as pyip

SIZES = {'Small':1, 'Medium':2, 'Large':3}
CHARITABILITY = {'Cheap':1, 'Average':2, 'Charitable':3}
RARITIES = ['Common', 'Uncommon', 'Rare', 'Legendary']
OPTIONS = ['Insert Location', 'Generate New Owner', 'Insert New Item', 'Query Table', 'Create Shop']
COLUMNS = ['LocationName', 'Owner'] #May be good idea to change into a dictionary
SHOP_TYPES = ['Potions', 'Weapons & Armor', 'Magic Itmes', 'General Store']

def get_tables() -> list:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
    """)
    
    tables = [row[0] for row in cursor.fetchall()]

    conn.close()
    return tables

def get_columns(table_name: str) -> list:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]

    conn.close()
    return columns

def generate_location() -> None:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    location = pyip.inputStr('Enter location name: ', blank= False)
    size = pyip.inputMenu([size for size in SIZES.keys()], numbered= True)

    size = SIZES[size]

    cursor.execute("""
        INSERT INTO LOCATIONS (LocationName, LocationSize)
        VALUES (?, ?)
    """, (location, size))

    conn.commit()
    conn.close()

def get_list(column=None, table=None) -> None:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    if table == None:
        table = pyip.inputMenu(get_tables(), numbered=True)
    if column == None:
        column = pyip.inputMenu(get_columns(table), numbered=True)

    cursor.execute(f"""
        SELECT {column}
        FROM {table}
    """)

    print([value[0] for value in cursor.fetchall()])

def generate_owner() -> None:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    owner = pyip.inputStr('Enter Owner Name', blank=False)
    charity = pyip.inputMenu([char for char in CHARITABILITY.keys()], numbered=True)
    charity = CHARITABILITY[charity]

    cursor.execute("""
        INSERT INTO OWNER_CHARITY (Owner, CharityValue)
        VALUES (?, ?)
    """, (owner, charity))

    conn.commit()
    conn.close()

def insert_item() -> None:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    ItemName = pyip.inputStr("Enter item name: ")
    Description = pyip.inputStr("Enter the item description: ")
    Rarity = pyip.inputMenu(RARITIES, numbered=True)
    
    cursor.execute("""
        INSERT INTO ITEM (ItemName, Description, Rarity)
        VALUES (?, ?, ?)
        """, (ItemName, Description, Rarity))

    conn.commit()
    conn.close()    

def generate_shop() -> None:
    conn = sql.connect("shop_inventory.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    Owner = pyip.inputMenu(get_list('Owner', 'OWNER_CHARITY'), 'Select Owner\n', numbered=True)
    LocationName = pyip.inputMenu(get_list('LocationName', 'LOCATIONS'), 'Select shop location\n', numbered=True)
    ShopType = pyip.inputMenu(SHOP_TYPES, 'Select shop type\n', numbered=True)

    cursor.executemany("""
        INSERT INTO SHOP (Owner, LocationName, ShopType)
        VALUES (?, ?, ?)
    """, (Owner, LocationName, ShopType))


    conn.commit()
    conn.close()

ACTIONS = {'Generate Location':generate_location, "Generate Owner":generate_owner, 'Insert Item':insert_item, 'Generate Shop':generate_shop, 'Query Table': get_list}
if __name__=='__main__':
    action = pyip.inputMenu([action for action in ACTIONS.keys()], numbered=True)
    ACTIONS[action]()




