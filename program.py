#!/usr/bin/env python3
"""
run with:
chmod +x expense_tracker.py
mv expense_tracker.py ~/bin/expense-tracker
"""

import argparse
import json
from datetime import date
FILENAME = "expenses.json"

def id_numbers():
    try:
        with open(FILENAME, "r") as f:
            expenses = json.load(f)
            if expenses:
                return max(item["id_number"] for item in expenses) + 1
            return 1
    except FileNotFoundError:
        return 1

def add_expense(amount, description):
    try:
        try:
            with open(FILENAME, "r") as f:
                expenses = json.load(f)
        except FileNotFoundError:
            expenses = []
        expenses.append({
                "id_number": id_numbers(),
                "amount": amount,
                "description": description,
                "date": date.today().strftime("%d %B %Y")
            })
        print(f"Added expense: {description}, ID : {expenses[-1]['id_number']}")
        with open(FILENAME, "w") as f:
            json.dump(expenses, f, indent=4)
    except Exception as e:
        print(f"Error adding expense: {e}")

def list_expenses():
    try:
        with open(FILENAME, "r") as f:
            expenses = json.load(f)
            for expense in expenses:
                print(f"ID: {expense['id_number']}, Amount: {expense['amount']}, Description: {expense['description']}, Date: {expense['date']}")
            print()
    except Exception as e:
        print(f"Error listing expenses: {e}")

def expense_summary(month=None):
    month_summary = 0
    try:
        with open(FILENAME, "r") as f:
            expenses = json.load(f)
            if month != None:
                for e in expenses:
                    if month.lower() in e["date"].lower():
                        month_summary += e["amount"]
            elif month == None:
                month_summary = sum(e["amount"] for e in expenses)
            print(f"Total expenses for {month}: {month_summary}")
    except Exception as e:
        print(f"Error summarizing expenses: {e}")
def delete_expense(id_num):
    try:
        with open(FILENAME, "r") as f:
            expenses = json.load(f)
            expenses = [e for e in expenses if e["id_number"] != id_num]
            with open(FILENAME, "w") as f:
                json.dump(expenses, f, indent=4)
                print(f"Deleted expense with ID: {id_num}")
    except Exception as e:
        print(f"Error deleting expense: {e}")

def main():

    parser = argparse.ArgumentParser(description="expense-tracker")
    subparsers = parser.add_subparsers(dest="command")

    #add parser
     
    add_parser = subparsers.add_parser("add", help="add an expense")
    add_parser.add_argument("--amount", type=int, required=True, help="set the amount of the expense")
    add_parser.add_argument("--description", type=str, required=True, help="set the description of the expense")

    #list parser

    list_parser = subparsers.add_parser("list", help="list all expenses")

    #summary parser

    summary_parser = subparsers.add_parser("summary", help="show a summary of expenses")
    summary_parser.add_argument("--month", type=str, required=False, help="set the month for the summary")

    #delete parser

    delete_parser = subparsers.add_parser("delete", help="delete an expense")
    delete_parser.add_argument("--id", type=int, required=True, help="set the id of the expense to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.amount, args.description)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        expense_summary(args.month)
    elif args.command == "delete":
        delete_expense(args.id)

if __name__ == "__main__":
    main()
