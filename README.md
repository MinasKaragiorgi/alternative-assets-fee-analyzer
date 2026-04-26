# Alternative Assets Fee Analyzer 📊

> A comprehensive Python tool for modeling, analyzing, and validating fee structures in Hedge Funds and Private Equity investments.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

---

## 🎯 Project Overview

This project demonstrates practical understanding of alternative asset fee structures and their impact on investor returns. Inspired by the work done at **Albourne Partners' Fee & Liquidity team**, this tool provides:

- **Fee Structure Modeling** for Hedge Funds (2/20) and Private Equity (2/20 with hurdle rates)
- **Net Return Calculations** showing the real impact of fees on investment performance
- **Scenario Analysis** comparing different fee structures across market conditions
- **Fee Validation Tools** to detect discrepancies between calculated and reported fees
- **Professional Visualizations** for clear stakeholder communication

---

## 💡 Why This Matters

**Fee impact is substantial:**
- Over 10 years, a 2/20 structure can consume 15-25% of gross returns
- Small fee differences (2/20 vs 1.5/15) can mean **millions** in savings for large portfolios
- Fee calculation errors are common in complex structures

**This tool helps:**
- Investors understand true costs of alternative investments
- Analysts validate fee calculations and identify discrepancies
- Fund selectors compare fee structures objectively
- Students learn practical financial modeling skills

---

## 🚀 Features

### 1. Hedge Fund Fee Calculator
- Traditional 2/20 structure modeling
- High-water mark implementation
- Management + performance fee breakdown
- Multi-year simulations with realistic volatility

### 2. Private Equity Fee Analyzer
- 2/20 structure with hurdle rates
- Carried interest (carry) calculations
- Waterfall distribution modeling
- Catch-up provision support
- IRR calculations for Limited Partners

### 3. Fee Validation Engine
- Compare calculated vs. reported fees
- Automated discrepancy detection
- Configurable tolerance thresholds
- Batch validation for multiple funds

### 4. Comprehensive Visualizations
- NAV growth over time
- Cumulative fee impact charts
- Fee drag analysis
- Gross vs. net return comparisons

---

## 📋 Requirements

```bash
Python 3.8+
numpy
pandas
matplotlib
seaborn
jupyter
```

---

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/alternative-assets-fee-analyzer.git
cd alternative-assets-fee-analyzer

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Notebook
jupyter notebook fee_analyzer.ipynb
```

---

## 📊 Usage Examples

### Quick Start - Hedge Fund Fee Calculation

```python
from fee_analyzer import HedgeFundFees

# Initialize fee structure
hf = HedgeFundFees(management_fee=0.02, performance_fee=0.20)

# Calculate fees for the year
result = hf.calculate_fees(
    nav_start=10_000_000,
    nav_end=11_500_000
)

print(f"Management Fee: ${result['management_fee']:,.0f}")
print(f"Performance Fee: ${result['performance_fee']:,.0f}")
print(f"Net NAV: ${result['net_nav']:,.0f}")
```

### Private Equity Scenario Analysis

```python
from fee_analyzer import PrivateEquityFees

# Initialize PE fund
pe_fund = PrivateEquityFees(
    management_fee=0.02,
    carried_interest=0.20,
    hurdle_rate=0.08
)

# Calculate returns for different exit multiples
results = pe_fund.calculate_fees(
    committed_capital=100_000_000,
    invested_capital=80_000_000,
    final_value=200_000_000,  # 2.5x exit
    years=10
)

print(f"LP IRR: {results['lp_irr']*100:.1f}%")
print(f"Carry Paid: ${results['carried_interest']/1e6:.1f}M")
```

### Fee Validation

```python
from fee_analyzer import FeeValidator

validator = FeeValidator(tolerance=0.02)  # 2% tolerance

# Validate reported fees
validation = validator.validate_hedge_fund_fees(
    fund_name="Alpha Fund",
    reported_mgmt_fee=207_500,
    reported_perf_fee=300_000,
    nav_start=10_000_000,
    nav_end=11_500_000
)

