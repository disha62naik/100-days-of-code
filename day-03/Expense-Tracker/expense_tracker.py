import os

FILE_NAME = "expenses.txt"


# --------- Add Expense ---------
def add_expense():
    name = input("Enter expense name: ")
    amount = input("Enter amount: ")

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    with open(FILE_NAME, "a") as file:
        file.write(f"{name},{amount}\n")

    print("Expense added successfully!\n")


# --------- View Expenses ---------
def view_expenses():
    if not os.path.exists(FILE_NAME):
        print("No expenses recorded yet.\n")
        return

    print("\n--- Expense List ---")
    with open(FILE_NAME, "r") as file:
        for line in file:
            name, amount = line.strip().split(",")
            print(f"{name} - ₹{amount}")
    print()


# --------- Calculate Total ---------
def calculate_total():
    if not os.path.exists(FILE_NAME):
        print("No expenses recorded yet.\n")
        return

    total = 0

    with open(FILE_NAME, "r") as file:
        for line in file:
            _, amount = line.strip().split(",")
            total += float(amount)

    print(f"\nTotal Spending: ₹{total}\n")


# --------- Main Menu ---------
def main():
    while True:
        print("===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Spending")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            calculate_total()
        elif choice == "4":
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
