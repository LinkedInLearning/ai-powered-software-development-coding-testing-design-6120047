import csv
import os

CSV_FILE = 'expenses.csv'
FIELDS = ['name', 'amount', 'category']

def load_expenses():
    expenses = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                expenses.append(row)
    return expenses

def save_expense(expense):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(expense)

def list_expenses(expenses):
    if not expenses:
        print("No expenses recorded.")
        return
    print(f"{'Name':20} {'Amount':10} {'Category':15}")
    print("-" * 45)
    for exp in expenses:
        print(f"{exp['name']:20} {exp['amount']:10} {exp['category']:15}")

def add_expense():
    name = input("Expense name: ").strip()
    amount = input("Amount: ").strip()
    category = input("Category: ").strip()
    expense = {'name': name, 'amount': amount, 'category': category}
    save_expense(expense)
    print("Expense added.")

def delete_expense():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to delete.")
        return
    
    print("\nCurrent expenses:")
    list_expenses(expenses)
    
    name_to_delete = input("\nEnter the name of the expense to delete: ").strip()
    
    # Find and remove the expense
    original_count = len(expenses)
    expenses = [exp for exp in expenses if exp['name'].lower() != name_to_delete.lower()]
    
    if len(expenses) == original_count:
        print("Expense not found.")
        return
    
    # Rewrite the entire CSV file with remaining expenses
    if expenses:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(expenses)
    else:
        # Remove the file if no expenses remain
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
    
    print("Expense deleted successfully.")

def edit_expense():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to edit.")
        return
    
    print("\nCurrent expenses:")
    list_expenses(expenses)
    
    name_to_edit = input("\nEnter the name of the expense to edit: ").strip()
    
    # Find the expense to edit
    expense_found = False
    for i, exp in enumerate(expenses):
        if exp['name'].lower() == name_to_edit.lower():
            expense_found = True
            print(f"\nCurrent details:")
            print(f"Name: {exp['name']}")
            print(f"Amount: {exp['amount']}")
            print(f"Category: {exp['category']}")
            
            print("\nEnter new details (press Enter to keep current value):")
            new_name = input(f"New name [{exp['name']}]: ").strip()
            new_amount = input(f"New amount [{exp['amount']}]: ").strip()
            new_category = input(f"New category [{exp['category']}]: ").strip()
            
            # Update with new values or keep current ones
            expenses[i]['name'] = new_name if new_name else exp['name']
            expenses[i]['amount'] = new_amount if new_amount else exp['amount']
            expenses[i]['category'] = new_category if new_category else exp['category']
            
            # Rewrite the entire CSV file
            with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(expenses)
            
            print("Expense updated successfully.")
            break
    
    if not expense_found:
        print("Expense not found.")

def main():
    while True:
        print("\nExpense Tracker")
        print("1. List expenses")
        print("2. Add expense")
        print("3. Delete expense")
        print("4. Edit expense")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            expenses = load_expenses()
            list_expenses(expenses)
        elif choice == '2':
            add_expense()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            edit_expense()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()