print(validation['mgmt_status'])  # ✓ PASS or ✗ FAIL
```

---

## 📈 Sample Results

### Hedge Fund Fee Impact (10 Years, $10M Initial Investment)

| Fee Structure | Final Value | Total Fees | Net Return | Fee Drag |
|--------------|-------------|------------|------------|----------|
| Gross (No Fees) | $31.1M | $0 | 211% | 0% |
| 2/20 (Traditional) | $26.4M | $4.7M | 164% | 15.1% |
| 1.5/15 (Investor-Friendly) | $27.8M | $3.3M | 178% | 10.6% |

**Savings with 1.5/15 structure: $1.4M** (30% fee reduction)

### Private Equity Returns by Exit Multiple

| Exit Multiple | Gross IRR | Net IRR | Total Fees | Hurdle Met? |
|--------------|-----------|---------|------------|-------------|
| 2.0x | 7.2% | 5.1% | $36M | ✗ No |
| 2.5x | 9.6% | 7.8% | $40M | ✓ Yes |
| 3.0x | 11.6% | 10.1% | $44M | ✓ Yes |

---

## 🎓 Learning Outcomes

This project demonstrates:

✅ **Financial Modeling** - Complex fee structure implementations  
✅ **Python Programming** - OOP, data analysis, visualization  
✅ **Quantitative Skills** - IRR calculations, Monte Carlo simulation potential  
✅ **Data Validation** - Automated reconciliation and error detection  
✅ **Domain Knowledge** - Alternative investment fee mechanics  

---

## 🔍 Real-World Relevance

### Albourne Partners Context

This project was inspired by Albourne Partners' proprietary tools:
- **FeeMometer™** - Tool for studying fee structure effects
- **FeeConciliation™** - Service for fee validation and reconciliation
- **Fee & Liquidity Team** - Validates fee data for Private Markets investments

### Industry Applications

- **Institutional Investors**: Evaluate fee impact before committing capital
- **Fund Administrators**: Validate fee calculations for accuracy
- **Consultants**: Compare fee structures across managers
- **Regulators**: Monitor fee transparency and compliance

---

## 🛣️ Roadmap

Future enhancements planned:

- [ ] **Advanced Structures**: Implement "1 or 30" and beta hurdle models
- [ ] **Clawback Modeling**: Full GP clawback provision calculations
- [ ] **Monte Carlo Simulation**: Probabilistic outcome analysis
- [ ] **Portfolio Aggregation**: Multi-fund fee analysis tools
- [ ] **API Integration**: Live data feeds for real-time validation
- [ ] **Web Dashboard**: Interactive Streamlit/Dash interface
- [ ] **Liquidity Modeling**: Capital call and distribution forecasting

---

## 📚 References & Resources

### Fee Structures
- Albourne Partners - "The Shape of Fees" initiative
- Preqin - Alternative Investment Fee Structures
- ILPA - Fee Reporting Template

### Technical Implementation
- NumPy Documentation
- Pandas User Guide
- Matplotlib Visualization Gallery

### Alternative Investments
- Hedge Fund Research (HFR)
- Private Equity International
- Institutional Investor

---

## 👤 Author

**Minas Karagiorgis**  
Computer Science Student | Finance Enthusiast  
University of Cyprus

📧 Email: minaskaragiorgi28@gmail.com  
📍 Location: Larnaca, Cyprus  


---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  

Feel free to check the [issues page](issues/) or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Albourne Partners** for publicly sharing insights about fee structures and industry best practices
- **University of Cyprus** Computer Science Department for technical foundation
- Open-source community for excellent Python libraries

---

## ⚠️ Disclaimer

This tool is for educational and analytical purposes only. It does not constitute financial advice. Fee structures can be highly complex and vary significantly between funds. Always consult with qualified professionals and review actual fund documentation for investment decisions.

---

## 📞 Contact

Questions? Suggestions? Want to discuss alternative investments or quantitative finance?

📧 **karagiorgiminas8@gmail.com**

---

<div align="center">

**If you found this project useful, please consider giving it a ⭐️!**

Made with ❤️ and Python

</div>
