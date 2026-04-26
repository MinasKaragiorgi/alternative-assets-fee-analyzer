# Quick Start Guide 🚀

Welcome! This guide will get you up and running with the Alternative Assets Fee Analyzer in under 5 minutes.

## Option 1: Jupyter Notebook (Recommended for Exploration)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Launch Notebook
```bash
jupyter notebook fee_analyzer.ipynb
```

### Step 3: Run All Cells
- Click `Cell` → `Run All` in the menu
- Or press `Shift + Enter` to run cells one by one
- Explore the examples and modify parameters

### What You'll See:
1. **Hedge Fund Analysis** - Compare 2/20 vs 1.5/15 fee structures
2. **Private Equity Scenarios** - Different exit multiples and their impact
3. **Fee Validation** - Automated discrepancy detection
4. **Interactive Visualizations** - NAV growth, fee drag, and more

---

## Option 2: Python Script (Quick Calculations)

### Step 1: Import the Module
```python
from fee_analyzer import HedgeFundFees, PrivateEquityFees, FeeValidator
```

### Step 2: Calculate Hedge Fund Fees
```python
# Initialize with 2/20 structure
hf = HedgeFundFees(management_fee=0.02, performance_fee=0.20)

# Calculate for one year
result = hf.calculate_fees(
    nav_start=10_000_000,   # $10M starting
    nav_end=11_500_000      # $11.5M ending (15% return)
)

print(f"Management Fee: ${result['management_fee']:,.0f}")
print(f"Performance Fee: ${result['performance_fee']:,.0f}")
print(f"Total Fees: ${result['total_fees']:,.0f}")
print(f"Net NAV: ${result['net_nav']:,.0f}")
```

**Output:**
```
Management Fee: $215,000
Performance Fee: $257,000
Total Fees: $472,000
Net NAV: $11,028,000
```

### Step 3: Analyze Private Equity
```python
# Initialize PE fund with 8% hurdle
pe = PrivateEquityFees(
    management_fee=0.02,
    carried_interest=0.20,
    hurdle_rate=0.08
)

# Calculate for 2.5x exit over 10 years
result = pe.calculate_fees(
    committed_capital=100_000_000,
    invested_capital=80_000_000,
    final_value=200_000_000,  # 2.5x multiple
    years=10
)

print(f"LP IRR: {result['lp_irr']*100:.1f}%")
print(f"Total Fees: ${result['total_fees']/1e6:.1f}M")
print(f"Hurdle Met: {'Yes ✓' if result['hurdle_met'] else 'No ✗'}")
```

**Output:**
```
LP IRR: 7.8%
Total Fees: $40.0M
Hurdle Met: Yes ✓
```

### Step 4: Validate Fees
```python
validator = FeeValidator(tolerance=0.02)  # 2% tolerance

validation = validator.validate_hedge_fund_fees(
    fund_name="Alpha Fund",
    reported_mgmt_fee=207_500,
    reported_perf_fee=300_000,
    nav_start=10_000_000,
    nav_end=11_500_000
)

print(f"Management Status: {validation['mgmt_status']}")
print(f"Performance Status: {validation['perf_status']}")
```

---

## Option 3: Command Line Demo

### Run the Built-in Example
```bash
python fee_analyzer.py
```

This will run demonstration calculations for both hedge funds and private equity.

---

## Common Use Cases

### 1. Compare Fee Structures
```python
from fee_analyzer import simulate_hedge_fund_returns

# 2/20 structure
traditional = simulate_hedge_fund_returns(
    initial_nav=10_000_000,
    annual_return=0.12,
    volatility=0.18,
    years=10,
    management_fee=0.02,
    performance_fee=0.20
)

# 1.5/15 structure
investor_friendly = simulate_hedge_fund_returns(
    initial_nav=10_000_000,
    annual_return=0.12,
    volatility=0.18,
    years=10,
    management_fee=0.015,
    performance_fee=0.15
)

# Compare
fee_savings = (traditional.iloc[-1]['cumulative_fees'] - 
               investor_friendly.iloc[-1]['cumulative_fees'])
print(f"Fee Savings: ${fee_savings:,.0f}")
```

### 2. Test Different Exit Scenarios (PE)
```python
pe = PrivateEquityFees(management_fee=0.02, carried_interest=0.20, hurdle_rate=0.08)

exit_multiples = [2.0, 2.5, 3.0, 3.5]
for multiple in exit_multiples:
    result = pe.calculate_fees(
        committed_capital=100_000_000,
        invested_capital=80_000_000,
        final_value=80_000_000 * multiple,
        years=10
    )
    print(f"{multiple}x Exit → LP IRR: {result['lp_irr']*100:.1f}%, "
          f"Carry: ${result['carried_interest']/1e6:.1f}M")
```

### 3. Batch Validate Multiple Funds
```python
validator = FeeValidator(tolerance=0.02)

funds = [
    {'name': 'Fund A', 'nav_start': 10_000_000, 'nav_end': 11_500_000, 
     'mgmt': 207_500, 'perf': 300_000},
    {'name': 'Fund B', 'nav_start': 25_000_000, 'nav_end': 26_200_000,
     'mgmt': 512_000, 'perf': 240_000},
]

for fund in funds:
    validator.validate_hedge_fund_fees(
        fund['name'], fund['mgmt'], fund['perf'], 
        fund['nav_start'], fund['nav_end']
    )

# Get report
report = validator.generate_report()
print(report[['fund_name', 'mgmt_status', 'perf_status']])
```

---

## Key Parameters Explained

### Hedge Funds
- `management_fee`: Annual % (e.g., 0.02 = 2%)
- `performance_fee`: % of profits (e.g., 0.20 = 20%)
- `nav_start`: Net Asset Value at period start
- `nav_end`: Net Asset Value at period end (before fees)

### Private Equity
- `committed_capital`: Total LP commitment
- `invested_capital`: Capital actually deployed
- `final_value`: Exit value of portfolio
- `years`: Fund life
- `hurdle_rate`: Minimum IRR before carry (e.g., 0.08 = 8%)

---

## Troubleshooting

### Import Error
```bash
# Make sure you're in the project directory
cd alternative_assets_fee_analyzer

# Install dependencies
pip install -r requirements.txt
```

### Jupyter Kernel Issues
```bash
# Install ipykernel
pip install ipykernel

# Add Python to Jupyter
python -m ipykernel install --user
```

### ModuleNotFoundError
```python
# If running scripts, make sure fee_analyzer.py is in same directory
import sys
sys.path.append('.')
from fee_analyzer import *
```

---

## Next Steps

1. **Explore the Notebook**: Open `fee_analyzer.ipynb` and run through all examples
2. **Modify Parameters**: Try different fee rates, returns, and time periods
3. **Add Your Data**: Replace example values with real fund data
4. **Extend Functionality**: Add new fee structures or validation logic
5. **Share Results**: Export charts and data for presentations

---

## Need Help?

- 📧 Email: minaskaragiorgi28@gmail.com
- 📚 Read the full [README.md](README.md)
- 🐛 Report issues on GitHub
- 💡 Check the code comments for detailed explanations

---

## Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Run Jupyter Notebook | `jupyter notebook fee_analyzer.ipynb` |
| Run demo script | `python fee_analyzer.py` |
| Import in Python | `from fee_analyzer import *` |
| Generate report | `validator.generate_report()` |

---

**Happy Analyzing! 📊**
