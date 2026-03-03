import re

def test_regex(pattern, text):
    try:
        compiled_pattern = re.compile(pattern)
        matches = list(compiled_pattern.finditer(text))

        if not matches:
            print("No matches found.")
            return

        print("Matches found:")
        highlighted_text = list(text)
        for match in matches:
            start, end = match.span()
            # Highlight with carets below the match
            for i in range(start, end):
                if i < len(highlighted_text):
                    highlighted_text[i] = f'\033[92m{highlighted_text[i]}\033[0m' # Green color
            print(f"  - Match: '{match.group()}' (Start: {start}, End: {end})")
        
        print("\nHighlighted Text:")
        print("".join(highlighted_text))

    except re.error as e:
        print(f"Invalid regex pattern: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    print("--- Regex Pattern Tester ---")
    print("Enter your regex pattern and test strings. Type 'quit' to exit.")
    print("\nBuilt-in Cheat Sheet:")
    print("  .  - Any character (except newline)")
    print("  ^  - Start of string")
    print("  $  - End of string")
    print("  *  - Zero or more occurrences")
    print("  +  - One or more occurrences")
    print("  ?  - Zero or one occurrence")
    print("  {n} - Exactly n occurrences")
    print("  {n,} - n or more occurrences")
    print("  {n,m} - n to m occurrences")
    print("  [] - Character set (e.g., [abc])")
    print("  |  - OR (e.g., a|b)")
    print("  () - Grouping")
    print("  \\d - Digit (0-9)")
    print("  \\D - Non-digit")
    print("  \\w - Word character (a-z, A-Z, 0-9, _)")
    print("  \\W - Non-word character")
    print("  \\s - Whitespace character")
    print("  \\S - Non-whitespace character")
    print("  \\b - Word boundary")
    print("  \\B - Non-word boundary")

    while True:
        pattern = input("\nEnter regex pattern (or 'quit'): ")
        if pattern.lower() == 'quit':
            break
        
        text = input("Enter test string: ")
        test_regex(pattern, text)

if __name__ == "__main__":
    main()
