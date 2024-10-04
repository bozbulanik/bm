import uuid
import json
# Original list
bookmarks = None
file_path = 'UNIQUE_BOOKMARKS.json'

try:
    with open(file_path, 'r') as file:
        bookmarks = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {file_path} does not contain valid JSON.")
    exit(1)

# Add a unique 'id' field to each element
for bookmark in bookmarks:
    bookmark["id"] = str(uuid.uuid4())  # Generate a unique UUID for each bookmark

with open('UNIQUE_BOOKMARKS.json', 'w') as outfile:
    json.dump(bookmarks, outfile, indent=4)

