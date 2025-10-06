import csv
import json

CSV_FILE = 'tailwind_traders_retail_data.csv'
JSON_FILE = 'retail_json_by_product_flat.json'


# Read CSV and convert to list of dictionaries
with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    data = [row for row in reader]

# Write to JSON file as an array of objects
with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)