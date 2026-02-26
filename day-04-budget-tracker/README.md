# Day 4: Budget Tracker

A professional CLI-based personal finance tracker with category-based summaries and data visualization.

## Features
- Add expenses with amount, category, and description.
- Persistent JSON-based storage.
- Categorized summary of expenses.
- Visual pie chart generation for expense distribution.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Add an expense:
```bash
python budget_tracker.py add 15.50 Food "Lunch at Joe's"
```

Show summary:
```bash
python budget_tracker.py summary
```

Generate chart:
```bash
python budget_tracker.py plot
```
