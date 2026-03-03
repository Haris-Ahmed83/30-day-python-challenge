# Day 10 - Regex Pattern Tester

This project is an interactive command-line tool for testing regular expressions. It allows users to input a regex pattern and a test string, then highlights all matches found within the string.

## Features

- **Interactive Testing:** Easily test different regex patterns against various strings.
- **Match Highlighting:** Visualizes where the regex matches within the test string.
- **Built-in Cheat Sheet:** Provides a quick reference for common regex syntax.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Haris-Ahmed83/30-day-python-challenge.git
    cd 30-day-python-challenge/Day_10_Regex_Pattern_Tester
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **No external dependencies are required for this project.**

## Usage

Run the script from your terminal:

```bash
python regex_tester.py
```

Follow the prompts to enter your regex pattern and test string. Type `quit` to exit the application.

Example:

```
--- Regex Pattern Tester ---
Enter your regex pattern and test strings. Type 'quit' to exit.

Built-in Cheat Sheet:
  .  - Any character (except newline)
  ^  - Start of string
  $  - End of string
  *  - Zero or more occurrences
  +  - One or more occurrences
  ?  - Zero or one occurrence
  {n} - Exactly n occurrences
  {n,} - n or more occurrences
  {n,m} - n to m occurrences
  [] - Character set (e.g., [abc])
  |  - OR (e.g., a|b)
  () - Grouping
  \d - Digit (0-9)
  \D - Non-digit
  \w - Word character (a-z, A-Z, 0-9, _)
  \W - Non-word character
  \s - Whitespace character
  \S - Non-whitespace character
  \b - Word boundary
  \B - Non-word boundary

Enter regex pattern (or 'quit'): \d+
Enter test string: My phone number is 123-456-7890.
Matches found:
  - Match: '123' (Start: 18, End: 21)
  - Match: '456' (Start: 22, End: 25)
  - Match: '7890' (Start: 26, End: 30)

Highlighted Text:
My phone number is \033[92m1\033[0m\033[92m2\033[0m\033[92m3\033[0m-\033[92m4\033[0m\033[92m5\033[0m\033[92m6\033[0m-\033[92m7\033[0m\033[92m8\033[0m\033[92m9\033[0m\033[92m0\033[0m.
```

---
*Created by Manus AI*
