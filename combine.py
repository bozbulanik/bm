import json

# Load the first JSON file
with open('db.json', 'r') as f1:
    data1 = json.load(f1)

# Load the second JSON file
with open('extracted_old.json', 'r') as f2:
    data2 = json.load(f2)

# Combine the two lists
combined_data = data1 + data2

# Write the combined data to a new JSON file
with open('combined2full.json', 'w') as outfile:
    json.dump(combined_data, outfile, indent=4)
