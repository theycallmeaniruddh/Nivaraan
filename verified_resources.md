# Directive: Verified Public Financial Inclusion Resources

## Objective
Maintain a strictly verified catalog of official government schemes, public financial assistance programs, and consumer safety helplines in India to support SDG 1 (No Poverty).

## Verification Standard
- **Zero Hallucinations**: Never invent or estimate eligibility rules, interest rates, government schemes, or phone numbers.
- **Source of Truth**: Only include verified schemes published by the Government of India, Reserve Bank of India (RBI), or official statutory bodies.

## Approved Core Schemes Catalog
1. **Pradhan Mantri Jan Dhan Yojana (PMJDY)**
   - Portal: `https://pmjdy.gov.in`
   - Scope: Zero-balance savings account, RuPay debit card, ₹2 Lakh accidental insurance, ₹10,000 overdraft facility.
2. **Pradhan Mantri Suraksha Bima Yojana (PMSBY)**
   - Portal: `https://financialservices.gov.in/beta/en/pmsby`
   - Scope: ₹20/year accident insurance cover for ₹2 Lakh.
3. **Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)**
   - Portal: `https://financialservices.gov.in/beta/en/pmjjby`
   - Scope: ₹436/year life insurance cover for ₹2 Lakh.
4. **Atal Pension Yojana (APY)**
   - Portal: `https://npscra.nsdl.co.in/scheme-details.php`
   - Scope: Guaranteed monthly pension of ₹1,000 to ₹5,000 for unorganized sector workers upon reaching age 60.
5. **Pradhan Mantri Mudra Yojana (PMMY)**
   - Portal: `https://www.mudra.org.in`
   - Scope: Micro-credit loans up to ₹10 Lakh for small business enterprises (Shishu, Kishore, Tarun).
6. **National Cyber Crime Helpline**
   - Helpline: `1930`
   - Portal: `https://cybercrime.gov.in`
   - Scope: Immediate reporting of online financial fraud & UPI scams.
7. **RBI Sachet / Ombudsman Portal**
   - Portal: `https://sachet.rbi.org.in` & `https://cms.rbi.org.in`
   - Scope: Reporting illegal loan apps and escalating bank grievances.
8. **PM SVANidhi (Street Vendor's AtmaNirbhar Nidhi)**
   - Portal: `https://pmsvanidhi.mohua.gov.in`
   - Scope: Collateral-free working capital loan up to ₹50,000 with 7% interest subsidy for street vendors.

## Updating Resources
Run `python3 execution/seed_resources.py` to refresh or re-populate the SQLite database.
