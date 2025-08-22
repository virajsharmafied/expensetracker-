import csv
from datetime import datetime
from abc import ABC, abstractmethod

class Record(ABC):
    @abstractmethod
    def __str__(self):
        pass

class Expense(Record):
    def __init__(self, item, amount, category, date):
        self.__item = item
        self.__amount = amount
        self.__category = category
        self.__date = date

    @property
    def item(self):
        return self.__item

    @property
    def amount(self):
        return self.__amount

    @property
    def category(self):
        return self.__category

    @property
    def date(self):
        return self.__date

    def __str__(self):
        return f"{self.date} | {self.item} | {self.category} | {self.amount:.2f}"

    def __eq__(self, other):
        return (self.item, self.amount, self.category, self.date) == (other.item, other.amount, other.category, other.date)

class ExpenseTracker:
    def __init__(self, file="expenses.csv"):
        self.expenses = []
        self.file = file
        self.load_from_file()

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.save_to_file()

    def view_expenses(self):
        if not self.expenses:
            print("no expenses recorded")
        else:
            for e in self.expenses:
                print(e)

    def total_expenses(self):
        return sum(e.amount for e in self.expenses)

    def expenses_by_category(self, category):
        return [e for e in self.expenses if e.category.lower() == category.lower()]

    def monthly_report(self, year, month):
        return [e for e in self.expenses if e.date.startswith(f"{year}-{month:02d}")]

    def search_expenses(self, keyword):
        return [e for e in self.expenses if keyword.lower() in e.item.lower() or keyword.lower() in e.category.lower()]

    def sort_expenses(self, key):
        if key == "date":
            return sorted(self.expenses, key=lambda e: e.date)
        elif key == "amount":
            return sorted(self.expenses, key=lambda e: e.amount)
        elif key == "category":
            return sorted(self.expenses, key=lambda e: e.category.lower())
        else:
            return self.expenses

    def clear_expenses(self):
        confirm = input("are you sure you want to clear all expenses? (y/n): ")
        if confirm.lower() == "y":
            self.expenses = []
            with open(self.file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["item", "amount", "category", "date"])
            print("all expenses cleared")
        else:
            print("clear cancelled")

    def save_to_file(self):
        with open(self.file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["item", "amount", "category", "date"])
            for e in self.expenses:
                writer.writerow([e.item, e.amount, e.category, e.date])

    def load_from_file(self):
        try:
            with open(self.file, "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) == 4:
                        item, amount, category, date = row
                        self.expenses.append(Expense(item, float(amount), category, date))
        except FileNotFoundError:
            pass

def valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def main():
    tracker = ExpenseTracker()
    while True:
        print("\nexpense tracker menu")
        print("1. add expense")
        print("2. view all expenses")
        print("3. view total expenses")
        print("4. view expenses by category")
        print("5. monthly report")
        print("6. search expenses")
        print("7. sort expenses")
        print("8. clear all expenses")
        print("9. quit")

        choice = input("choose an option: ")

        if choice == "1":
            item = input("enter item name: ")
            amount = float(input("enter amount: "))
            category = input("enter category: ")
            date = input("enter date (yyyy-mm-dd): ")
            if valid_date(date):
                tracker.add_expense(Expense(item, amount, category, date))
                print("expense added")
            else:
                print("invalid date format")

        elif choice == "2":
            tracker.view_expenses()

        elif choice == "3":
            print("total expenses:", tracker.total_expenses())

        elif choice == "4":
            cat = input("enter category: ")
            results = tracker.expenses_by_category(cat)
            if results:
                for e in results:
                    print(e)
            else:
                print("no expenses found for this category")

        elif choice == "5":
            year = int(input("enter year (yyyy): "))
            month = int(input("enter month (1-12): "))
            results = tracker.monthly_report(year, month)
            if results:
                for e in results:
                    print(e)
            else:
                print("no expenses found for this month")

        elif choice == "6":
            keyword = input("enter keyword to search: ")
            results = tracker.search_expenses(keyword)
            if results:
                for e in results:
                    print(e)
            else:
                print("no matching expenses found")

        elif choice == "7":
            key = input("sort by (date/amount/category): ")
            results = tracker.sort_expenses(key)
            for e in results:
                print(e)

        elif choice == "8":
            tracker.clear_expenses()

        elif choice == "9":
            print("goodbye")
            break
        else:
            print("invalid choice")

if __name__ == "__main__":
    main()
