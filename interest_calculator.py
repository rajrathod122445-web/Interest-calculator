#!/usr/bin/env python3
"""
Interest Calculator in Python
-----------------------------
Features (and formulas used):

  1. Simple interest     SI = P x R x T / 100
  2. Compound amount     A  = P x (1 + R / (100n)) ^ (nT)
  3. Loan EMI            EMI = P x r x (1+r)^N / ((1+r)^N - 1)
  4. SIP future value    FV = M x (((1+i)^N - 1) / i) x (1+i)
  5. Doubling time       Rule of 72: 72 / R   and   ln 2 / ln(1 + R/100)

P = principal, R = annual rate (%), T = years, n = compounding periods/year,
r = monthly loan rate, i = monthly SIP rate, N = number of months, M = monthly SIP.
"""

import math


# ------------------------------------------------------------------ calculations

def simple_interest(p: float, rate: float, years: float) -> dict:
    """SI = P x R x T / 100"""
    si = p * rate * years / 100
    return {"principal": p, "interest": si, "total": p + si}


def compound_amount(p: float, rate: float, years: float, n: int = 1) -> dict:
    """A = P x (1 + R / (100n)) ^ (nT)"""
    amount = p * (1 + rate / (100 * n)) ** (n * years)
    return {"principal": p, "interest": amount - p, "total": amount}


def loan_emi(p: float, annual_rate: float, years: float) -> dict:
    """EMI = P x r x (1+r)^N / ((1+r)^N - 1), r = monthly rate."""
    n_months = int(round(years * 12))
    r = annual_rate / 12 / 100
    if r == 0:
        emi = p / n_months
    else:
        factor = (1 + r) ** n_months
        emi = p * r * factor / (factor - 1)
    total_payment = emi * n_months
    return {
        "emi": emi,
        "months": n_months,
        "total_payment": total_payment,
        "total_interest": total_payment - p,
    }


def amortization_schedule(p: float, annual_rate: float, years: float) -> list:
    """Return rows of (month, emi, interest, principal_paid, balance)."""
    r = annual_rate / 12 / 100
    emi = loan_emi(p, annual_rate, years)["emi"]
    balance = p
    rows = []
    for month in range(1, int(round(years * 12)) + 1):
        interest = balance * r
        principal_paid = emi - interest
        balance = max(balance - principal_paid, 0.0)
        rows.append((month, emi, interest, principal_paid, balance))
    return rows


def sip_future_value(monthly: float, annual_rate: float, years: float) -> dict:
    """FV = M x (((1+i)^N - 1) / i) x (1+i), i = monthly rate."""
    n_months = int(round(years * 12))
    i = annual_rate / 12 / 100
    if i == 0:
        fv = monthly * n_months
    else:
        fv = monthly * (((1 + i) ** n_months - 1) / i) * (1 + i)
    invested = monthly * n_months
    return {"invested": invested, "returns": fv - invested, "future_value": fv}


def doubling_time(rate: float) -> dict:
    """Rule of 72 (approx.) and exact logarithmic doubling time, in years."""
    if rate <= 0:
        raise ValueError("Rate must be greater than 0.")
    return {
        "rule_of_72": 72 / rate,
        "exact": math.log(2) / math.log(1 + rate / 100),
    }


# ------------------------------------------------------------------ input helpers

def ask_float(prompt: str, minimum: float = 0.0, allow_equal: bool = True) -> float:
    while True:
        try:
            value = float(input(prompt).replace(",", "").strip())
        except ValueError:
            print("  Invalid number, please try again.")
            continue
        if value < minimum or (not allow_equal and value == minimum):
            print(f"  Please enter a value {'at least' if allow_equal else 'greater than'} {minimum:g}.")
            continue
        return value


