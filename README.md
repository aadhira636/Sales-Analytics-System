# Sales Analytics System 🚀

**Complete Python assignment solution processing sales data, API integration, analysis, and reporting.**

## 📋 Features

✅ File reading with encoding handling  
✅ Data cleaning & validation (70/80 records)  
✅ Sales analysis (regions, products, customers, trends)  
✅ DummyJSON API integration  
✅ Data enrichment & export  
✅ Comprehensive formatted report generation  
✅ Interactive CLI with filtering  

## 📁 Structure

sales-analytics-system/
├── main.py # Main executable
├── requirements.txt # Dependencies
├── data/
│ └── sales_data.txt # Input data (80 records)
├── output/ # Generated reports
│ └── sales_report.txt
├── data/ # Generated enriched data
│ └── enriched_sales_data.txt
└── utils/
├── file_handler.py # Part 1: Read/parse/validate
├── data_processor.py # Part 2: Analysis functions
├── api_handler.py # Part 3: API integration
└── report_generator.py # Part 4: Report generation


## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/sales-analytics-system.git
cd sales-analytics-system
pip install -r requirements.txt

2. Run Complete System
    python main.py

3. Expected Output
    SALES ANALYTICS SYSTEM
    1/10 Reading sales data... (80 records)
    Valid: 68, Invalid: 12
    Region-wise analysis...
    API enrichment... (0-20% match expected)
    ✅ PROCESS COMPLETE!
    📊 Report: output/sales_report.txt
    💾 Enriched: data/enriched_sales_data.txt

🧪 Test Individual Parts
    # Part 1: Data handling
    python test_script.py
    # Part 2: Analysis  
    python test_part2.py
    # Part 3: API Integration
    python test_part3.py
    # Part 4: Report Generation
    python test_part4.py

🛠️ Data Quality Handling
Issue	Handled
Non-UTF8 encoding	Multi-encoding fallback
Commas in names	"Mouse,Wireless" → "Mouse Wireless"
Commas in numbers	"1,916" → 1916
Invalid records	12/80 removed (0 qty/price, bad IDs)
API mismatches	APIMatch=False, graceful handling
📈 Key Metrics (Sample)
Valid Records: 68/80 (85%)

Total Revenue: ~₹12-18 lakhs

API Success: 0-20% (expected)

Peak Day: Highest revenue date shown

🔧 Troubleshooting
FileNotFound: Ensure data/sales_data.txt exists
ModuleNotFound: pip install -r requirements.txt
No API matches: Normal – P101+ don't exist in DummyJSON (1-100)

📝 Assignment Compliance
✅ All 5 parts implemented
✅ Exact file structure
✅ Required console output format
✅ Report with 8 sections
✅ GitHub public repo
✅ requirements.txt included

