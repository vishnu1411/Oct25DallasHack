
import csv
import json

CSV_FILE = 'tailwind_traders_retail_data.csv'
JSON_FILE = 'retail_json_by_product.json'

grouped = {}
try:
    with open(CSV_FILE, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            product_name = row.get('ProductName')
            if not product_name:
                print(f"Warning: Missing ProductName in row: {row}")
                continue
            if product_name not in grouped:
                grouped[product_name] = []
            grouped[product_name].append(row)
    print(f"Total unique products: {len(grouped)}")
except Exception as e:
    print(f"Error reading CSV: {e}")

output = []
for product_name, records in grouped.items():
    output.append({
        'ProductName': product_name,
        'records': records
    })

try:
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)
    print(f"Output written to {JSON_FILE} with {len(output)} products.")
except Exception as e:
    print(f"Error writing JSON: {e}")