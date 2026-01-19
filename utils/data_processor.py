# utils/data_processor.py
def calculate_total_revenue(transactions):
    """Total revenue = sum(Quantity * Unit_Price)"""
    total = sum(t['Quantity'] * t['Unit_Price'] for t in transactions)
    print(f"Total Revenue: {total:,.2f}")
    return total

def region_wise_sales(transactions):
    """Region stats: total sales, count, percentage – sorted by sales desc"""
    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)
    
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['Unit_Price']
        if region not in region_stats:
            region_stats[region] = {'total_sales': 0, 'transaction_count': 0}
        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1
    
    # Add percentages and sort
    for region in region_stats:
        pct = (region_stats[region]['total_sales'] / total_revenue) * 100
        region_stats[region]['percentage'] = f"{pct:.2f}%"
    
    sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True)
    print("Region-wise Sales:")
    for region, stats in sorted_regions:
        print(f"{region}: {stats['total_sales']:,.0f} ({stats['percentage']}), {stats['transaction_count']} txns")
    return dict(sorted_regions)

def top_selling_products(transactions, n=5):
    """Top n products by total quantity sold"""
    product_stats = {}
    
    for t in transactions:
        product = t['Product_Name']
        qty = t['Quantity']
        revenue = qty * t['Unit_Price']
        if product not in product_stats:
            product_stats[product] = {'total_qty': 0, 'total_revenue': 0}
        product_stats[product]['total_qty'] += qty
        product_stats[product]['total_revenue'] += revenue
    
    # Sort by quantity desc, take top n
    top_products = sorted(product_stats.items(), key=lambda x: x[1]['total_qty'], reverse=True)[:n]
    
    print(f"Top {n} Products:")
    for product, stats in top_products:
        print(f"{product}: {stats['total_qty']} qty, {stats['total_revenue']:,.0f}")
    
    return [(p, stats['total_qty'], stats['total_revenue']) for p, stats in top_products]

def customer_analysis(transactions):
    """Customer stats: total spent, purchase count, avg order, unique products"""
    customer_stats = {}
    
    for t in transactions:
        customer = t['Customer_ID']
        amount = t['Quantity'] * t['Unit_Price']
        product = t['Product_Name']
        
        if customer not in customer_stats:
            customer_stats[customer] = {
                'total_spent': 0, 'purchase_count': 0, 'products': set()
            }
        customer_stats[customer]['total_spent'] += amount
        customer_stats[customer]['purchase_count'] += 1
        customer_stats[customer]['products'].add(product)
    
    # Calculate avg and sort by total_spent desc
    for customer in customer_stats:
        stats = customer_stats[customer]
        stats['avg_order_value'] = stats['total_spent'] / stats['purchase_count']
        stats['products_bought'] = ', '.join(sorted(stats['products']))
    
    sorted_customers = sorted(customer_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True)
    
    print("Top Customers:")
    for customer, stats in sorted_customers[:5]:  # Show top 5
        print(f"{customer}: {stats['total_spent']:,.0f} ({stats['purchase_count']} orders, avg {stats['avg_order_value']:,.0f})")
    
    return dict(sorted_customers)

def daily_sales_trend(transactions):
    """Daily revenue, txn count, unique customers – sorted by date"""
    daily_stats = {}
    
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['Unit_Price']
        customer = t['Customer_ID']
        
        if date not in daily_stats:
            daily_stats[date] = {'revenue': 0, 'transaction_count': 0, 'unique_customers': set()}
        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['unique_customers'].add(customer)
    
    # Convert set to count and sort chronologically
    for date in daily_stats:
        daily_stats[date]['unique_customers'] = len(daily_stats[date]['unique_customers'])
    
    sorted_days = dict(sorted(daily_stats.items()))
    
    print("Daily Sales Trend:")
    for date, stats in sorted_days.items():
        print(f"{date}: {stats['revenue']:,.0f}, {stats['transaction_count']} txns, {stats['unique_customers']} customers")
    
    return sorted_days

def find_peak_sales_day(transactions):
    """Date with highest revenue"""
    daily_stats = daily_sales_trend(transactions)
    peak_date = max(daily_stats.items(), key=lambda x: x[1]['revenue'])
    print(f"Peak Day: {peak_date[0]}, {peak_date[1]['revenue']:,.0f}, {peak_date[1]['transaction_count']} txns")
    return peak_date

def low_performing_products(transactions, threshold=10):
    """Products with total quantity < threshold, sorted asc"""
    product_stats = {}
    
    for t in transactions:
        product = t['Product_Name']
        qty = t['Quantity']
        revenue = qty * t['Unit_Price']
        if product not in product_stats:
            product_stats[product] = {'total_qty': 0, 'total_revenue': 0}
        product_stats[product]['total_qty'] += qty
        product_stats[product]['total_revenue'] += revenue
    
    low_performers = [
        (p, stats['total_qty'], stats['total_revenue']) 
        for p, stats in product_stats.items() 
        if stats['total_qty'] < threshold
    ]
    low_performers.sort(key=lambda x: x[1])  # Sort by qty asc
    
    print(f"Low Performing Products (<{threshold} qty):")
    for product, qty, revenue in low_performers:
        print(f"{product}: {qty} qty, {revenue:,.0f}")
    
    return low_performers
