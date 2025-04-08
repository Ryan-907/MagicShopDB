from TableClasess import Shop, Item, Location, Owner, DatabaseManager
from tkinter import messagebox
import tkinter as tk
import sqlite3

SIZES = {'Small': 1, 'Medium': 2, 'Large': 3}
CHARITABILITY = {'Cheap': 0, 'Average': 1, 'Charitable': 2}
RARITIES = ['Common', 'Uncommon', 'Rare', 'Legendary']
SHOP_TYPES = ['Potions', 'Weapons & Armor', 'Magic Items', 'General Store']
WINDOW_SIZE = '900x600'

db = DatabaseManager("shop_inventory.db")

def get_list(column, table):
    data = db.fetchall(f"SELECT {column} FROM {table}")
    return [row[0] for row in data]


def generate_location():
    location_window = tk.Toplevel()
    location_window.title('Creating New Location')
    location_window.geometry(WINDOW_SIZE)

    tk.Label(location_window, text='Enter Location Name').pack(pady=(10,0))
    loc_name_entry = tk.Entry(location_window)
    loc_name_entry.focus()
    loc_name_entry.pack(pady=5)

    tk.Label(location_window, text='Select Size').pack()
    size_var = tk.StringVar(location_window)
    size_var.set(next(iter(SIZES)))

    size_menu = tk.OptionMenu(location_window, size_var, *SIZES.keys())
    size_menu.pack(pady=5)

    def submit_location():
        name = loc_name_entry.get().strip()
        size_key = size_var.get()
        if not name:
            messagebox.showerror("Input error", "Location can't be null.")
            return
        size = SIZES[size_key]
        try:
            Location.create_new(db, name, size)
            messagebox.showinfo("Success", f"Location '{name} ({size})' created.")
            location_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Database Error", f"A location named '{name}' already exists.")


        location_window.destroy()
    
    tk.Button(location_window, text="Create location", command=submit_location).pack(pady=10)

def generate_owner():
    owner_window = tk.Toplevel()
    owner_window.title('Creating New Owner')
    owner_window.geometry(WINDOW_SIZE)
    
    tk.Label(owner_window, text='Enter Owner Name').pack(pady=(10,0))
    owner_name_entry = tk.Entry(owner_window)
    owner_name_entry.focus()
    owner_name_entry.pack(pady=5)

    tk.Label(owner_window, text='Select generosity').pack()
    char_var = tk.StringVar(owner_window)
    char_var.set(next(iter(CHARITABILITY)))
    char_menu = tk.OptionMenu(owner_window, char_var, *CHARITABILITY.keys())
    char_menu.pack(pady=5)

    def submit_owner():
        owner = owner_name_entry.get().strip()
        char_var_key = char_var.get()
        if not owner:
            messagebox.showerror("Input error", "Owner can't be null.")
            return
        charity = CHARITABILITY[char_var_key]
        try:
            Owner.create_new(db, owner, charity)
            messagebox.showinfo("Success", f"Owner '{owner} ({CHARITABILITY[char_var_key]})' created.")
            owner_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Database Error", f"Owner '{owner}' already exists.")

        owner_window.destroy()
    
    tk.Button(owner_window, text="Create owner", command=submit_owner).pack(pady=10)

def generate_item():
    item_window = tk.Toplevel()
    item_window.title('Creating New Item')
    item_window.geometry(WINDOW_SIZE)

    tk.Label(item_window, text='Enter item name').pack(pady=(10,0))
    item_name_entry = tk.Entry(item_window)
    item_name_entry.focus()
    item_name_entry.pack(pady=5)

    tk.Label(item_window, text='Description').pack()
    item_description_entry = tk.Text(item_window, height=5, width=40)
    item_description_entry.pack(pady=5)

    tk.Label(item_window, text='Select Item Rarity').pack()
    rarity_var = tk.StringVar(item_window)
    rarity_var.set(RARITIES[0]) 
    rarity_menu = tk.OptionMenu(item_window, rarity_var, *RARITIES) 
    rarity_menu.pack(pady=5)

    tk.Label(item_window, text='Select Item Category').pack()
    categroies = get_list('Category', 'SHOP_TYPE_ALLOWED_CATEGORIES')
    category_var = tk.StringVar(item_window)
    category_var.set(categroies[0])
    category_menu = tk.OptionMenu(item_window, category_var, *categroies)
    category_menu.pack(pady=5)

    universal_check = tk.IntVar()
    universal_check.set(0)
    check_box = tk.Checkbutton(
        item_window,
        text='Universal?',
        variable=universal_check,
        onvalue=1,
        offvalue=0
    )
    check_box.pack(pady=5)

    def submit_item():
        name = item_name_entry.get().strip()
        description = item_description_entry.get("1.0", "end-1c")
        rarity = rarity_var.get()
        category = category_var.get()
        universal = universal_check.get()

        if not name:
            messagebox.showerror('Error', 'Item must have name')
            return
        if not description:
            messagebox.showerror("Error", "Item must have description")
            return
        
        try:
            Item.create_new(db, name, description, rarity, category, universal)
            messagebox.showinfo("Success", f"{name} ({category}) created.")
            item_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Database Error", f"Owner '{name}' already exists.")

        item_window.destroy()

    tk.Button(item_window, text="Create item", command=submit_item).pack(pady=10)

