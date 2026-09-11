#!/usr/bin/env python3
"""
Seed script for Nivaaran Verified Public Resources.
Populates the SQLite database with verified government schemes, financial inclusion portals, and safety helplines.
"""

import sys
import os

# Add parent directory to python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, init_db
from backend.models import PublicResource

VERIFIED_RESOURCES = [
    # Banking & Savings
    {
        "title": "Pradhan Mantri Jan Dhan Yojana (PMJDY)",
        "category": "Banking",
        "description": "National mission for financial inclusion ensuring access to basic savings bank accounts with zero minimum balance, RuPay debit card, and free accidental insurance cover of ₹2 Lakh.",
        "eligibility": "Any Indian citizen above age 10 without a bank account. Requires basic KYC (Aadhaar or Voter ID).",
        "official_url": "https://pmjdy.gov.in",
        "helpline": "1800-180-1111 / 1800-11-0001",
        "verified": True
    },
    {
        "title": "Basic Savings Bank Deposit Account (BSBDA)",
        "category": "Banking",
        "description": "RBI-mandated zero-balance savings account offered by all scheduled commercial banks in India with no minimum balance penalties and free cash deposit/withdrawal facilities.",
        "eligibility": "All individuals without prior bank accounts or seeking zero-cost basic banking.",
        "official_url": "https://rbi.org.in",
        "helpline": "14440 (RBI Financial Literacy)",
        "verified": True
    },
    {
        "title": "Post Office Savings Account & Recurring Deposit",
        "category": "Banking",
        "description": "Government-backed secure micro-savings with attractive interest rates starting from as low as ₹100/month, accessible in every local post office branch across rural and urban India.",
        "eligibility": "Open to all Indian residents, including minors via guardians.",
        "official_url": "https://www.indiapost.gov.in",
        "helpline": "1800-266-6868",
        "verified": True
    },

    # Micro-Loans & Enterprise Support
    {
        "title": "Pradhan Mantri Mudra Yojana (PMMY)",
        "category": "Micro-Loans",
        "description": "Collateral-free micro-loans for non-corporate, non-farm small/micro enterprises. Split into 3 categories: Shishu (up to ₹50,000), Kishore (₹50,000 to ₹5 Lakh), and Tarun (₹5 Lakh to ₹10 Lakh).",
        "eligibility": "Small business owners, shopkeepers, artisans, fruit/vegetable vendors, and service providers.",
        "official_url": "https://www.mudra.org.in",
        "helpline": "1800-180-1111",
        "verified": True
    },
    {
        "title": "PM SVANidhi (Street Vendor's AtmaNirbhar Nidhi)",
        "category": "Micro-Loans",
        "description": "Special micro-credit facility providing affordable, collateral-free working capital loan starting at ₹10,000, progressing to ₹20,000 and ₹50,000 on timely repayment with 7% interest subsidy.",
        "eligibility": "Urban, peri-urban, and rural street vendors engaged in vending before March 24, 2020.",
        "official_url": "https://pmsvanidhi.mohua.gov.in",
        "helpline": "1800-11-1979",
        "verified": True
    },
    {
        "title": "Stand-Up India Scheme",
        "category": "Micro-Loans",
        "description": "Bank loans between ₹10 Lakh and ₹1 Crore to at least one Scheduled Caste (SC) or Scheduled Tribe (ST) borrower and at least one woman borrower per bank branch for setting up greenfield enterprises.",
        "eligibility": "SC/ST and women entrepreneurs above 18 years of age.",
        "official_url": "https://www.standupmitra.in",
        "helpline": "1800-180-1111",
        "verified": True
    },

    # Insurance & Social Security
    {
        "title": "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
        "category": "Insurance",
        "description": "High-affordability accident insurance providing ₹2 Lakh cover for accidental death or permanent total disability, and ₹1 Lakh for partial disability for an annual premium of just ₹20.",
        "eligibility": "Individuals aged 18 to 70 years with an active savings bank or post office account.",
        "official_url": "https://financialservices.gov.in/beta/en/pmsby",
        "helpline": "1800-180-1111",
        "verified": True
    },
    {
        "title": "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
        "category": "Insurance",
        "description": "One-year renewable life insurance scheme offering ₹2 Lakh cover for death due to any reason at a nominal premium of ₹436 per annum.",
        "eligibility": "Individuals aged 18 to 50 years having a bank/post office account.",
        "official_url": "https://financialservices.gov.in/beta/en/pmjjby",
        "helpline": "1800-180-1111",
        "verified": True
    },
    {
        "title": "Ayushman Bharat PM-JAY",
        "category": "Insurance",
        "description": "World's largest health assurance scheme providing health cover of ₹5 Lakh per family per year for secondary and tertiary care hospitalization across impaneled public and private hospitals.",
        "eligibility": "Bottom 40% vulnerable families identified based on SECC 2011 criteria.",
        "official_url": "https://pmjay.gov.in",
        "helpline": "14555",
        "verified": True
    },

    # Pension & Senior Citizen Security
    {
        "title": "Atal Pension Yojana (APY)",
        "category": "Pensions",
        "description": "Government-guaranteed pension scheme providing fixed monthly pension of ₹1,000, ₹2,000, ₹3,000, ₹4,000, or ₹5,000 after age 60 based on modest contribution amounts.",
        "eligibility": "All citizens aged 18 to 40 years holding a savings bank account who are not income tax payers.",
        "official_url": "https://npscra.nsdl.co.in/scheme-details.php",
        "helpline": "1800-110-069",
        "verified": True
    },
    {
        "title": "Sukanya Samriddhi Yojana (SSY)",
        "category": "Savings",
        "description": "High-interest, tax-free small savings scheme for girl children to support higher education and marriage expenses, opened from birth up to age 10 with minimum ₹250 annual deposit.",
        "eligibility": "Parents or legal guardians of a girl child below 10 years of age.",
        "official_url": "https://www.nsiindia.gov.in",
        "helpline": "1800-266-6868",
        "verified": True
    },

    # Consumer Safety, Helplines & Fraud Reporting
    {
        "title": "National Cyber Crime Reporting Helpline (1930)",
        "category": "Safety & Helplines",
        "description": "Immediate emergency response helpline and portal to report online financial frauds, UPI scams, fake payment apps, and credit card theft to freeze stolen funds in transit.",
        "eligibility": "Available 24/7 to all citizens across India.",
        "official_url": "https://cybercrime.gov.in",
        "helpline": "1930",
        "verified": True
    },
    {
        "title": "RBI Sachet Portal (Unregulated Deposit & Loan App Watch)",
        "category": "Safety & Helplines",
        "description": "Official Reserve Bank of India portal to verify if a financial entity/app is legally registered and to lodge complaints against illegal multi-level marketing, unauthorized loan apps, and fraudulent deposit schemes.",
        "eligibility": "Open to all public users.",
        "official_url": "https://sachet.rbi.org.in",
        "helpline": "14440",
        "verified": True
    },
    {
        "title": "RBI Integrated Ombudsman Scheme (CMS)",
        "category": "Safety & Helplines",
        "description": "One Nation One Ombudsman mechanism for free-of-cost grievance redressal against deficiencies in services provided by Banks, NBFCs, and Non-Bank Payment System Participants if not resolved by the bank within 30 days.",
        "eligibility": "Any customer of RBI-regulated banks or financial institutions.",
        "official_url": "https://cms.rbi.org.in",
        "helpline": "14448",
        "verified": True
    },
    {
        "title": "National Consumer Helpline (NCH)",
        "category": "Safety & Helplines",
        "description": "Official grievance redressal portal operated by the Department of Consumer Affairs for unfair trade practices, misleading financial advertisements, and defective financial services.",
        "eligibility": "All consumers.",
        "official_url": "https://consumerhelpline.gov.in",
        "helpline": "1915",
        "verified": True
    }
]


def seed():
    print("🌱 Initializing Database schema...")
    init_db()
    db = SessionLocal()

    try:
        # Check existing resources count
        existing_count = db.query(PublicResource).count()
        print(f"Current verified resources in DB: {existing_count}")

        added_count = 0
        updated_count = 0

        for r_data in VERIFIED_RESOURCES:
            existing = db.query(PublicResource).filter(PublicResource.title == r_data["title"]).first()
            if not existing:
                res = PublicResource(**r_data)
                db.add(res)
                added_count += 1
            else:
                for key, val in r_data.items():
                    setattr(existing, key, val)
                updated_count += 1

        db.commit()
        total = db.query(PublicResource).count()
        print(f"✅ Seeding complete: {added_count} added, {updated_count} updated. Total active resources: {total}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding resources: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
