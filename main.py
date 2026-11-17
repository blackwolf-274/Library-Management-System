import json
import os
from datetime import datetime

# File Constants
USERS_FILE = 'users.json'
BOOKS_FILE = 'books.json'
LOGS_FILE = 'logs.json'


# --- STORAGE & LOGGING ---
def load_data(filename):
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def log_action(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOGS_FILE, 'a') as file:
        file.write(f"[{timestamp}] {msg}\n")


# --- AUTHENTICATION ---
def create_account():
    print("\n--- CREATE ACCOUNT ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if not username or not password:
        print("[!] Username and password cannot be empty.\n")
        return

    users = load_data(USERS_FILE)
    if username in users:
        print("[!] Username already exists!\n")
        return

    users[username] = password
    save_data(USERS_FILE, users)
    log_action(f"Account created for {username}")
    print("[+] Account created successfully!\n")


def login():
    print("\n--- LOGIN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    users = load_data(USERS_FILE)
    if username in users and password == users[username]:
        print(f"[+] Welcome back, {username}!\n")
        log_action(f"{username} logged in")
        return username
    else:
        print("[!] Invalid credentials!\n")
        log_action(f"Failed login attempt for {username}")
        return None


# --- BOOK MANAGEMENT ---
def show_books(username):
    books = load_data(BOOKS_FILE)
    user_books = books.get(username, {})

    print(f"\n--- {username.upper()}'S BOOK SHELF ---")
    if not user_books:
        print("Your shelf is currently empty.\n")
        return

    for book_id, book in user_books.items():
        print(f"ID: {book_id} | Title: {book['title']} | Author: {book['author']} | Year: {book['year']}")
    print("-" * 45 + "\n")
    log_action(f"{username} listed books")


def add_books(username):
    print("\n--- ADD NEW BOOK ---")
    try:
        book_id = int(input("Book ID (number): ").strip())
    except ValueError:
        print("[!] Invalid ID. Please enter a valid number.\n")
        return

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year = input("Published Year: ").strip()

    if not title or not author:
        print("[!] Title and author cannot be empty.\n")
        return

    books = load_data(BOOKS_FILE)
    if username not in books:
        books[username] = {}

    books[username][str(book_id)] = {
        'id': book_id,
        'title': title,
        'author': author,
        'year': year
    }
    
    save_data(BOOKS_FILE, books)
    log_action(f"{username} added book '{title}'")
    print(f"[+] Added '{title}' to your shelf successfully!\n")


def update_books(username):
    show_books(username)
    books = load_data(BOOKS_FILE)
    user_books = books.get(username, {})

    if not user_books:
        return

    book_id = input("Enter Book ID to update: ").strip()
    if book_id not in user_books:
        print("[!] Invalid book ID.\n")
        log_action(f"{username} attempted to update non-existent book ID {book_id}")
        return

    current = user_books[book_id]
    print("\n(Leave blank to keep current value)")
    title = input(f"New Title [{current['title']}]: ").strip() or current['title']
    author = input(f"New Author [{current['author']}]: ").strip() or current['author']
    year = input(f"New Year [{current['year']}]: ").strip() or current['year']

    user_books[book_id] = {
        'id': book_id,
        'title': title,
        'author': author,
        'year': year
    }
    
    save_data(BOOKS_FILE, books)
    log_action(f"{username} updated book ID {book_id}")
    print(f"[+] Book ID {book_id} updated successfully!\n")


def delete_books(username):
    show_books(username)
    books = load_data(BOOKS_FILE)
    user_books = books.get(username, {})

    if not user_books:
        return

    book_id = input("Enter Book ID to delete: ").strip()
    if book_id in user_books:
        deleted_book = user_books.pop(book_id)
        save_data(BOOKS_FILE, books)
        print(f"[+] Deleted book '{deleted_book['title']}' (ID: {book_id})\n")
        log_action(f"{username} deleted book ID {book_id}")
    else:
        print("[!] Invalid book ID.\n")
        log_action(f"{username} attempted to delete non-existent book ID {book_id}")


# --- DASHBOARD & MAIN ---
def dashboard(username):
    while True:
        print(f"=== LIBRARY DASHBOARD ({username}) ===")
        print("1. Show books")
        print("2. Add book")
        print("3. Update book")
        print("4. Delete book")
        print("5. Logout")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            show_books(username)
        elif choice == '2':
            add_books(username)
        elif choice == '3':
            update_books(username)
        elif choice == '4':
            delete_books(username)
        elif choice == '5':
            log_action(f"{username} logged out")
            print(f"Logging out, goodbye {username}!\n")
            break
        else:
            print("[!] Invalid choice. Please enter a number between 1 and 5.\n")


def main():
    while True:
        print("==================================")
        print("   LIBRARY MANAGEMENT SYSTEM      ")
        print("==================================")
        print("1. Create account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            create_account()
        elif choice == '2':
            username = login()
            if username:
                dashboard(username)
        elif choice == '3':
            print("Exiting application. Goodbye!\n")
            break
        else:
            print("[!] Invalid choice. Please enter 1, 2, or 3.\n")


if __name__ == '__main__':
    main()