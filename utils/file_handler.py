# utils/file_handler.py
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns list of raw lines (strings), skipping header and empty lines.
    """
    try:
        # Try multiple encodings
        encodings = ['utf-8', 'latin-1', 'cp1252']
        raw_lines = []
        
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                raw_lines = [line.strip() for line in lines[1:] if line.strip()]  # Skip header, empty
                print(f"Successfully read {len(raw_lines)} transactions using {encoding}")
                return raw_lines
            except UnicodeDecodeError:
                continue
        
        print("Could not decode file with common encodings")
        return []
        
    except FileNotFoundError:
        print(f"File not found: {filename}. Ensure data/sales_data.txt exists.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    Handles commas in ProductName and numeric fields.
    """
    transactions = []
    
    for line in raw_lines:
        fields = line.split('|')
        if len(fields) != 8:
            continue  # Skip malformed rows
            
        TransactionID, Date, ProductID, ProductName, Quantity_str, UnitPrice_str, CustomerID, Region = fields
        
        # Clean ProductName: replace commas with space
        ProductName = ProductName.replace(',', ' ').strip()
        
        # Clean numerics: remove commas and convert
        try:
            Quantity = int(Quantity_str.replace(',', ''))
            UnitPrice = float(UnitPrice_str.replace(',', ''))
        except ValueError:
            continue  # Skip invalid numbers
            
        # Create dict
        transaction = {
            'Transaction_ID': TransactionID.strip(),
            'Date': Date.strip(),
            'Product_ID': ProductID.strip(),
            'Product_Name': ProductName,
            'Quantity': Quantity,
            'Unit_Price': UnitPrice,
            'Customer_ID': CustomerID.strip(),
            'Region': Region.strip()
        }
        transactions.append(transaction)
    
    print(f"Parsed {len(transactions)} valid transactions")
    return transactions

def validate_and_filter_transactions(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns (valid_transactions, invalid_count, filter_summary)
    """
    # Print available info
    if transactions:
        regions = list(set(t['Region'] for t in transactions if t['Region']))
        amounts = [t['Quantity'] * t['Unit_Price'] for t in transactions]
        print(f"Available Regions: {', '.join(regions)}")
        print(f"Transaction Amount Range: {min(amounts):,.0f} - {max(amounts):,.0f}")
    
    valid = []
    invalid_count = 0
    
    for t in transactions:
        # Validation rules
        amount = t['Quantity'] * t['Unit_Price']
        if (t['Quantity'] <= 0 or 
            t['Unit_Price'] <= 0 or 
            not t['Customer_ID'] or 
            not t['Region'] or 
            not t['Transaction_ID'].startswith('T')):
            invalid_count += 1
            continue
        
        # Filters
        if region and t['Region'] != region:
            invalid_count += 1
            continue
        if min_amount and amount < min_amount:
            invalid_count += 1
            continue
        if max_amount and amount > max_amount:
            invalid_count += 1
            continue
            
        valid.append(t)
    
    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': 1 if region else 0,
        'filtered_by_amount': 1 if min_amount or max_amount else 0,
        'final_count': len(valid)
    }
    
    print(f"Valid: {len(valid)}, Invalid: {invalid_count}")
    return valid, invalid_count, summary