def ask_compounding() -> int:
    options = {"1": ("Annually", 1), "2": ("Half-yearly", 2),
               "3": ("Quarterly", 4), "4": ("Monthly", 12), "5": ("Daily", 365)}
    print("\nCompounding frequency (n):")
    for k, (name, n) in options.items():
        print(f"  {k}. {name} (n={n})")
    while True:
        choice = input("Choose (1-5) [1]: ").strip() or "1"
        if choice in options:
            return options[choice][1]
        print("  Invalid choice.")


def line(label: str, value: float, width: int = 20) -> None:
    print(f"  {label:<{width}}{value:>16,.2f}")


def banner(title: str) -> None:
    print("\n" + "=" * 38)
    print(f"  {title}")
    print("=" * 38)


# ------------------------------------------------------------------ menu actions

def do_simple() -> None:
    p = ask_float("Principal (P): ")
    r = ask_float("Annual rate % (R): ")
    t = ask_float("Time in years (T): ")
    res = simple_interest(p, r, t)
    banner("Simple Interest")
    line("Principal", res["principal"])
    line("Interest (SI)", res["interest"])
    line("Total amount", res["total"])


def do_compound() -> None:
    p = ask_float("Principal (P): ")
    r = ask_float("Annual rate % (R): ")
    t = ask_float("Time in years (T): ")
    n = ask_compounding()
    res = compound_amount(p, r, t, n)
    banner("Compound Interest")
    line("Principal", res["principal"])
    line("Interest earned", res["interest"])
    line("Compound amount (A)", res["total"])


def do_emi() -> None:
    p = ask_float("Loan amount (P): ", 0, allow_equal=False)
    r = ask_float("Annual interest rate %: ")
    t = ask_float("Loan tenure in years: ", 0, allow_equal=False)
    res = loan_emi(p, r, t)
    banner("Loan EMI")
    line("Monthly EMI", res["emi"])
    line("Total interest", res["total_interest"])
    line("Total payment", res["total_payment"])
    print(f"  {'Number of EMIs':<20}{res['months']:>16}")

    if input("\nShow amortization schedule? (y/n) [n]: ").strip().lower() == "y":
        print(f"\n  {'Mon':<5}{'EMI':>12}{'Interest':>12}{'Principal':>12}{'Balance':>14}")
        print("  " + "-" * 55)
        for m, emi, intr, prin, bal in amortization_schedule(p, r, t):
            print(f"  {m:<5}{emi:>12,.2f}{intr:>12,.2f}{prin:>12,.2f}{bal:>14,.2f}")


def do_sip() -> None:
    m = ask_float("Monthly SIP amount (M): ")
    r = ask_float("Expected annual return %: ")
    t = ask_float("Investment period in years: ")
    res = sip_future_value(m, r, t)
    banner("SIP Future Value")
    line("Total invested", res["invested"])
    line("Estimated returns", res["returns"])
    line("Future value", res["future_value"])


def do_doubling() -> None:
    r = ask_float("Annual rate %: ", 0, allow_equal=False)
    res = doubling_time(r)
    banner("Doubling Time")
    print(f"  Rule of 72 (72 / R)     : {res['rule_of_72']:.2f} years")
    print(f"  Exact (ln2 / ln(1+R/100)): {res['exact']:.2f} years")


MENU = {
    "1": ("Simple interest", do_simple),
    "2": ("Compound amount", do_compound),
    "3": ("Loan EMI", do_emi),
    "4": ("SIP future value", do_sip),
    "5": ("Doubling time", do_doubling),
}


def main() -> None:
    print("=== Interest Calculator in Python ===")
    while True:
        print("\nChoose a calculation:")
        for key, (name, _) in MENU.items():
            print(f"  {key}. {name}")
        print("  6. Quit")
        choice = input("Option (1-6): ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        if choice in MENU:
            try:
                MENU[choice][1]()
            except (ValueError, ZeroDivisionError) as err:
                print(f"  Error: {err}")
        else:
            print("  Invalid option, please choose 1-6.")


if __name__ == "__main__":
    main()
