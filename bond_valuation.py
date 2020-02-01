#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose: Bond Pricing
Date created: 2020-02-01

Contributor(s):
    Mark Moretto
    
Note:
    A bond's value is the present value of the payments the issuer is
    contractually obligated to make -- from the present until maturity.
    The discount rate depends on the prevailing interest rate for debt
    obligations with similar risks and maturities. 
"""


__all__ = ['Bond', 'FinanceTime']
    


class FinanceTime:
    SEGMENTS = {
            'annual': 1,
            'semiannual': 2,
            'quarterly': 4,
            'monthly': 12,
            }
    def __init__(self):
        pass
    
    @staticmethod
    def validate_decimal(n):
        if not str(n).startswith("0."):
            n *= 1.0
            n /= 100
        return n

    def payment(self, par, coupon, compounding = 'annual'):
        coupon = self.validate_decimal(coupon)
        periods = self.SEGMENTS[compounding]
        return (par * coupon) / periods
    

    def pv_multiplier(self, i, n):
        i = self.validate_decimal(i)
        return 1 / (1 + i) ** n


    def fv_ord_annuity(self, amt, i, n):
        """Payment at end of period."""
        i = self.validate_decimal(i)
        amt *= 1.0
        numer = (1 + i) ** n - 1
        return round(amt * (numer / i), 4)
    
    def pv_ord_annuity(self, amt, i, n):
        """Payment at end of period."""
        i = self.validate_decimal(i)
        amt *= 1.0
        numer = 1 - ((1 + i) ** -n)
        return round(amt * (numer / i), 4)
    

    def fv_annuity_due(self, amt, i, n):
        """Payment at start of period."""
        i = self.validate_decimal(i)
        amt *= 1.0
        lhs = ((1 + i) ** n) - 1
        lhs /= i
        rhs = (1 + i)
        return round(amt * lhs * rhs, 4)
    

    def pv_annuity_due(self, amt, i, n):
        """Payment at start of period."""
        i = self.validate_decimal(i)
        amt *= 1.0
        lhs = 1 - ((1 + i) ** -n) 
        lhs /= i
        rhs = (1 + i)
        return round(amt * lhs * rhs, 4)
    

            

class Bond:
    def __init__(self, par_value, coupon, market_rate, n_periods, compounding = 'annual'):
        self.ft = FinanceTime()
        self.par_value = par_value
        self.coupon = coupon
        self.market_rate = market_rate
        self.n_years = n_periods
        self.compounding = compounding
        self.bond_value = None


    def calc_bond_value(self):
        pmt = self.ft.payment(self.par_value, self.coupon, self.compounding)
        
        lhs = pmt * self.ft.pv_ord_annuity(1, self.market_rate, self.n_years)
        rhs = self.par_value * self.ft.pv_multiplier(self.market_rate, self.n_years)
        self.bond_value = lhs + rhs
    

par_value = 1000
coupon = 8.6
market_rate = 8.0
N = 10

bond = Bond(par_value, coupon, market_rate, N)

bond.calc_bond_value()

assert (round(bond.bond_value, 2) == 1040.26), "Error: bond.calc_bond_value()"





#def return_rate(pv, fv, y):
#	return ((fv / pv) ** (1. / y)) - 1.




def test_ft():
    ft = FinanceTime()
    par_ = 1000
    i_ = 0.05
    n_per_ = 5
    
    assert ft.fv_ord_annuity(par_, i_, n_per_) == 5525.6313, "Error: fv_ord_annuity"
    assert ft.pv_ord_annuity(par_, i_, n_per_) == 4329.4767,"Error: pv_ord_annuity"
    assert ft.fv_annuity_due(par_, i_, n_per_) == 5801.9128, "Error: fv_annuity_due"
    assert ft.pv_annuity_due(par_, i_, n_per_) == 4545.9505,"Error: pv_annuity_due"
        
