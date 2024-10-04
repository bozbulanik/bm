import json


file_path = 'TOBEFILTERED.json'
bookmarks = None
try:
    with open(file_path, 'r') as file:
        bookmarks = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {file_path} does not contain valid JSON.")
    exit(1)

def remove_bookmark_with_string(bookmarks, search_str):
    kept_bookmarks = []
    removed_bookmarks = []

    for bookmark in bookmarks:
        if search_str in bookmark['url']:
            removed_bookmarks.append(bookmark)
        else:
            kept_bookmarks.append(bookmark)
    
    for bookmark in removed_bookmarks:
        print(f"Title: {bookmark['title']}")
        print(f"URL: {bookmark['url']}")

    return kept_bookmarks
# Example usage
search_string = input("String to delete: ")
filtered_bookmarks = remove_bookmark_with_string(bookmarks, search_string)

# Print the updated bookmarks
with open('TOBEFILTERED.json', 'w') as json_file:
    json.dump(filtered_bookmarks, json_file, indent=4)
