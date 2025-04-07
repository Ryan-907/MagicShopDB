import pyinputplus as pyip
from TableClasess import Shop, Item, Location, Owner, DatabaseManager

SIZES = {'Small': 1, 'Medium': 2, 'Large': 3}
CHARITABILITY = {'Cheap': 0, 'Average': 1, 'Charitable': 2}
RARITIES = ['Common', 'Uncommon', 'Rare', 'Legendary']
SHOP_TYPES = ['Potions', 'Weapons & Armor', 'Magic Items', 'General Store']

db = DatabaseManager("shop_inventory.db")


def get_list(column, table):
    data = db.fetchall(f"SELECT {column} FROM {table}")
    return [row[0] for row in data]



def generate_location():
    name = pyip.inputStr("Enter location name: ")
    size = SIZES[pyip.inputMenu(list(SIZES.keys()), numbered=True, prompt="\n")] 
    Location.create_new(db, name, size)
    print(f"Location '{name}' created.")


def generate_owner():
    name = pyip.inputStr("Enter owner name: ")
    charity = CHARITABILITY[pyip.inputMenu(list(CHARITABILITY.keys()), numbered=True, prompt="\n")]
    Owner.create_new(db, name, charity)
    print(f"Owner '{name}' created.")


def generate_item():
    name = pyip.inputStr("Enter item name: ")
    desc = pyip.inputStr("Enter description: ")
    rarity = pyip.inputMenu(RARITIES, numbered=True)
    category = pyip.inputStr("Enter item category: ")
    universal = pyip.inputYesNo("Is this item universal (can be sold by any shop)?") == "yes"
    item = Item.create_new(db, name, desc, rarity, category, int(universal))
    print(f"Item '{item.name}' added with ID {item.id}.")


def generate_shop():
    owner = pyip.inputMenu(get_list('Owner', 'OWNER'), "Select Owner:\n", numbered=True)
    location = pyip.inputMenu(get_list('LocationName', 'LOCATIONS'), "Select Location:\n", numbered=True)
    shop_type = pyip.inputMenu(SHOP_TYPES, "Select Shop Type:\n", numbered=True)
    size = db.fetchone("SELECT LocationSize FROM LOCATIONS WHERE LocationName = ?", (location,))[0]
    gold = size * 100
    shop = Shop.create_new(db, owner, location, shop_type, gold)
    print(f"Shop created: {shop}")




def update_location():
    old_name = pyip.inputMenu(get_list('LocationName', 'LOCATIONS'), "Select a location to update:\n", numbered=True)
    location = Location.load_from_db(db, old_name)

    new_name = pyip.inputStr("Enter new name (leave blank to keep current): ", blank=True)
    size_key = pyip.inputMenu(list(SIZES.keys()), numbered=True, blank=True, prompt="\n")
    new_size = SIZES[size_key] if size_key else None

    location.update(db, new_name or None, new_size)
    print(f"Location updated: {location}")


def update_owner():
    old_name = pyip.inputMenu(get_list('Owner', 'OWNER'), "Select an owner to update:\n", numbered=True)
    owner = Owner.load_from_db(db, old_name)

    new_name = pyip.inputStr("Enter new name (leave blank to keep current): ", blank=True)
    char_key = pyip.inputMenu(list(CHARITABILITY.keys()), numbered=True, blank=True, prompt="\n")
    new_charity = CHARITABILITY[char_key] if char_key else None

    owner.update(db, new_name or None, new_charity)
    print(f"Owner updated: {owner}")


def update_item():
    item_id = int(pyip.inputNum("Enter the Item ID to update: ", min=1))
    item = Item.load_from_db(db, item_id)

    new_name = pyip.inputStr("New name (leave blank to keep current): ", blank=True)
    new_desc = pyip.inputStr("New description (leave blank to keep current): ", blank=True)
    new_rarity = pyip.inputMenu(RARITIES, numbered=True, blank=True, prompt="\n")
    new_cat = pyip.inputStr("New category (leave blank to keep current): ", blank=True)
    new_universal = pyip.inputYesNo("Change universal flag? (leave blank = no change)", blank=True)

    item.name = new_name or item.name
    item.description = new_desc or item.description
    item.rarity = new_rarity or item.rarity
    item.category = new_cat or item.category
    if new_universal:
        item.universal = 1 if new_universal == "yes" else 0

    item.update(db)
    print(f"Item updated: {item}")




