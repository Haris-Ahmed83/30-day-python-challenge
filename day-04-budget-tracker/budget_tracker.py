import json
import os
import argparse
from datetime import datetime
import matplotlib.pyplot as plt

class BudgetTracker:
    def __init__(self, filename='budget_data.json'):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"expenses": []}
        return {"expenses": []}

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_expense(self, amount, category, description):
        expense = {
            "amount": float(amount),
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data["expenses"].append(expense)
        self.save_data()
        print(f"Added expense: ${amount:.2f} for {category} ({description})")

    def show_summary(self):
        if not self.data["expenses"]:
            print("No expenses recorded yet.")
            return

        summary = {}
        total = 0
        for expense in self.data["expenses"]:
            cat = expense.get("category", "Uncategorized")
            amt = expense.get("amount", 0)
            summary[cat] = summary.get(cat, 0) + amt
            total += amt

        print("\n--- Budget Summary ---")
        for cat, amt in summary.items():
            print(f"{cat}: ${amt:.2f} ({(amt/total)*100:.1f}%)")
        print(f"Total: ${total:.2f}\n")

    def plot_summary(self):
        if not self.data["expenses"]:
            print("No expenses to plot.")
            return

        summary = {}
        for expense in self.data["expenses"]:
            cat = expense.get("category", "Uncategorized")
            amt = expense.get("amount", 0)
            summary[cat] = summary.get(cat, 0) + amt

        categories = list(summary.keys())
        amounts = list(summary.values())

        plt.figure(figsize=(10, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Expense Distribution by Category')
        plt.axis('equal')
        plt.savefig('budget_summary.png')
        print("Summary chart saved as 'budget_summary.png'")

def main():
    parser = argparse.ArgumentParser(description="Professional Budget Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add expense
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("amount", type=float, help="Amount spent")
    add_parser.add_argument("category", type=str, help="Expense category (e.g., Food, Rent, Travel)")
    add_parser.add_argument("description", type=str, help="Short description")

    # Show summary
    subparsers.add_parser("summary", help="Show textual summary of expenses")

    # Plot summary
    subparsers.add_parser("plot", help="Generate a pie chart of expenses")

    args = parser.parse_args()
    tracker = BudgetTracker()

    if args.command == "add":
        tracker.add_expense(args.amount, args.category, args.description)
    elif args.command == "summary":
        tracker.show_summary()
    elif args.command == "plot":
        tracker.plot_summary()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
