"""
Alternative Assets Fee Analyzer
================================

A comprehensive toolkit for modeling and analyzing fee structures in 
Hedge Funds and Private Equity investments.

Author: Minas Karagiorgis
Email: minaskaragiorgi28@gmail.com
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, Optional


class HedgeFundFees:
    """
    Hedge Fund Fee Calculator with High-Water Mark
    
    Typical Structure: 2/20 (2% management, 20% performance)
    - Management fee charged on NAV regardless of performance
    - Performance fee only charged on gains above high-water mark
    
    Example:
        >>> hf = HedgeFundFees(management_fee=0.02, performance_fee=0.20)
        >>> result = hf.calculate_fees(nav_start=10_000_000, nav_end=11_500_000)
        >>> print(f"Total fees: ${result['total_fees']:,.0f}")
    """
    
    def __init__(self, management_fee: float = 0.02, performance_fee: float = 0.20):
        """
        Initialize hedge fund fee calculator
        
        Args:
            management_fee: Annual management fee as decimal (e.g., 0.02 for 2%)
            performance_fee: Performance fee as decimal (e.g., 0.20 for 20%)
        """
        self.management_fee = management_fee
        self.performance_fee = performance_fee
        self.high_water_mark = 0
        
    def calculate_fees(self, nav_start: float, nav_end: float) -> Dict[str, float]:
        """
        Calculate annual fees for a hedge fund
        
        Args:
            nav_start: NAV at start of period
            nav_end: NAV at end of period (before fees)
            
        Returns:
            Dictionary containing:
                - management_fee: Management fee charged
                - performance_fee: Performance fee charged
                - total_fees: Sum of all fees
                - net_nav: NAV after fees
                - high_water_mark: Updated high-water mark
        """
        # Management fee on average NAV
        avg_nav = (nav_start + nav_end) / 2
        mgmt_fee = avg_nav * self.management_fee
        
        # Performance fee on gains above high-water mark
        nav_after_mgmt = nav_end - mgmt_fee
        
        if nav_after_mgmt > self.high_water_mark:
            profit = nav_after_mgmt - max(self.high_water_mark, nav_start)
            perf_fee = max(0, profit * self.performance_fee)
            self.high_water_mark = nav_after_mgmt - perf_fee
        else:
            perf_fee = 0
        
        total_fees = mgmt_fee + perf_fee
        net_nav = nav_end - total_fees
        
        return {
            'management_fee': mgmt_fee,
            'performance_fee': perf_fee,
            'total_fees': total_fees,
            'net_nav': net_nav,
            'high_water_mark': self.high_water_mark
        }
    
    def reset_high_water_mark(self):
        """Reset high-water mark (e.g., for new fund or analysis)"""
        self.high_water_mark = 0


class PrivateEquityFees:
    """
    Private Equity Fee Calculator with Hurdle Rate and Catch-up
    
    Typical Structure: 2/20 with 8% hurdle
    - Management fee on committed/invested capital
    - Carried interest (20%) only after investors achieve hurdle rate
    - Catch-up provision: GP gets larger % to "catch up" after hurdle met
    
    Example:
        >>> pe = PrivateEquityFees(management_fee=0.02, carried_interest=0.20, hurdle_rate=0.08)
        >>> result = pe.calculate_fees(
        ...     committed_capital=100_000_000,
        ...     invested_capital=80_000_000,
        ...     final_value=200_000_000,
        ...     years=10
        ... )
        >>> print(f"LP IRR: {result['lp_irr']*100:.1f}%")
    """
    
    def __init__(self, 
                 management_fee: float = 0.02,
                 carried_interest: float = 0.20,
                 hurdle_rate: float = 0.08,
                 catch_up: float = 1.0):
        """
        Initialize private equity fee calculator
        
        Args:
            management_fee: Annual fee as % of committed/invested capital
            carried_interest: GP's share of profits above hurdle ("carry")
            hurdle_rate: Minimum IRR before carry applies (preferred return)
            catch_up: % of profits GP receives after hurdle until they reach full carry
        """
        self.management_fee = management_fee
        self.carried_interest = carried_interest
        self.hurdle_rate = hurdle_rate
        self.catch_up = catch_up
        
    def calculate_fees(self, 
                      committed_capital: float,
                      invested_capital: float,
                      final_value: float,
                      years: int,
                      investment_period: bool = True) -> Dict[str, float]:
        """
        Calculate fees for a PE fund
        
        Args:
            committed_capital: Total capital committed by LPs
            invested_capital: Capital actually deployed
            final_value: Exit value of investments
            years: Fund life in years
            investment_period: If True, charge on committed capital; else on invested
            
        Returns:
            Dictionary containing:
                - management_fees: Total management fees over fund life
                - carried_interest: GP carry (performance fee)
                - total_fees: Sum of all fees
                - lp_proceeds: Net proceeds to Limited Partners
                - lp_irr: LP net IRR
                - hurdle_met: Boolean indicating if hurdle was achieved
                - gross_multiple: Total value / invested capital
                - net_multiple: LP proceeds / invested capital
        """
        # Management fees over fund life
        base_for_mgmt = committed_capital if investment_period else invested_capital
        annual_mgmt_fee = base_for_mgmt * self.management_fee
        total_mgmt_fees = annual_mgmt_fee * years
        
        # Calculate hurdle amount (what LPs must get before GP gets carry)
        hurdle_value = invested_capital * ((1 + self.hurdle_rate) ** years)
        
        # Distribute proceeds
        value_after_mgmt = final_value - total_mgmt_fees
        
        if value_after_mgmt <= hurdle_value:
            # Below hurdle: LPs get everything after management fees
            carry = 0
            lp_proceeds = value_after_mgmt
        else:
            # Above hurdle: GP gets carry on profits above hurdle
            profit_above_hurdle = value_after_mgmt - hurdle_value
            
            # Apply catch-up (GP gets higher % initially to "catch up")
            catch_up_amount = min(profit_above_hurdle, 
                                 hurdle_value * self.carried_interest / (1 - self.carried_interest))
            gp_catch_up = catch_up_amount * self.catch_up
            
            # Remaining profits split by carry %
            remaining_profit = profit_above_hurdle - catch_up_amount
            gp_remaining = remaining_profit * self.carried_interest
            
            carry = gp_catch_up + gp_remaining
            lp_proceeds = value_after_mgmt - carry
        
        total_fees = total_mgmt_fees + carry
        
        # Calculate realized IRR for LPs
        lp_multiple = lp_proceeds / invested_capital
        lp_irr = (lp_multiple ** (1/years)) - 1 if years > 0 else 0
        
        return {
            'management_fees': total_mgmt_fees,
            'carried_interest': carry,
            'total_fees': total_fees,
            'lp_proceeds': lp_proceeds,
            'lp_irr': lp_irr,
            'hurdle_met': value_after_mgmt > hurdle_value,
            'gross_multiple': final_value / invested_capital,
            'net_multiple': lp_proceeds / invested_capital
        }


class FeeValidator:
    """
    Fee Validation Tool - Similar to Albourne's FeeMometer™
    
    Compares calculated fees vs. reported fees to identify discrepancies
    
    Example:
        >>> validator = FeeValidator(tolerance=0.02)
        >>> result = validator.validate_hedge_fund_fees(
        ...     fund_name="Alpha Fund",
        ...     reported_mgmt_fee=207_500,
        ...     reported_perf_fee=300_000,
        ...     nav_start=10_000_000,
        ...     nav_end=11_500_000
        ... )
        >>> print(result['mgmt_status'])  # ✓ PASS or ✗ FAIL
    """
    
    def __init__(self, tolerance: float = 0.01):
        """
        Initialize fee validator
        
        Args:
            tolerance: Acceptable variance (e.g., 0.01 = 1% tolerance)
        """
        self.tolerance = tolerance
        self.validations = []
    
    def validate_hedge_fund_fees(self,
                                fund_name: str,
                                reported_mgmt_fee: float,
                                reported_perf_fee: float,
                                nav_start: float,
                                nav_end: float,
                                mgmt_fee_rate: float = 0.02,
                                perf_fee_rate: float = 0.20) -> Dict:
        """
        Validate reported hedge fund fees against calculated fees
        
        Args:
            fund_name: Name of the fund
            reported_mgmt_fee: Management fee as reported by fund
            reported_perf_fee: Performance fee as reported by fund
            nav_start: Starting NAV
            nav_end: Ending NAV (before fees)
            mgmt_fee_rate: Expected management fee rate
            perf_fee_rate: Expected performance fee rate
            
        Returns:
            Dictionary with validation results including pass/fail status
        """
        hf = HedgeFundFees(mgmt_fee_rate, perf_fee_rate)
        hf.high_water_mark = nav_start  # Simplified assumption
        
        calculated = hf.calculate_fees(nav_start, nav_end)
        
        mgmt_diff = abs(calculated['management_fee'] - reported_mgmt_fee)
        perf_diff = abs(calculated['performance_fee'] - reported_perf_fee)
        
        mgmt_variance = mgmt_diff / calculated['management_fee'] if calculated['management_fee'] > 0 else 0
        perf_variance = perf_diff / calculated['performance_fee'] if calculated['performance_fee'] > 0 else 0
        
        mgmt_status = "✓ PASS" if mgmt_variance <= self.tolerance else "✗ FAIL"
        perf_status = "✓ PASS" if perf_variance <= self.tolerance else "✗ FAIL"
        
        validation = {
            'fund_name': fund_name,
            'reported_mgmt_fee': reported_mgmt_fee,
            'calculated_mgmt_fee': calculated['management_fee'],
            'mgmt_difference': mgmt_diff,
            'mgmt_variance_%': mgmt_variance * 100,
            'mgmt_status': mgmt_status,
            'reported_perf_fee': reported_perf_fee,
            'calculated_perf_fee': calculated['performance_fee'],
            'perf_difference': perf_diff,
            'perf_variance_%': perf_variance * 100,
            'perf_status': perf_status
        }
        
        self.validations.append(validation)
        return validation
    
    def generate_report(self) -> pd.DataFrame:
        """Generate validation report as pandas DataFrame"""
        return pd.DataFrame(self.validations)


def simulate_hedge_fund_returns(initial_nav: float,
                               annual_return: float,
                               volatility: float,
                               years: int,
                               management_fee: float = 0.02,
                               performance_fee: float = 0.20,
                               seed: int = 42) -> pd.DataFrame:
    """
    Simulate hedge fund performance over time with fees
    
    Args:
        initial_nav: Starting NAV
        annual_return: Expected annual return (e.g., 0.10 for 10%)
        volatility: Annual volatility (e.g., 0.15 for 15%)
        years: Number of years to simulate
        management_fee: Annual management fee
        performance_fee: Performance fee on profits
        seed: Random seed for reproducibility
        
    Returns:
        DataFrame with year-by-year NAV, fees, and cumulative results
    """
    np.random.seed(seed)
    
    hf_fees = HedgeFundFees(management_fee, performance_fee)
    
    results = []
    nav_gross = initial_nav
    nav_net = initial_nav
    
    for year in range(years + 1):
        if year == 0:
            results.append({
                'year': year,
                'nav_gross': nav_gross,
                'nav_net': nav_net,
                'management_fee': 0,
                'performance_fee': 0,
                'total_fees': 0,
                'cumulative_fees': 0
            })
            continue
        
        # Generate random return
        random_return = np.random.normal(annual_return, volatility)
        
        # Gross NAV (without fees)
        nav_gross_start = nav_gross
        nav_gross = nav_gross * (1 + random_return)
        
        # Calculate fees on net NAV
        fee_calc = hf_fees.calculate_fees(results[-1]['nav_net'], 
                                         nav_gross * (results[-1]['nav_net'] / nav_gross_start))
        
        nav_net = fee_calc['net_nav']
        
        cumulative_fees = results[-1]['cumulative_fees'] + fee_calc['total_fees']
        
        results.append({
            'year': year,
            'nav_gross': nav_gross,
            'nav_net': nav_net,
            'management_fee': fee_calc['management_fee'],
            'performance_fee': fee_calc['performance_fee'],
            'total_fees': fee_calc['total_fees'],
            'cumulative_fees': cumulative_fees
        })
    
    df = pd.DataFrame(results)
    df['fee_drag'] = ((df['nav_gross'] - df['nav_net']) / df['nav_gross'] * 100)
    
    return df


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("ALTERNATIVE ASSETS FEE ANALYZER")
    print("="*60)
    
    # Example 1: Hedge Fund
    print("\n--- Hedge Fund Example ---")
    hf = HedgeFundFees(management_fee=0.02, performance_fee=0.20)
    result = hf.calculate_fees(nav_start=10_000_000, nav_end=11_500_000)
    
    print(f"Starting NAV: ${10_000_000:,.0f}")
    print(f"Ending NAV (before fees): ${11_500_000:,.0f}")
    print(f"\nManagement Fee: ${result['management_fee']:,.0f}")
    print(f"Performance Fee: ${result['performance_fee']:,.0f}")
    print(f"Total Fees: ${result['total_fees']:,.0f}")
    print(f"Net NAV: ${result['net_nav']:,.0f}")
    
    # Example 2: Private Equity
    print("\n--- Private Equity Example ---")
    pe = PrivateEquityFees(management_fee=0.02, carried_interest=0.20, hurdle_rate=0.08)
    result = pe.calculate_fees(
        committed_capital=100_000_000,
        invested_capital=80_000_000,
        final_value=200_000_000,
        years=10
    )
    
    print(f"Invested Capital: ${80_000_000:,.0f}")
    print(f"Final Value: ${200_000_000:,.0f}")
    print(f"Gross Multiple: {result['gross_multiple']:.2f}x")
    print(f"\nManagement Fees: ${result['management_fees']:,.0f}")
    print(f"Carried Interest: ${result['carried_interest']:,.0f}")
    print(f"Total Fees: ${result['total_fees']:,.0f}")
    print(f"\nLP Proceeds: ${result['lp_proceeds']:,.0f}")
    print(f"Net Multiple: {result['net_multiple']:.2f}x")
    print(f"LP IRR: {result['lp_irr']*100:.1f}%")
    print(f"Hurdle Met: {'Yes ✓' if result['hurdle_met'] else 'No ✗'}")
    
    print("\n" + "="*60)
