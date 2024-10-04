import json

def remove_duplicate_urls(data):
    seen_urls = set()
    unique_data = []
    
    for item in data:
        if item['url'] not in seen_urls:
            seen_urls.add(item['url'])
            unique_data.append(item)
    
    return unique_data

# File path
file_path = 'combined.json'

# Load JSON data from file
try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {file_path} does not contain valid JSON.")
    exit(1)

# Remove duplicates
unique_data = remove_duplicate_urls(data)

# Optionally, save the result to a new file
output_file_path = 'combined_truncated.json'
with open(output_file_path, 'w') as file:
    json.dump(unique_data, file, indent=2)

print(f"Unique data has been saved to {output_file_path}")
