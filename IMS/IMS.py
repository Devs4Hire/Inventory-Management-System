import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    products_df = pd.read_csv('products.csv')
    transactions_df = pd.read_csv('transaction.csv')
    inventory_df = pd.read_csv('inventory.csv')
    admin_df = pd.read_csv('admin.csv')
    return products_df, transactions_df, inventory_df, admin_df

def save_data(products_df, transactions_df, inventory_df):
    products_df.to_csv('products.csv', index=False)
    transactions_df.to_csv('transaction.csv', index=False)
    inventory_df.to_csv('inventory.csv', index=False)
    admin_df.to_csv('admin.csv', index=False)

def admin_password_check():
    entered_id = int(input("Enter admin ID: "))
    entered_password = input("Enter admin Password: ")
    if ((admin_df['ID'] == entered_id) & (admin_df['Password'] == entered_password)).any():
        return True
    else:
        print("Incorrect password. Access denied.")
        return False

def add_storage(storage_name):
    new_storage = pd.DataFrame({'storage_name': [storage_name]})
    inventory_df = pd.read_csv('inventory.csv')
    inventory_df = pd.concat([inventory_df, new_storage], ignore_index=True)
    save_data(products_df, transactions_df, inventory_df)
    print(f"Storage '{storage_name}' added successfully.")

def add_items(product_name, quantity, storage_name):
    products_df = pd.read_csv('products.csv')
    inventory_df = pd.read_csv('inventory.csv')

    if product_name not in products_df['product_name'].values:
        print(f"Product '{product_name}' not found. Add the product first.")
        return

    if storage_name not in inventory_df['storage_name'].values:
        print(f"Storage '{storage_name}' not found. Add the storage first.")
        return

    transaction_data = {'product_name': [product_name], 'quantity': [quantity], 'storage_name': [storage_name]}
    transaction_df = pd.DataFrame(transaction_data)
    transactions_df = pd.concat([transactions_df, transaction_df], ignore_index=True)

    inventory_df.loc[(inventory_df['product_name'] == product_name) & (inventory_df['storage_name'] == storage_name),
                     'quantity_in_stock'] += quantity

    save_data(products_df, transactions_df, inventory_df)
    print(f"{quantity} units of '{product_name}' added to '{storage_name}'.")

def delete_items(product_name, quantity, storage_name):
    inventory_df = pd.read_csv('inventory.csv')

    if storage_name not in inventory_df['storage_name'].values:
        print(f"Storage '{storage_name}' not found.")
        return

    if product_name not in inventory_df.loc[inventory_df['storage_name'] == storage_name, 'product_name'].values:
        print(f"Product '{product_name}' not found in storage '{storage_name}'.")
        return

    current_quantity = inventory_df.loc[(inventory_df['product_name'] == product_name) & (inventory_df['storage_name'] == storage_name),
                                        'quantity_in_stock'].values[0]

    if quantity > current_quantity:
        print(f"Cannot delete {quantity} units of '{product_name}' from '{storage_name}'. Insufficient quantity.")
        return

    transactions_df = pd.read_csv('transactions.csv')
    transaction_data = {'product_name': [product_name], 'quantity': [-quantity], 'storage_name': [storage_name]}
    transaction_df = pd.DataFrame(transaction_data)
    transactions_df = pd.concat([transactions_df, transaction_df], ignore_index=True)

    inventory_df.loc[(inventory_df['product_name'] == product_name) & (inventory_df['storage_name'] == storage_name),
                     'quantity_in_stock'] -= quantity

    save_data(products_df, transactions_df, inventory_df)
    print(f"{quantity} units of '{product_name}' deleted from '{storage_name}'.")

def delete_storage(storage_name):
    inventory_df = pd.read_csv('inventory.csv')

    if storage_name not in inventory_df['storage_name'].values:
        print(f"Storage '{storage_name}' not found.")
        return

    inventory_df = inventory_df[inventory_df['storage_name'] != storage_name]
    save_data(products_df, transactions_df, inventory_df)
    print(f"Storage '{storage_name}' deleted successfully.")

def view_inventory():
    inventory_df = pd.read_csv('inventory.csv')
    print("Current Inventory:")
    print(inventory_df)

# Main function
def main():
    if admin_password_check():
        while True:
            print("\nMenu:")
            print("1. Add Storage")
            print("2. Add Items")
            print("3. Delete Items")
            print("4. Delete Storage")
            print("5. View Inventory")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                storage_name = input("Enter the name of the new storage: ")
                add_storage(storage_name)
            elif choice == '2':
                product_name = input("Enter the product name: ")
                quantity = int(input("Enter the quantity to add: "))
                storage_name = input("Enter the storage name: ")
                add_items(product_name, quantity, storage_name)
            elif choice == '3':
                product_name = input("Enter the product name: ")
                quantity = int(input("Enter the quantity to delete: "))
                storage_name = input("Enter the storage name: ")
                delete_items(product_name, quantity, storage_name)
            elif choice == '4':
                storage_name = input("Enter the name of the storage to delete: ")
                delete_storage(storage_name)
            elif choice == '5':
                view_inventory()
            elif choice == '6':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    products_df, transactions_df, inventory_df, admin_df = load_data()
    main()
