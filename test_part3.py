from utils.file_handler import *
from utils.data_processor import *
from utils.api_handler import *
import os

print("=== PART 3: API INTEGRATION ===")

# Get clean data
raw_lines = read_sales_data('data/sales_data.txt')
transactions = parse_transactions(raw_lines)
valid, invalid, _ = validate_and_filter_transactions(transactions)

# Part 3
api_products = fetch_all_products()
product_mapping = create_product_mapping(api_products)
enriched = enrich_sales_data(valid, product_mapping)

print("✅ Part 3 Complete! Check data/enriched_sales_data.txt")
