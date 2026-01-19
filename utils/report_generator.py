 # utils/report_generator.py
from datetime import datetime
import os

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """Generate comprehensive formatted text report"""
    
    # Create output dir
    os.makedirs('output', exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("SALES ANALYTICS REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {len(transactions)}\n\n")
        
        # 1. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 20 + "\n")
        total_revenue = sum(t['Quantity'] * t['Unit_Price'] for t in transactions)
        total_txns = len(transactions)
        avg_order = total_revenue / total_txns if total_txns > 0 else 0
        dates = sorted(set(t['Date'] for t in transactions))
        date_range = f"{min(dates)} to {max(dates)}"
        
        f.write(f"Total Revenue: {total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_txns}\n")
        f.write(f"Average Order Value: {avg_order:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")
        
        # 2. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 25 + "\n")
        region_stats = {}
        for t in transactions:
            region = t['Region']
            amount = t['Quantity'] * t['Unit_Price']
            region_stats.setdefault(region, {'sales': 0, 'count': 0})['sales'] += amount
            region_stats.setdefault(region, {'sales': 0, 'count': 0})['count'] += 1
        
        sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]['sales'], reverse=True)
        for region, stats in sorted_regions:
            pct = (stats['sales'] / total_revenue) * 100
            f.write(f"{region:10} {stats['sales']:>10,.0f} ({pct:>5.1f}%) {stats['count']:>3} txns\n")
        f.write("\n")
        
        # 3. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 15 + "\n")
        product_stats = {}
        for t in transactions:
            prod = t['Product_Name']
            qty = t['Quantity']
            rev = qty * t['Unit_Price']
            product_stats.setdefault(prod, {'qty': 0, 'rev': 0})
            product_stats[prod]['qty'] += qty
            product_stats[prod]['rev'] += rev
        
        top_products = sorted(product_stats.items(), key=lambda x: x[1]['qty'], reverse=True)[:5]
        for i, (prod, stats) in enumerate(top_products, 1):
            f.write(f"{i:2}. {prod:<20} {stats['qty']:>3} qty  {stats['rev']:>10,.0f}\n")
        f.write("\n")
        
        # 4. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 18 + "\n")
        customer_stats = {}
        for t in transactions:
            cust = t['Customer_ID']
            amount = t['Quantity'] * t['Unit_Price']
            customer_stats.setdefault(cust, {'spent': 0, 'count': 0})['spent'] += amount
            customer_stats.setdefault(cust, {'spent': 0, 'count': 0})['count'] += 1
        
        top_customers = sorted(customer_stats.items(), key=lambda x: x[1]['spent'], reverse=True)[:5]
        for i, (cust, stats) in enumerate(top_customers, 1):
            avg = stats['spent'] / stats['count']
            f.write(f"{i:2}. {cust:<8} {stats['spent']:>10,.0f}  {stats['count']:>2} orders\n")
        f.write("\n")
        
        # 5. DAILY SALES TREND (first 10 days)
        f.write("DAILY SALES TREND\n")
        f.write("-" * 18 + "\n")
        daily_stats = {}
        for t in transactions:
            date = t['Date']
            amount = t['Quantity'] * t['Unit_Price']
            cust = t['Customer_ID']
            daily_stats.setdefault(date, {'rev': 0, 'count': 0, 'custs': set()})
            daily_stats[date]['rev'] += amount
            daily_stats[date]['count'] += 1
            daily_stats[date]['custs'].add(cust)
        
        sorted_days = sorted(daily_stats.items())
        for date, stats in sorted_days[:10]:  # First 10 days
            f.write(f"{date:<12} {stats['rev']:>8,.0f}  {stats['count']:>3} txns  {len(stats['custs']):>2} custs\n")
        f.write("\n")
        
        # 6. PEAK DAY
        peak_day = max(daily_stats.items(), key=lambda x: x[1]['rev'])
        f.write("PEAK SALES DAY\n")
        f.write("-" * 15 + "\n")
        f.write(f"{peak_day[0]:<12} {peak_day[1]['rev']:>8,.0f}\n\n")
        
        # 7. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 22 + "\n")
        enriched_count = len(enriched_transactions)
        success_count = sum(1 for t in enriched_transactions if t['API_Match'])
        success_rate = (success_count / enriched_count) * 100 if enriched_count > 0 else 0
        
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.1f}%\n")
        if success_count == 0:
            f.write("No products matched API catalog\n")
        f.write("\n")
    
    print(f"Report saved to {output_file}")
