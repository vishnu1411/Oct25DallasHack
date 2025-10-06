import csv, json

docs = []
with open('tailwind_traders_challange2_data.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader, start=1):
        # Clean non-breaking spaces and strip whitespace
        product = row["Product"].replace('\u00a0', ' ').strip()
        suggestions = [
            row["AlsoBought1"].replace('\u00a0', ' ').strip(),
            row["AlsoBought2"].replace('\u00a0', ' ').strip(),
            row["AlsoBought3"].replace('\u00a0', ' ').strip()
        ]
        # Remove empty suggestions
        suggestions = [s for s in suggestions if s]
        doc = {
            "id": f"rec{idx}",
            "product": product,
            "suggestions": suggestions
        }
        docs.append(doc)

with open('recommendations.json', 'w', encoding='utf-8') as out:
    json.dump(docs, out, indent=2, ensure_ascii=False)