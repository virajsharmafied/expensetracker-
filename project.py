import datetime
import csv
import os


class Expense:
    def __init__(self, amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

    def __str__(self):
        return f"{self.date} | {self.category} | ${self.amount:.2f}"


class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.expenses = []
        self.filename = filename
        self.load_expenses()

    def add_expense(self, amount, category, date):
        exp = Expense(amount, category, date)
        self.expenses.append(exp)
        self.save_expenses()
        print(f"expense of ${amount:.2f} added in '{category}'")

    def view_expenses(self):
        if not self.expenses:
            print("no expenses recorded")
        else:
            print("\n--- all expenses ---")
            for idx, e in enumerate(self.expenses, start=1):
                print(f"{idx}. {e}")

    def total_expenses(self):
        total = sum(e.amount for e in self.expenses)
        print(f"\ntotal expenses: ${total:.2f}")

    def expenses_by_category(self, category):
        cat_exp = [e for e in self.expenses if e.category.lower() == category.lower()]
        if not cat_exp:
            print(f"no expenses found in category '{category}'")
        else:
            print(f"\n--- expenses in '{category}' ---")
            for e in cat_exp:
                print(e)
            print(f"subtotal: ${sum(e.amount for e in cat_exp):.2f}")

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            removed = self.expenses.pop(index)
            self.save_expenses()
            print(f"deleted: {removed}")
        else:
            print("invalid index")

    def sort_expenses(self, by="date"):
        if by == "amount":
            self.expenses.sort(key=lambda e: e.amount)
        elif by == "date":
            self.expenses.sort(key=lambda e: e.date)
        print(f"expenses sorted by {by}")

    def monthly_summary(self, year, month):
        summary = [e for e in self.expenses if e.date.startswith(f"{year}-{month:02d}")]
        if not summary:
            print("no expenses found for this month")
        else:
            print(f"\nsummary for {year}-{month:02d}")
            for e in summary:
                print(e)
            print(f"total: ${sum(e.amount for e in summary):.2f}")

    def save_expenses(self):
        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            for e in self.expenses:
                writer.writerow([e.amount, e.category, e.date])

    def load_expenses(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        amount, category, date = row
                        self.expenses.append(Expense(float(amount), category, date))


def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def menu():
    tracker = ExpenseTracker()
    while True:
        print("\n=== expense tracker menu ===")
        print("1. add expense")
        print("2. view all expenses")
        print("3. show total expenses")
        print("4. show expenses by category")
        print("5. delete an expense")
        print("6. sort expenses (by date/amount)")
        print("7. monthly summary")
        print("8. quit")

        choice = input("choose an option (1-8): ")

        if choice == "1":
            try:
                amount = float(input("enter amount: "))
                category = input("enter category: ")
                while True:
                    date_input = input("enter date (yyyy-mm-dd): ").strip()
                    if validate_date(date_input):
                        date = date_input
                        break
                    else:
                        print("invalid date format, try again")
                tracker.add_expense(amount, category, date)
            except ValueError:
                print("invalid input. amount must be a number")
        elif choice == "2":
            tracker.view_expenses()
        elif choice == "3":
            tracker.total_expenses()
        elif choice == "4":
            cat = input("enter category: ")
            tracker.expenses_by_category(cat)
        elif choice == "5":
            tracker.view_expenses()
            try:
                idx = int(input("enter expense number to delete: ")) - 1
                tracker.delete_expense(idx)
            except ValueError:
                print("invalid input")
        elif choice == "6":
            by = input("sort by 'date' or 'amount': ").strip().lower()
            tracker.sort_expenses(by)
        elif choice == "7":
            try:
                year = int(input("enter year (yyyy): "))
                month = int(input("enter month (1-12): "))
                tracker.monthly_summary(year, month)
            except ValueError:
                print("invalid year/month")
        elif choice == "8":
            print("goodbye")
            break
        else:
            print("invalid choice. please select 1-8")


if __name__ == "__main__":
    menu()
