from utils.file_handler import *
from utils.api_handler import *
from utils.report_generator import *

# Get data
raw_lines = read_sales_data('data/sales_data.txt')
transactions = parse_transactions(raw_lines)
valid, invalid, _ = validate_and_filter_transactions(transactions)

# Get enriched from Part 3
api_products = fetch_all_products()
mapping = create_product_mapping(api_products)
enriched = enrich_sales_data(valid, mapping)

# Generate report
generate_sales_report(valid, enriched)

print("✅ Part 4 Complete!")