def select_shop() -> Shop:
    owner = pyip.inputMenu(get_list('Owner', 'OWNER'), "Select Owner:\n", numbered=True)
    shop_types = db.fetchall("SELECT ShopType FROM SHOP WHERE Owner = ?", (owner,))
    if not shop_types:
        raise ValueError("No shops found for this owner.")
    shop_type = pyip.inputMenu([s[0] for s in shop_types], "Select Shop Type:\n", numbered=True, blank=True)
    shop_id = db.fetchone("SELECT ShopID FROM SHOP WHERE Owner = ? AND ShopType = ?", (owner, shop_type))[0]
    return Shop.load_from_db(db, shop_id)


def shop_inventory_menu():
    shop = select_shop()
    print(shop)

    while True:
        action = pyip.inputMenu(["Buy", "Sell", "Add (No Sale)", "Remove (No Sale)", "Show Inventory", "Exit"], numbered=True)

        if action == "Exit":
            break

        if action == "Show Inventory":
            inventory = db.fetchall("""
                SELECT I.ItemName, S.Quantity, I.Rarity, I.Category
                FROM SHOP_INVENTORY S
                JOIN ITEM I ON S.ItemID = I.ItemID
                WHERE S.ShopID = ?
            """, (shop.id,))
            print(f"\n{shop.Owner}'s {shop.ShopType} Inventory:")
            for item in inventory:
                print(f"- {item[0]} x{item[1]} ({item[2]}, {item[3]})")
            print()
            continue  # Prevents it from asking for Item ID & Quantity

        # Fetch eligible items by shop type
        eligible_items = db.fetchall("""
            SELECT ItemID, ItemName FROM ITEM
            WHERE Category = ? OR Universal = 1
        """, (shop.ShopType,))
        item_names = [f"{row[1]} (ID {row[0]})" for row in eligible_items]

        if not item_names:
            print("No items available for this shop type.")
            continue

        selected_item = pyip.inputMenu(item_names, "Select Item:\n", numbered=True)
        item_id = int(selected_item.split("ID ")[1][:-1])
        quantity = int(pyip.inputNum("Enter Quantity: ", min=1))

        item = Item.load_from_db(db, item_id)
        price = item.base_price

        try:
            if action == "Buy":
                shop.buy_item(db, item_id, quantity, price)
                print(f"Bought {quantity}x {item.name}")
            elif action == "Sell":
                shop.sell_item(db, item_id, quantity, price)
                print(f"Sold {quantity}x {item.name}")
            elif action == "Add (No Sale)":
                shop.add_item(db, item_id, quantity)
                print(f"Added {quantity}x {item.name} (no cost)")
            elif action == "Remove (No Sale)":
                shop.remove_item(db, item_id, quantity)
                print(f"Removed {quantity}x {item.name} (no cost)")
        except ValueError as e:
            print("Error:", e)

        print()



# === Main Menu ===

def main():
    ACTIONS = {
        'Generate Location': generate_location,
        'Generate Owner': generate_owner,
        'Generate Item': generate_item,
        'Create Shop': generate_shop,
        'Update Location': update_location,
        'Update Owner': update_owner,
        'Update Item': update_item,
        'Open Shop': shop_inventory_menu
    }

    while True:
        print("\n--- Magic Shop Manager ---")
        choice = pyip.inputMenu(list(ACTIONS.keys()) + ['Exit'], numbered=True)
        if choice == 'Exit':
            print("Goodbye!")
            break
        ACTIONS[choice]()


if __name__ == "__main__":
    main()
