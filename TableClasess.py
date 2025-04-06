import sqlite3 as sql
from dataclasses import dataclass, field

# Mapping for readability
LocationSizes = {1: "small", 2: "medium", 3: "large"}
PRICES = {
    "Common": 50,
    "Uncommon": 250,
    "Rare": 2_500,
    "Very Rare": 25_000,
    "Legendary": 100_000
}

class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sql.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        
    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        
    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

@dataclass
class Location:
    LocationName: str
    LocationSize: int

    @property
    def max_wares(self):
        return self.LocationSize * 10 #Not currently enforced. Considering removal. Logical to limit, but who am I?

    @property
    def max_gold(self):
        return self.LocationSize * 100

    @classmethod
    def load_from_db(cls, db: DatabaseManager, name: str):
        data = db.fetchone("SELECT LocationName, LocationSize FROM LOCATIONS WHERE LocationName = ?", (name,))
        if data:
            return cls(*data)
        else:
            raise ValueError(f"{name} not found")

    def __repr__(self):
        return f"{self.LocationName} is in a {LocationSizes[self.LocationSize]} town"

@dataclass
class Owner:
    Owner: str
    charity_value: int

    @classmethod
    def load_from_db(cls, db: DatabaseManager, Owner: str):
        data = db.fetchone("SELECT Owner, CharityValue FROM OWNER WHERE Owner = ?", (Owner,))
        if data:
            return cls(*data)
        else:
            raise ValueError(f"{Owner} not found")

@dataclass
class Item:
    id: int
    name: str
    description: str
    rarity: str
    category: str
    universal: int = 0

    @property
    def base_price(self):
        return PRICES[self.rarity]

    @classmethod
    def create_new(cls, db: DatabaseManager, name: str, description: str, rarity: str, category: str, universal: int = 0):
        db.execute("""
            INSERT INTO ITEM (ItemName, Description, Rarity, Category, Universal)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, rarity, category, universal)) #Universal is a binary classification for if any shop can own the item or not
        item_id = db.cursor.lastrowid
        return cls(item_id, name, description, rarity, category, universal)

    @classmethod
    def load_from_db(cls, db: DatabaseManager, item_id: int):
        data = db.fetchone("""
            SELECT ItemID, ItemName, Description, Rarity, Category, Universal
            FROM ITEM
            WHERE ItemID = ?
        """, (item_id,))
        if data:
            return cls(*data)
        else:
            raise ValueError(f"Item with ID {item_id} not found.")

    @classmethod
    def load_all(cls, db: DatabaseManager):
        data_list = db.fetchall("""
            SELECT ItemID, ItemName, Description, Rarity, Category, Universal
            FROM ITEM
        """)
        return [cls(*row) for row in data_list]

    def update(self, db: DatabaseManager):
        db.execute("""
            UPDATE ITEM
            SET ItemName = ?, Description = ?, Rarity = ?, Category = ?, Universal = ?
            WHERE ItemID = ?
        """, (self.name, self.description, self.rarity, self.category, self.universal, self.id))

    def __repr__(self):
        return f"<Item #{self.id}: {self.name} ({self.rarity}, {self.category})>"

@dataclass
class Shop:
    id: int
    Owner: str
    LocationName: str
    ShopType: str
    Gold: int
    inventory: list = field(default_factory=list)

    @classmethod
    def load_from_db(cls, db: DatabaseManager, id: int):
        data = db.fetchone("SELECT ShopID, Owner, LocationName, ShopType, Gold FROM SHOP WHERE ShopID = ?", (id,))
        if data:
            return cls(*data)
        else:
            raise ValueError(f"Shop with id {id} not found")

    def update_gold(self, db: DatabaseManager):
        db.execute("UPDATE SHOP SET Gold = ? WHERE ShopID = ?", (self.Gold, self.id))

    def buy_item(self, db: DatabaseManager, item_id: int, quantity: int, price: int):
        total_cost = quantity * price
        current = db.fetchone("SELECT Quantity FROM SHOP_INVENTORY WHERE ShopID = ? AND ItemID = ?", (self.id, item_id))
        if self.Gold < total_cost:
            raise ValueError("Not enough gold to buy item.")
        if current:
            db.execute("UPDATE SHOP_INVENTORY SET Quantity = Quantity + ? WHERE ShopID = ? AND ItemID = ?",
                       (quantity, self.id, item_id))
        else:
            db.execute("INSERT INTO SHOP_INVENTORY (ShopID, ItemID, Quantity) VALUES (?, ?, ?)",
                       (self.id, item_id, quantity))
        self.Gold -= total_cost
        self.update_gold(db)

    def sell_item(self, db: DatabaseManager, item_id: int, quantity: int, price: int):
        current = db.fetchone("SELECT Quantity FROM SHOP_INVENTORY WHERE ShopID = ? AND ItemID = ?", (self.id, item_id))
        if not current or current[0] < quantity:
            raise ValueError("Not enough items in inventory to sell.")
        db.execute("UPDATE SHOP_INVENTORY SET Quantity = Quantity - ? WHERE ShopID = ? AND ItemID = ?",
                   (quantity, self.id, item_id))
        db.execute("DELETE FROM SHOP_INVENTORY WHERE Quantity <= 0 AND ShopID = ? AND ItemID = ?",
                   (self.id, item_id))
        self.Gold += quantity * price
        self.update_gold(db)

    def add_item(self, db: DatabaseManager, item_id: int, quantity: int):
        current = db.fetchone("SELECT Quantity FROM SHOP_INVENTORY WHERE ShopID = ? AND ItemID = ?", (self.id, item_id))
        if current:
            db.execute("UPDATE SHOP_INVENTORY SET Quantity = Quantity + ? WHERE ShopID = ? AND ItemID = ?",
                       (quantity, self.id, item_id))
        else:
            db.execute("INSERT INTO SHOP_INVENTORY (ShopID, ItemID, Quantity) VALUES (?, ?, ?)",
                       (self.id, item_id, quantity))

    def remove_item(self, db: DatabaseManager, item_id: int, quantity: int):
        current = db.fetchone("SELECT Quantity FROM SHOP_INVENTORY WHERE ShopID = ? AND ItemID = ?", (self.id, item_id))
        if not current or current[0] < quantity:
            raise ValueError("Cannot remove that many items.")
        db.execute("UPDATE SHOP_INVENTORY SET Quantity = Quantity - ? WHERE ShopID = ? AND ItemID = ?",
                   (quantity, self.id, item_id))
        db.execute("DELETE FROM SHOP_INVENTORY WHERE Quantity <= 0 AND ShopID = ? AND ItemID = ?",
                   (self.id, item_id))

    def __repr__(self):
        return f"<Shop #{self.id}: {self.Owner}'s {self.ShopType} in {self.LocationName} with {self.Gold}g>"
