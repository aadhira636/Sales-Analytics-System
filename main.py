#!/usr/bin/env python3
"""
SALES ANALYTICS SYSTEM - Complete Assignment Solution
"""
import os
from utils.file_handler import *
from utils.data_processor import *
from utils.api_handler import *
from utils.report_generator import *

def main():
    print("SALES ANALYTICS SYSTEM")
    print("=" * 30)
    
    try:
        # 1. Read and parse data
        print("\n1/10 Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        
        print("2/10 Parsing and cleaning...")
        transactions = parse_transactions(raw_lines)
        
        print("3/10 Filter options:")
        valid, invalid_count, summary = validate_and_filter_transactions(transactions)
        
        # 4. User filter interaction
        print("\nApply filters? (y/n): ", end="")
        choice = input().strip().lower()
        if choice == 'y':
            print("Enter region (or Enter for none): ", end="")
            region_filter = input().strip() or None
            
            print("Min amount (or Enter for none): ", end="")
            min_amt = input().strip()
            min_amt = float(min_amt) if min_amt else None
            
            print("Max amount (or Enter for none): ", end="")
            max_amt = input().strip()
            max_amt = float(max_amt) if max_amt else None
            
            valid, invalid_count, summary = validate_and_filter_transactions(
                transactions, region_filter, min_amt, max_amt
            )
        
        print(f"Valid: {len(valid)}, Invalid: {invalid_count}")
        
        # 5. Analyze data (Part 2)
        print("5/10 Analyzing sales data...")
        calculate_total_revenue(valid)
        region_wise_sales(valid)
        top_selling_products(valid, n=5)
        customer_analysis(valid)
        daily_sales_trend(valid)
        find_peak_sales_day(valid)
        low_performing_products(valid, threshold=10)
        
        # 6. API Integration (Part 3)
        print("6/10 Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        
        print("7/10 Enriching sales data...")
        enriched = enrich_sales_data(valid, product_mapping)
        
        # 8. Generate Report (Part 4)
        print("8/10 Generating report...")
        generate_sales_report(valid, enriched)
        
        # 9. Success message
        print("\n" + "=" * 40)
        print("✅ PROCESS COMPLETE!")
        print(f"📊 Report: output/sales_report.txt")
        print(f"💾 Enriched: data/enriched_sales_data.txt")
        print("=" * 40)
        
    except KeyboardInterrupt:
        print("\n\n👋 Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Ensure all utils/ files exist and requirements.txt installed")

if __name__ == "__main__":
    main()
