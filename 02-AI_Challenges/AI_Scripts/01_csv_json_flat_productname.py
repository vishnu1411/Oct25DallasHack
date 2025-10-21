import csv
import json

CSV_FILE = 'tailwind_traders_retail_data.csv'
JSON_FILE = 'retail_json_by_product_flat.json'

# Read CSV and convert to list of dictionaries with character cleaning
with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    data = []
    for idx, row in enumerate(reader, start=1):
        # Clean each field by removing non-breaking spaces and stripping whitespace
        cleaned_row = {}
        for key, value in row.items():
            if isinstance(value, str):
                # Remove non-breaking spaces (\u00a0) and strip whitespace
                cleaned_value = value.replace('\u00a0', ' ').strip()
                cleaned_row[key] = cleaned_value
            else:
                cleaned_row[key] = value
        
        # Add unique id field for Azure Search (required as key field)
        cleaned_row['id'] = f"record_{idx}"
        
        data.append(cleaned_row)

# Write to JSON file as an array of objects
with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Converted {len(data)} records from CSV to JSON with character cleaning and unique IDs applied.")