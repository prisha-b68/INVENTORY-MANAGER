# Shop Inventory Manager
# keeps track of products, stock and sales for a small shop

inventory = {}
sales_log = []
invoice_counter = 1


def get_non_empty_string(prompt):
    # keep asking until they actually type something
    while True:
        value = input(prompt)
        if value == '':
            print("This field cannot be empty.")
        else:
            return value


def get_positive_int(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        else:
            print("Please enter a valid whole number.")


def get_positive_float(prompt):
    while True:
        value = input(prompt)
        if value.replace(".", "", 1).isdigit():
            return float(value)
        else:
            print("Please enter a valid number.")


def add_product():
    print("\n--- Add Product ---")
    category = get_non_empty_string("Enter category (e.g. grocery, dairy): ").lower()
    product = get_non_empty_string("Enter product name: ").lower()

    if category in inventory and product in inventory[category]:
        print("'" + product + "' already exists. Use Restock instead.")
        return

    quantity = get_positive_int("Enter starting quantity: ")
    price = get_positive_float("Enter price per unit: ")
    min_stock = get_positive_int("Enter low-stock alert level: ")

    if category not in inventory:
        inventory[category] = {}

    inventory[category][product] = {"quantity": quantity, "price": price, "min_stock": min_stock}

    print("'" + product.title() + "' added under '" + category.title() + "'.")


def find_product(product_name):
    product_name = product_name.lower()
    for category in inventory:
        products = inventory[category]
        if product_name in products:
            return category, product_name
    return None, None


def view_inventory():
    print("\n--- Current Inventory ---")
    if not inventory:
        print("Inventory is empty.")
        return

    for category in inventory:
        products = inventory[category]
        if not products:
            continue
        print("\nCategory:", category.title())
        print("Product  Quantity  Price  Min Stock")
        for name in products:
            details = products[name]
            print(name.title(), details["quantity"], details["price"], details["min_stock"])


def sell_product():
    global invoice_counter

    print("\n--- Sell Product ---")
    if not inventory:
        print("Inventory is empty.")
        return

    customer = get_non_empty_string("Enter customer name: ")
    staff = get_non_empty_string("Enter staff name: ")
    product_input = get_non_empty_string("Enter product name to sell: ")

    category, product = find_product(product_input)
    if product is None:
        print("Product '" + product_input + "' not found.")
        return

    details = inventory[category][product]
    print("Available stock of '" + product.title() + "':", details["quantity"])
    qty = get_positive_int("Enter quantity to sell: ")

    if qty == 0:
        print("Sale cancelled (quantity was 0).")
        return

    if qty > details["quantity"]:
        print("Not enough stock. Only", details["quantity"], "units available.")
        return

    details["quantity"] = details["quantity"] - qty
    total = round(qty * details["price"], 2)

    sale_record = {
        "invoice_no": invoice_counter,
        "customer": customer,
        "staff": staff,
        "category": category,
        "product": product,
        "quantity": qty,
        "price": details["price"],
        "total": total
    }
    sales_log.append(sale_record)

    print_receipt(sale_record)

    if details["quantity"] <= details["min_stock"]:
        print("\n*** LOW STOCK ALERT:", product.title(), "is at", details["quantity"],
              "units (min level:", details["min_stock"], ") ***")

    invoice_counter += 1


def print_receipt(sale):
    print("\n------------------------------------------")
    print(shop_name.upper())
    print("------------------------------------------")
    print("Invoice No: INV-" + str(sale["invoice_no"]))
    print("Customer:", sale["customer"])
    print("Staff:", sale["staff"])
    print("Product:", sale["product"].title())
    print("Quantity:", sale["quantity"])
    print("Price per unit:", sale["price"])
    print("Grand Total:", sale["total"])
    print("------------------------------------------")
    print("Thank you for shopping!")


def restock_product():
    print("\n--- Restock Product ---")
    if not inventory:
        print("Inventory is empty.")
        return

    product_input = get_non_empty_string("Enter product name to restock: ")
    category, product = find_product(product_input)

    if product is None:
        print("Product '" + product_input + "' not found.")
        return

    add_qty = get_positive_int("Enter quantity to add: ")
    inventory[category][product]["quantity"] += add_qty
    new_qty = inventory[category][product]["quantity"]
    print("'" + product.title() + "' restocked. New quantity:", new_qty)


def search_product():
    print("\n--- Search Product ---")
    if not inventory:
        print("Inventory is empty.")
        return

    product_input = get_non_empty_string("Enter product name to search: ")
    category, product = find_product(product_input)

    if product is None:
        print("'" + product_input + "' was not found.")
        return

    details = inventory[category][product]
    print("\nFound '" + product.title() + "' in category '" + category.title() + "':")
    print("Quantity:", details["quantity"])
    print("Price:", details["price"])
    print("Min Stock:", details["min_stock"])


def check_low_stock():
    print("\n--- Low Stock Alerts ---")
    if not inventory:
        print("Inventory is empty.")
        return

    found_any = False
    for category in inventory:
        products = inventory[category]
        for name in products:
            details = products[name]
            if details["quantity"] <= details["min_stock"]:
                found_any = True
                print("[LOW STOCK]", name.title(), "(" + category.title() + "):",
                      details["quantity"], "left, min is", details["min_stock"])

    if found_any == False:
        print("No low stock items.")


def total_value():
    print("\n--- Total Inventory Value ---")
    if not inventory:
        print("Inventory is empty.")
        return

    grand_total = 0
    for category in inventory:
        products = inventory[category]
        category_total = 0
        for name in products:
            details = products[name]
            category_total = category_total + details["quantity"] * details["price"]
        print(category.title(), ":", category_total)
        grand_total = grand_total + category_total

    print("Grand Total:", grand_total)


def view_sales_log():
    print("\n--- Sales Log ---")
    if not sales_log:
        print("No sales have been made yet.")
        return

    print("Inv No  Product  Qty  Total")
    for sale in sales_log:
        print("INV-" + str(sale["invoice_no"]), sale["product"].title(), sale["quantity"], sale["total"])


def show_menu():
    print("\n----------------------------------------")
    print(shop_name.upper(), "- INVENTORY MANAGER")
    print("----------------------------------------")
    print("1. Add Product")
    print("2. View Inventory")
    print("3. Sell Product")
    print("4. Restock Product")
    print("5. Search Product")
    print("6. Check Low Stock")
    print("7. Total Inventory Value")
    print("8. View Sales Log")
    print("9. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            sell_product()
        elif choice == "4":
            restock_product()
        elif choice == "5":
            search_product()
        elif choice == "6":
            check_low_stock()
        elif choice == "7":
            total_value()
        elif choice == "8":
            view_sales_log()
        elif choice == "9":
            print("\nThank you for using " + shop_name + "'s Inventory Manager. Goodbye!")
            break
        else:
            print("Invalid choice.")


print("****************************************")
print("  WELCOME TO THE SHOP INVENTORY MANAGER")
print("****************************************")
shop_name = get_non_empty_string("Enter your shop name: ")
print("\nWelcome to " + shop_name + "!")
main()
