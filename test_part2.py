from utils.file_handler import *
from utils.data_processor import *

# Get clean data from Part 1
raw_lines = read_sales_data('data/sales_data.txt')
transactions = parse_transactions(raw_lines)
valid, invalid, summary = validate_and_filter_transactions(transactions)

print("=== PART 2 TESTS ===")
calculate_total_revenue(valid)
region_wise_sales(valid)
top_selling_products(valid, n=5)
customer_analysis(valid)
daily_sales_trend(valid)
find_peak_sales_day(valid)
low_performing_products(valid, threshold=10)
