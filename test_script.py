from utils.file_handler import *

raw_lines = read_sales_data('data/sales_data.txt')
print("Raw lines:", len(raw_lines))

transactions = parse_transactions(raw_lines)
print("Parsed:", len(transactions))

valid, invalid, summary = validate_and_filter_transactions(transactions)
print("Summary:", summary)
