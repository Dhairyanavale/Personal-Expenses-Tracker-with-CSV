# Personal Expenses Tracker

A menu-driven Python terminal application for recording daily expenses by category, saving them to a CSV file (`expenses.csv`) so they stay saved across restarts, filtering entries, and viewing spending summaries.

## Project Overview

This program uses only Python's built-in modules (`csv`, `collections`, and `datetime`) to store and analyze expenses from the terminal. Each expense has four fields:

- **`date`**: Formatted as `YYYY-MM-DD` (for example, `2026-10-03`)
- **`category`**: Category such as `Food`, `Travel`, `Study`, `Bills`, or `Fun` (or any non-empty category entered)
- **`description`**: Short note describing the expense
- **`amount`**: Non-negative number formatted to two decimal places when saved

Entries are stored in `expenses.csv` under the header `date,category,description,amount`. If `expenses.csv` does not exist yet or is empty, the program creates it automatically with the header row before writing rows.

## What You Need

- **Python 3.10 or newer** (no external libraries or `pip` installs needed)
- A terminal or editor (such as Windows Terminal or VS Code)
- Optional: A spreadsheet viewer (such as Google Sheets or LibreOffice Calc) to inspect `expenses.csv`

## How to Run (Line by Line)

1. Put `main.py` and `expenses.csv` in the same project folder (or let `main.py` create `expenses.csv` when you save your first expense).
2. Open your terminal (such as Windows Terminal) in that project folder.
3. Run the program by typing:

```bash
py main.py or python.py