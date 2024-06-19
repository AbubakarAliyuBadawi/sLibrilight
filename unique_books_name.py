import re

# Regular expression to match JSON key-value pairs with paths ending in 'text.txt'
pattern = re.compile(r'"([^"]+)":\s*"([^"]+/([^/]+)/text\.txt)"')

# Set to store unique book names
book_names = set()

try:
    # Open and read the file line by line
    with open('books-dump.txt', 'r') as file:  # Adjust filename if necessary
        for line in file:
            match = pattern.search(line)
            if match:
                book_name = match.group(3)  # The book name right before 'text.txt'
                book_names.add(book_name)

    # Open a new text file for writing the book names
    with open('book_names.txt', 'w') as output_file:
        for book_name in sorted(book_names):  # Sort if you need alphabetical order
            output_file.write(book_name + '\n')

    print("Book names have been saved to 'book_names.txt'.")

except FileNotFoundError:
    print("File not found. Please check the filename and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
