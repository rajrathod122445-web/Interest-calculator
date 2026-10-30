# Interest Calculator in Python

A command-line calculator covering the five calculations below. Pure Python 3.7+, no dependencies.

## Formulas used

| Calculation       | Formula |
|-------------------|---------|
| Simple interest   | `SI = P x R x T / 100` |
| Compound amount   | `A = P x (1 + R / (100n)) ^ (nT)` |
| Loan EMI          | `P x r x (1+r)^N / ((1+r)^N - 1)` |
| SIP future value  | `M x (((1+i)^N - 1) / i) x (1+i)` |
| Doubling time     | `72 / R` and `ln 2 / ln(1 + R/100)` |

**Symbols:** P = principal, R = annual rate (%), T = years, n = compounding periods per year,
r = monthly loan rate (R / 12 / 100), i = monthly SIP rate, N = number of months, M = monthly SIP amount.

## Run

```bash
python interest_calculator.py
```

Menu:

```
1. Simple interest
2. Compound amount
3. Loan EMI          (optional month-by-month amortization schedule)
4. SIP future value
5. Doubling time     (Rule of 72 and exact)
6. Quit
```

## Use as a module

```python
from interest_calculator import loan_emi, sip_future_value

print(loan_emi(1_000_000, 8.5, 20))
print(sip_future_value(5000, 12, 10))
```

## Functions

| Function | Returns |
|----------|---------|
| `simple_interest(p, rate, years)` | principal, interest, total |
| `compound_amount(p, rate, years, n=1)` | principal, interest, total |
| `loan_emi(p, annual_rate, years)` | emi, months, total_payment, total_interest |
| `amortization_schedule(p, annual_rate, years)` | list of (month, emi, interest, principal, balance) |
| `sip_future_value(monthly, annual_rate, years)` | invested, returns, future_value |
| `doubling_time(rate)` | rule_of_72, exact |

## Notes

- SIP assumes the deposit is made at the **start** of each month (the `x (1+i)` term).
- Results are estimates and ignore taxes, fees and inflation.