def generate_shop():
    shop_window = tk.Toplevel()
    shop_window.title("Creating New Shop")
    shop_window.geometry(WINDOW_SIZE)

    tk.Label(shop_window, text='Select Owner').pack()
    owners = get_list('Owner', 'OWNER')
    owner_var = tk.StringVar(shop_window)
    owner_var.set(owners[0])
    owner_menu = tk.OptionMenu(shop_window, owner_var, *owners)
    owner_menu.pack(pady=5)

    tk.Label(shop_window, text='Select Location').pack()
    locations = get_list('LocationName', 'LOCATIONS')
    location_var = tk.StringVar(shop_window)
    location_var.set(locations[0])
    location_menu = tk.OptionMenu(shop_window, location_var, *locations)
    location_menu.pack(pady=5)

    tk.Label(shop_window, text='Select Shop Type').pack()
    location_type_var = tk.StringVar(shop_window)
    location_type_var.set(SHOP_TYPES[0])
    location_type_menu = tk.OptionMenu(shop_window, location_type_var, *SHOP_TYPES)
    location_type_menu.pack(pady=5)


    def submit_shop():
        size = db.fetchone("SELECT LocationSize FROM LOCATIONS WHERE LocationName = ?", (location_var,))[0]
        gold = size * 100
        owner = owner_var.get()
        location_name = location_var.get()
        location_type = location_type_var.get

        Shop.create_new(db, owner, location_name, location_type, gold)
        messagebox.showinfo("Success", f"{owner}'s {location_type} ({location_name}) created.")

        shop_window.destroy()

    tk.Button(shop_window, text="Create shop", command=submit_shop).pack()    

def update_location():
    update_loc_window = tk.Toplevel()
    update_loc_window.title("Updating Location")
    update_loc_window.geometry(WINDOW_SIZE)

    tk.Label(update_loc_window, text='Select Location to edit').pack()
    locations = get_list('LocationName', 'LOCATIONS')
    location_var = tk.StringVar(update_loc_window)
    location_var.set(locations[0])
    location_menu = tk.OptionMenu(update_loc_window, location_var, *locations)
    location_menu.pack(pady=5)

    tk.Label(update_loc_window, text='Enter new location name').pack(pady=(10,0))
    new_name_entry = tk.Entry(update_loc_window)
    new_name_entry.focus()
    new_name_entry.pack(pady=5)

    tk.Label(update_loc_window, text='Select new size').pack()
    new_size_var = tk.StringVar(update_loc_window)
    new_size_var.set(next(iter(SIZES)))
    new_size_menu = tk.OptionMenu(update_loc_window, new_size_var, *SIZES.keys())
    new_size_menu.pack(pady=5)

    def submit_updated_location():
        size = int(SIZES[new_size_var.get()]) 
        new_loc_name = new_name_entry.get()
        current_name = location_var.get()

        loc = Location.load_from_db(db=db, name=current_name)

        loc.update(db=db, new_name=new_loc_name, new_size=size)

        messagebox.showinfo("Success", f"{current_name} has been changed to {new_loc_name}")
        update_loc_window.destroy()


    tk.Button(update_loc_window, text="Update Shop", command=submit_updated_location).pack()    


if __name__=='__main__':
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry(WINDOW_SIZE)

    gen_loc_button = tk.Button(root, text='Generate Location', command=generate_location)
    gen_loc_button.pack()

    gen_owner_button = tk.Button(root, text='Generate Owner', command=generate_owner)
    gen_owner_button.pack()

    gen_item_button = tk.Button(root, text="Generate Item", command=generate_item)
    gen_item_button.pack()

    gen_shop_button = tk.Button(root, text="Generate shop", command=generate_shop)
    gen_shop_button.pack()

    update_location_button = tk.Button(root, text="Update location", command=update_location)
    update_location_button.pack()
    


    root.mainloop()