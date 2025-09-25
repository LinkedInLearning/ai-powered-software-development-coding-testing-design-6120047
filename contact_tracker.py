import json
import os
from typing import List, Dict, Optional

# Global variable to store contacts
contacts = []
CONTACTS_FILE = "contacts.json"

def display_menu():
    """Display the main menu options for the contact tracker."""
    print("\n" + "="*50)
    print("           CONTACT TRACKER")
    print("="*50)
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contacts")
    print("4. Delete Contact")
    print("5. Save Contacts to File")
    print("6. Load Contacts from File")
    print("7. Exit")
    print("="*50)

def add_contact():
    """Add a new contact to the contacts list."""
    print("\n--- ADD NEW CONTACT ---")
    
    name = input("Enter contact name: ").strip()
    if not name:
        print("Error: Name cannot be empty!")
        return
    
    phone = input("Enter phone number: ").strip()
    if not phone:
        print("Error: Phone number cannot be empty!")
        return
    
    email = input("Enter email address (optional): ").strip()
    address = input("Enter address (optional): ").strip()
    
    # Check if contact with same name already exists
    for contact in contacts:
        if contact['name'].lower() == name.lower():
            print(f"Error: Contact '{name}' already exists!")
            return
    
    # Create new contact
    new_contact = {
        'name': name,
        'phone': phone,
        'email': email if email else "N/A",
        'address': address if address else "N/A"
    }
    
    contacts.append(new_contact)
    print(f"✓ Contact '{name}' added successfully!")

def view_contacts():
    """Display all contacts in the list."""
    print("\n--- ALL CONTACTS ---")
    
    if not contacts:
        print("No contacts found. Add some contacts first!")
        return
    
    print(f"Total contacts: {len(contacts)}")
    print("-" * 60)
    
    for i, contact in enumerate(contacts, 1):
        print(f"{i}. Name: {contact['name']}")
        print(f"   Phone: {contact['phone']}")
        print(f"   Email: {contact['email']}")
        print(f"   Address: {contact['address']}")
        print("-" * 60)

def search_contacts():
    """Search for contacts by name or phone number."""
    print("\n--- SEARCH CONTACTS ---")
    
    if not contacts:
        print("No contacts found. Add some contacts first!")
        return
    
    search_term = input("Enter name or phone number to search: ").strip().lower()
    
    if not search_term:
        print("Error: Search term cannot be empty!")
        return
    
    found_contacts = []
    for contact in contacts:
        if (search_term in contact['name'].lower() or 
            search_term in contact['phone'].lower()):
            found_contacts.append(contact)
    
    if not found_contacts:
        print(f"No contacts found matching '{search_term}'")
        return
    
    print(f"\nFound {len(found_contacts)} contact(s):")
    print("-" * 60)
    
    for i, contact in enumerate(found_contacts, 1):
        print(f"{i}. Name: {contact['name']}")
        print(f"   Phone: {contact['phone']}")
        print(f"   Email: {contact['email']}")
        print(f"   Address: {contact['address']}")
        print("-" * 60)

def delete_contact():
    """Delete a contact from the list."""
    print("\n--- DELETE CONTACT ---")
    
    if not contacts:
        print("No contacts found. Add some contacts first!")
        return
    
    # Display contacts for selection
    print("Available contacts:")
    for i, contact in enumerate(contacts, 1):
        print(f"{i}. {contact['name']} - {contact['phone']}")
    
    try:
        choice = int(input("\nEnter the number of contact to delete: ")) - 1
        
        if 0 <= choice < len(contacts):
            deleted_contact = contacts.pop(choice)
            print(f"✓ Contact '{deleted_contact['name']}' deleted successfully!")
        else:
            print("Error: Invalid contact number!")
            
    except ValueError:
        print("Error: Please enter a valid number!")

def save_contacts_to_file():
    """Save contacts to a JSON file."""
    print("\n--- SAVE CONTACTS ---")
    
    if not contacts:
        print("No contacts to save!")
        return
    
    try:
        with open(CONTACTS_FILE, 'w') as file:
            json.dump(contacts, file, indent=2)
        print(f"✓ {len(contacts)} contact(s) saved to '{CONTACTS_FILE}' successfully!")
    except Exception as e:
        print(f"Error saving contacts: {e}")

def load_contacts_from_file():
    """Load contacts from a JSON file."""
    print("\n--- LOAD CONTACTS ---")
    
    if not os.path.exists(CONTACTS_FILE):
        print(f"File '{CONTACTS_FILE}' not found!")
        return
    
    try:
        with open(CONTACTS_FILE, 'r') as file:
            loaded_contacts = json.load(file)
        
        # Clear existing contacts and load new ones
        contacts.clear()
        contacts.extend(loaded_contacts)
        
        print(f"✓ {len(contacts)} contact(s) loaded from '{CONTACTS_FILE}' successfully!")
    except Exception as e:
        print(f"Error loading contacts: {e}")

def main():
    """Main application loop."""
    print("Welcome to Contact Tracker!")
    
    # Load existing contacts on startup
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r') as file:
                loaded_contacts = json.load(file)
                contacts.extend(loaded_contacts)
                print(f"Loaded {len(contacts)} existing contact(s).")
        except:
            print("Could not load existing contacts. Starting fresh.")
    
    while True:
        display_menu()
        
        try:
            choice = int(input("\nEnter your choice (1-7): "))
            
            if choice == 1:
                add_contact()
            elif choice == 2:
                view_contacts()
            elif choice == 3:
                search_contacts()
            elif choice == 4:
                delete_contact()
            elif choice == 5:
                save_contacts_to_file()
            elif choice == 6:
                load_contacts_from_file()
            elif choice == 7:
                print("\nThank you for using Contact Tracker!")
                break
            else:
                print("Error: Please enter a number between 1 and 7!")
                
        except ValueError:
            print("Error: Please enter a valid number!")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break

if __name__ == "__main__":
    main()
