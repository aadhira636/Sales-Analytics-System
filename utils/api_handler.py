# utils/api_handler.py
import requests # type: ignore
import os
import re

def fetch_all_products():
    """Fetch all products from DummyJSON API"""
    try:
        url = "https://dummyjson.com/products?limit=100"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        products = data['products']
        print(f"Fetched {len(products)} products from API")
        return products
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def create_product_mapping(api_products):
    """Create dict mapping numeric product ID to product info"""
    mapping = {}
    for product in api_products:
        product_id = str(product['id'])  # P101 → '101'
        mapping[product_id] = {
            'title': product['title'],
            'category': product['category'],
            'brand': product.get('brand', 'Unknown'),
            'price': product['price'],
            'rating': product['rating']
        }
    print(f"Created mapping for {len(mapping)} product IDs")
    return mapping

def extract_numeric_id(product_id):
    """Extract number from Product_ID like P101 → 101, P5 → 5"""
    match = re.search(r'(\d+)', product_id)
    return match.group(1) if match else None

def enrich_sales_data(transactions, product_mapping):
    """Add API data to transactions, save enriched to data/enriched_sales_data.txt"""
    enriched = []
    
    for t in transactions:
        enriched_t = t.copy()
        numeric_id = extract_numeric_id(t['Product_ID'])
        
        if numeric_id and numeric_id in product_mapping:
            api_data = product_mapping[numeric_id]
            enriched_t.update({
                'API_Category': api_data['category'],
                'API_Brand': api_data['brand'],
                'API_Rating': api_data['rating'],
                'API_Match': True
            })
            print(f"✅ Enriched {t['Product_ID']} → {api_data['title']}")
        else:
            enriched_t.update({
                'API_Category': None,
                'API_Brand': None,
                'API_Rating': None,
                'API_Match': False
            })
            print(f"❌ No match for {t['Product_ID']}")
        
        enriched.append(enriched_t)
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    save_enriched_data(enriched, 'data/enriched_sales_data.txt')
    
    success_rate = sum(1 for t in enriched if t['API_Match']) / len(enriched) * 100
    print(f"Enriched {len(enriched)} transactions ({success_rate:.1f}% success)")
    
    return enriched

def save_enriched_data(enriched_transactions, filename):
    """Save enriched data as pipe-delimited file"""
    header = "Transaction_ID|Date|Product_ID|Product_Name|Quantity|Unit_Price|Customer_ID|Region|API_Category|API_Brand|API_Rating|API_Match"
    
    with open(filename, 'w') as f:
        f.write(header + '\n')
        for t in enriched_transactions:
            line = '|'.join([
                str(t.get('Transaction_ID', '')),
                str(t.get('Date', '')),
                str(t.get('Product_ID', '')),
                str(t.get('Product_Name', '')),
                str(t.get('Quantity', '')),
                str(t.get('Unit_Price', '')),
                str(t.get('Customer_ID', '')),
                str(t.get('Region', '')),
                str(t.get('API_Category', '')),
                str(t.get('API_Brand', '')),
                str(t.get('API_Rating', '')),
                str(t.get('API_Match', ''))
            ])
            f.write(line + '\n')
    
    print(f"Saved enriched data to {filename}")
