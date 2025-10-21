try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    exit(1)
    
import json
import time
import csv

def check_index_fields():
    """Check what fields are actually defined in the Azure Search index"""
    print("CHECKING INDEX FIELD DEFINITIONS...\n")
    
    service_name = "your-search-service-name"
    api_key = "your_azure_search_admin_key_here"
    
    headers = {'api-key': api_key}
    
    # Get index definition
    uri = f"https://{service_name}.search.windows.net/indexes/csv-retail-index?api-version=2021-04-30-Preview"
    
    try:
        response = requests.get(uri, headers=headers)
        if response.status_code == 200:
            index_def = response.json()
            fields = index_def.get('fields', [])
            
            print(f"INDEX FIELDS ({len(fields)} total):")
            field_types = {}
            for field in fields:
                field_name = field.get('name')
                field_type = field.get('type')
                searchable = field.get('searchable', False)
                field_types[field_name] = field_type
                print(f"  - {field_name} ({field_type}) {'[Searchable]' if searchable else ''}")
            
            return [f['name'] for f in fields], field_types
        else:
            print(f"Failed to get index definition: {response.status_code}")
            return None, None
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error checking index: {e}")
        return None, None

def check_csv_fields():
    """Check the actual fields in the CSV file"""
    print("\nCHECKING CSV FILE FIELDS...\n")
    
    try:
        with open('CSV_Optimized/retail_data_azure_fixed.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            csv_headers = next(reader)  # Get first row (headers)
            
        print(f"CSV HEADERS ({len(csv_headers)} total):")
        for i, header in enumerate(csv_headers):
            print(f"  {i+1}. {header}")
        
        return csv_headers
    except (FileNotFoundError, IOError, csv.Error) as e:
        print(f"Error reading CSV headers: {e}")
        return None

def upload_with_correct_fields(index_fields, field_types=None, csv_headers=None):
    """Upload CSV data using correct field mapping and types"""
    print("\nUPLOADING WITH CORRECT FIELD MAPPING AND TYPES...\n")
    
    # Use the provided field_types and csv_headers for validation
    if field_types:
        print(f"Available field types: {len(field_types)} fields")
    if csv_headers:
        print(f"CSV headers available: {len(csv_headers)} columns")
    
    service_name = "your-search-service-name"
    api_key = "your_azure_search_admin_key_here"

    try:
        # Read CSV data
        with open('CSV_Optimized/retail_data_azure_fixed.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        print(f"Found {len(rows)} records in CSV")
        
        # Take first 100 records for testing
        test_rows = rows[:100]
        print(f"Using first {len(test_rows)} records for test upload")
        
        # Create field mapping
        print("\nFIELD MAPPING (all fields as strings):")
        upload_docs = []
        
        for i, row in enumerate(test_rows):
            # Create document with only fields that exist in the index
            doc = {"@search.action": "upload"}
            
            # Map CSV fields to index fields - CONVERT ALL TO STRINGS since index expects strings
            if 'id' in index_fields:
                doc['id'] = str(row.get('id', f'doc_{i+1}')).strip()
            
            if 'CustomerID' in index_fields:
                doc['CustomerID'] = str(row.get('CustomerID', '')).strip()
            
            if 'ProductName' in index_fields:
                doc['ProductName'] = str(row.get('ProductName', '')).strip()
                
            if 'ProductCategory' in index_fields:
                doc['ProductCategory'] = str(row.get('ProductCategory', '')).strip()
            
            if 'CustomerName' in index_fields:
                doc['CustomerName'] = str(row.get('CustomerName', '')).strip()
                
            if 'EmailAddress' in index_fields:
                doc['EmailAddress'] = str(row.get('EmailAddress', '')).strip()
                
            if 'PurchaseDate' in index_fields:
                doc['PurchaseDate'] = str(row.get('PurchaseDate', '')).strip()
                
            if 'StoreLocation' in index_fields:
                doc['StoreLocation'] = str(row.get('StoreLocation', '')).strip()
                
            if 'Quantity' in index_fields:
                # Convert to string since index expects Edm.String
                doc['Quantity'] = str(row.get('Quantity', '0')).strip()
                    
            if 'UnitPrice' in index_fields:
                # Convert to string since index expects Edm.String
                doc['UnitPrice'] = str(row.get('UnitPrice', '0')).strip()
                    
            if 'TotalAmount' in index_fields:
                # Convert to string since index expects Edm.String
                doc['TotalAmount'] = str(row.get('TotalAmount', '0')).strip()
                    
            if 'PaymentMethod' in index_fields:
                doc['PaymentMethod'] = str(row.get('PaymentMethod', '')).strip()
                
            if 'LoyaltyTier' in index_fields:
                doc['LoyaltyTier'] = str(row.get('LoyaltyTier', '')).strip()
            
            upload_docs.append(doc)
        
        print(f"Prepared {len(upload_docs)} documents for upload")
        
        # Show first document as example
        if upload_docs:
            print("\nSAMPLE DOCUMENT (all values as strings):")
            for key, value in upload_docs[0].items():
                if key != '@search.action':
                    print(f"  {key}: '{value}' (type: {type(value).__name__})")
        
        # Upload to index
        upload_data = {"value": upload_docs}
        
        headers = {
            'Content-Type': 'application/json',
            'api-key': api_key
        }
        
        upload_uri = f"https://{service_name}.search.windows.net/indexes/csv-retail-index/docs/index?api-version=2021-04-30-Preview"
        
        print("\nUploading documents to index...")
        response = requests.post(upload_uri, headers=headers, data=json.dumps(upload_data))
        
        if response.status_code == 200:
            result = response.json()
            print("✅ UPLOAD SUCCESSFUL!")
            print(f"   Documents processed: {len(result.get('value', []))}")
            
            # Check for any errors
            success_count = 0
            for item in result.get('value', []):
                if item.get('status') == True:
                    success_count += 1
                else:
                    print(f"   ⚠️ Document {item.get('key')} error: {item.get('errorMessage', 'Unknown error')}")
            
            print(f"   Successfully uploaded: {success_count}/{len(result.get('value', []))} documents")
            
            print("Waiting 15 seconds for indexing...")
            time.sleep(15)
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except (requests.RequestException, FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"❌ Upload error: {e}")
        return False

def test_router_search():
    """Test Router search functionality"""
    print("\nTESTING ROUTER SEARCH...\n")
    
    service_name = "your-search-service-name"
    api_key = "your_azure_search_admin_key_here"
    
    # Check index document count
    headers = {'api-key': api_key}
    stats_uri = f"https://{service_name}.search.windows.net/indexes/csv-retail-index/stats?api-version=2021-04-30-Preview"
    
    try:
        response = requests.get(stats_uri, headers=headers)
        if response.status_code == 200:
            stats = response.json()
            doc_count = stats.get('documentCount', 0)
            print(f"CURRENT INDEX DOCUMENT COUNT: {doc_count:,}")
            
            if doc_count > 0:
                # Test Router search
                search_uri = f"https://{service_name}.search.windows.net/indexes/csv-retail-index/docs/search?api-version=2021-04-30-Preview"
                
                # Search for Router products
                search_body = {
                    "search": "Router",
                    "top": 10,
                    "searchFields": "ProductName",
                    "select": "ProductName,CustomerName,UnitPrice,StoreLocation"
                }
                
                search_response = requests.post(search_uri, 
                                              headers={'api-key': api_key, 'Content-Type': 'application/json'}, 
                                              data=json.dumps(search_body))
                
                if search_response.status_code == 200:
                    results = search_response.json()
                    router_results = results.get('value', [])
                    
                    print(f"ROUTER SEARCH RESULTS: {len(router_results)} found")
                    
                    if router_results:
                        print("\nROUTER PRODUCTS:")
                        for i, item in enumerate(router_results, 1):
                            print(f"{i}. Customer: {item.get('CustomerName', 'Unknown')}")
                            print(f"   Product: {item.get('ProductName', 'Unknown')}")
                            print(f"   Price: ${item.get('UnitPrice', 'Unknown')}")
                            print(f"   Store: {item.get('StoreLocation', 'Unknown')}")
                            print()
                        
                        print("🎉 SUCCESS! Azure Search Router functionality is working!")
                        print("Your multi-agent system can now search for Router and other products!")
                        return True
                    else:
                        print("No Router products found. Let's check all products...")
                        
                        # Try broader search
                        broad_search = {
                            "search": "*",
                            "top": 5,
                            "select": "ProductName,CustomerName"
                        }
                        
                        broad_response = requests.post(search_uri, 
                                                     headers={'api-key': api_key, 'Content-Type': 'application/json'}, 
                                                     data=json.dumps(broad_search))
                        
                        if broad_response.status_code == 200:
                            broad_results = broad_response.json()
                            print("SAMPLE PRODUCTS IN INDEX:")
                            for item in broad_results.get('value', [])[:5]:
                                print(f"  - {item.get('ProductName', 'Unknown')}")
                        else:
                            print(f"Broad search failed: {broad_response.status_code}")
                else:
                    print(f"Router search failed: {search_response.status_code}")
                    print(f"Error: {search_response.text}")
            else:
                print("No documents in index yet.")
        else:
            print(f"Stats check failed: {response.status_code}")
    
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Search test error: {e}")
    
    return False

if __name__ == "__main__":
    print("FIXED DIRECT UPLOAD FOR AZURE SEARCH (STRING TYPES)...\n")
    
    # Step 1: Check what fields are defined in the index
    available_fields, field_type_info = check_index_fields()
    
    if not available_fields:
        print("❌ Could not get index field definitions!")
        exit(1)
    
    # Step 2: Check CSV file structure
    csv_header_list = check_csv_fields()
    
    if not csv_header_list:
        print("❌ Could not read CSV headers!")
        exit(1)
    
    # Step 3: Upload with correct field mapping and string conversion
    upload_success = upload_with_correct_fields(available_fields, field_type_info, csv_header_list)
    
    if upload_success:
        # Step 4: Test Router search
        search_success = test_router_search()
        
        if search_success:
            print("\n" + "="*60)
            print("🎉 CONGRATULATIONS!")
            print("Azure Search is fully operational!")
            print("- Direct upload bypassed connection string issues")
            print("- Router search functionality confirmed")
            print("- Ready for multi-agent system integration")
            print("="*60)
        else:
            print("\nUpload succeeded but Router search needs verification.")
            print("Check the sample products listed above.")
    else:
        print("\n❌ Direct upload failed.")
        print("Try the Azure Portal approach:")
        print("1. Go to Azure Search 'aiscsearch'")
        print("2. Use Import Data wizard")
        print("3. Point to your CSV file in blob storage")
        print("4. Let Azure auto-detect fields")
    
    print("\n🏁 Fixed upload test completed!")