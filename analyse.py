import json
from urllib.parse import urlparse
from collections import Counter

file_path = 'filtered_bookmarks.json'
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


domains = [urlparse(bookmark["url"]).netloc for bookmark in bookmarks]

# Count the occurrences of each domain
domain_count = Counter(domains)

top_domains = domain_count.most_common()

# Output the results
for x, (domain, count) in enumerate(top_domains):
    print(f"Website: {domain}, Count: {count}")
    if(x == 10):
        break
