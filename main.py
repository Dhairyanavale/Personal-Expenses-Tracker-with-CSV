import csv
from collections import defaultdict
from datetime import datetime

FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]
CATEGORIES = ["Food", "Travel", "Study", "Bills", "Fun"]


def ensure_csv():
    try:
        with open(FILE, "r", newline="", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            with open(FILE, "w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, FIELDS).writeheader()
    except FileNotFoundError:
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, FIELDS).writeheader()


def save_expense(row):
    ensure_csv()
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, FIELDS).writerow(row)


def load_expenses():
    try:
        with open(FILE, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def parse_amount(raw):
    try:
        val = float(raw)
        if val != val or val in (float("inf"), float("-inf")):
            return None
        return val
    except (ValueError, TypeError):
        return None


def totals_by_category(rows):
    totals = defaultdict(float)
    for r in rows:
        amt = parse_amount(r.get("amount"))
        if amt is not None:
            totals[r["category"]] += amt
    return dict(totals)


def get_valid_date():
    while True:
        date_str = input("Date (YYYY-MM-DD): ").strip()
        if len(date_str) == 10:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                pass
        print("Use YYYY-MM-DD format, like 2026-10-12.")


def get_valid_category():
    print("Suggested categories:", ", ".join(CATEGORIES))
    while True:
        cat = input("Category: ").strip()
        if cat:
            return cat
        print("Category can't be empty.")


def get_valid_description():
    while True:
        desc = input("Description: ").strip()
        if desc:
            return desc
        print("Description can't be empty.")


def get_valid_amount():
    while True:
        raw = input("Amount: ").strip()
        amt = parse_amount(raw)
        if amt is None:
            print("Enter a valid number.")
            continue
        if amt < 0:
            print("Amount can't be negative.")
            continue
        return f"{amt:.2f}"


def add_expense():
    print("\nAdd a new expense")
    expense = {
        "date": get_valid_date(),
        "category": get_valid_category(),
        "description": get_valid_description(),
        "amount": get_valid_amount(),
    }
    save_expense(expense)
    print("Saved.")


def show_rows(rows):
    if not rows:
        print("No matching expenses.")
        return

    print(f"\n{'Date':<10}  {'Category':<12}  {'Description':<28}  {'Amount':>10}")
    print("-" * 68)
    for r in rows:
        amt = parse_amount(r.get("amount"))
        if amt is None:
            print(f"Skipping bad row in CSV: {r}")
            continue

        print(
            f"{r['date']:<10}  "
            f"{r['category'][:12]:<12}  "
            f"{r['description'][:28]:<28}  "
            f"{amt:>10.2f}"
        )


def filter_expenses(rows):
    print("\nFilter by:")
    print("1. Category")
    print("2. Month (YYYY-MM)")
    choice = input("Pick 1 or 2: ").strip()

    if choice == "1":
        target = input("Category name: ").strip().lower()
        matches = [r for r in rows if r["category"].lower() == target]
        show_rows(matches)
    elif choice == "2":
        month = input("Month (YYYY-MM): ").strip()
        matches = [r for r in rows if r["date"][:7] == month]
        show_rows(matches)
    else:
        print("Invalid choice.")


def show_summary(rows):
    valid_rows = [r for r in rows if parse_amount(r.get("amount")) is not None]
    if not valid_rows:
        print("\nNo valid expenses recorded yet.")
        return

    by_cat = totals_by_category(valid_rows)
    grand_total = sum(parse_amount(r["amount"]) or 0.0 for r in valid_rows)
    biggest = max(valid_rows, key=lambda r: parse_amount(r["amount"]) or 0.0)

    print("\n--- Summary ---")
    for cat, total in sorted(by_cat.items()):
        print(f"{cat:<14}: {total:.2f}")
    print(f"Grand total   : {grand_total:.2f}")
    print(
        f"Biggest spend : {parse_amount(biggest['amount']):.2f} "
        f"({biggest['description']} on {biggest['date']})"
    )


def main():
    ensure_csv()
    while True:
        print("\n1. Add")
        print("2. View all")
        print("3. Filter")
        print("4. Summary")
        print("5. Quit")

        choice = input("Choose an option (1-5): ").strip()
        rows = load_expenses()

        if choice == "1":
            add_expense()
        elif choice == "2":
            show_rows(rows)
        elif choice == "3":
            filter_expenses(rows)
        elif choice == "4":
            show_summary(rows)
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()