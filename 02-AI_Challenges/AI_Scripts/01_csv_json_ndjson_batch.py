import csv
import json

CSV_FILE = 'tailwind_traders_retail_data.csv'
JSON_FILE_ARRAY = 'retail_json_by_product_flat.json'  # Array format (current)
JSON_FILE_NDJSON = 'retail_json_by_product_flat.ndjson'  # NDJSON format (for Azure Search)
JSON_FILE_BATCH = 'retail_json_batch.json'  # Batch format (for Azure Search)
JSON_FILE_UPLOAD = 'retail_json_upload.json'  # Correct upload format with actions

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

# Write array format (current format)
with open(JSON_FILE_ARRAY, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Write NDJSON format (for Azure Search direct upload)
with open(JSON_FILE_NDJSON, 'w', encoding='utf-8') as f:
    for record in data:
        json.dump(record, f, ensure_ascii=False)
        f.write('\n')

# Write batch format (for Azure Search REST API)
batch_data = {"value": data}
with open(JSON_FILE_BATCH, 'w', encoding='utf-8') as f:
    json.dump(batch_data, f, indent=2, ensure_ascii=False)

# Write correct upload format with action metadata
upload_documents = []
for record in data:
    upload_doc = {
        "@search.action": "upload",
        **record  # Spread the record fields
    }
    upload_documents.append(upload_doc)

upload_data = {"value": upload_documents}
with open(JSON_FILE_UPLOAD, 'w', encoding='utf-8') as f:
    json.dump(upload_data, f, indent=2, ensure_ascii=False)

print(f"Converted {len(data)} records with character cleaning and unique IDs.")
print("Generated files:")
print(f"  - Array format: {JSON_FILE_ARRAY}")
print(f"  - NDJSON format: {JSON_FILE_NDJSON}")
print(f"  - Batch format: {JSON_FILE_BATCH}")
print(f"  - Upload format: {JSON_FILE_UPLOAD} (USE THIS FOR AZURE SEARCH)")