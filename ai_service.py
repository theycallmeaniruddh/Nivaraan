import os
import re
import logging
from typing import List, Dict, Any, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# System Prompt embodying SDG 1 Financial Inclusion, Financial Literacy, Safety & Disclaimer
NIVAARAN_SYSTEM_INSTRUCTION = """
You are "Nivaaran" (निवारण), an empathetic, friendly, and highly knowledgeable AI Financial Inclusion Assistant.
Your core mission is aligned with UN Sustainable Development Goal 1 (SDG 1: No Poverty) - helping individuals, families, daily earners, small business owners, and beginners achieve financial stability, literacy, and security.

### Your Core Principles:
1. **Explain Simply & Clearly**: Break down complicated financial concepts (budgeting, compounding interest, inflation, debt traps, credit scores, insurance) into simple, everyday language and relatable analogies.
2. **Actionable & Realistic Guidance**:
   - Provide realistic breakdowns (e.g. 50/30/20 rule, envelope method, micro-savings, emergency fund building).
   - Tailor examples to realistic incomes (e.g. ₹10,000, ₹20,000, ₹50,000/month or informal earnings).
3. **Financial Safety & Scam Protection (CRITICAL)**:
   - NEVER ask for sensitive credentials: OTP, UPI PIN, ATM PIN, passwords, CVV, or full card numbers.
   - Proactively warn users if they mention suspicious calls, SMS links, lottery wins, fake work-from-home tasks, electricity disconnection threats, or urgent requests for remote access apps (AnyDesk, TeamViewer).
   - Educate on the Golden Rule of UPI: "You NEVER need to enter your UPI PIN to RECEIVE money, only to SEND money."
   - Advise victims of cyber financial fraud to immediately call the National Cyber Crime Helpline at 1930 or report on cybercrime.gov.in.
4. **Verified Public Support & Government Schemes (India / Financial Inclusion)**:
   - Promote verified public programs when relevant:
     - *PM Jan Dhan Yojana (PMJDY)*: Zero-balance basic savings bank account, RuPay card, accidental insurance.
     - *PM Suraksha Bima Yojana (PMSBY)*: ₹20/year accident insurance cover (₹2 Lakh).
     - *PM Jeevan Jyoti Bima Yojana (PMJJBY)*: ₹436/year life insurance cover (₹2 Lakh).
     - *Atal Pension Yojana (APY)*: Guaranteed monthly pension of ₹1,000-₹5,000 for unorganized workers from age 60.
     - *PM Mudra Yojana (PMMY)*: Micro-credit business loans (Shishu up to ₹50,000, Kishore up to ₹5 Lakh, Tarun up to ₹10 Lakh).
     - *PM SVANidhi*: Collateral-free working capital loan for street vendors.
     - *RBI Ombudsman / Sachet Portal*: Official grievance redressal against unauthorized lenders and banking disputes.
   - Never invent schemes, unrealistic rates, or fake contact numbers.
5. **Educational Disclaimer**:
   - Maintain a non-judgmental, supportive tone.
   - Distinguish general financial education from licensed financial planning. Avoid guaranteeing returns or recommending specific speculative stocks/crypto.
   - Recommend consulting a certified financial planner, tax advisor, or authorized bank official for formal contractual decisions.

### Format & Tone:
- Use clean Markdown with headers (`###`), bullet points, bold key terms, and structured tables or step-by-step checklists when helpful.
- Provide a brief 1-2 sentence supportive follow-up question or suggestion at the end of relevant responses to keep the dialogue natural and encouraging.
"""


def _clean_api_key(key: str) -> str:
    if not key or key.startswith("your_") or "api_key" in key:
        return ""
    return key.strip()


def build_fallback_response(user_message: str, conversation_history: List[Dict[str, str]]) -> str:
    """Intelligent educational fallback response engine when API key is missing or offline."""
    query = user_message.lower()

    # 1. Scam & Security Safety Check
    if any(w in query for w in ["otp", "pin", "scam", "fraud", "hacked", "stolen", "fake", "link", "lottery", "urgent call"]):
        return (
            "### 🚨 Financial Safety & Scam Alert\n\n"
            "If someone is asking you for sensitive banking information or you suspect a scam, please follow these golden safety rules immediately:\n\n"
            "- **Never Share OTP or UPI PIN**: Bank officials, police, and government staff will **never** ask you for your OTP, UPI PIN, ATM PIN, or password.\n"
            "- **Receiving Money Rule**: You **never** need to scan a QR code or enter your UPI PIN to *receive* money. A PIN is only required to *send* money.\n"
            "- **No Remote Screen Sharing**: Never install remote access applications like AnyDesk, TeamViewer, or RustDesk on the instruction of an unknown caller.\n"
            "- **Immediate Action for Fraud**: If you have lost money to cyber fraud, immediately report it to the **National Cyber Crime Helpline at 1930** or file a complaint at [cybercrime.gov.in](https://cybercrime.gov.in) within 2-4 hours to increase the chance of freezing the transaction.\n"
            "- **Bank Helpline**: Call your bank's official toll-free number (printed on your debit card) to block your card and digital banking access immediately.\n\n"
            "*Nivaaran is an educational assistant and will never ask you for your passwords or credentials. Did you receive a specific suspicious message or link you'd like to check?*"
        )

    # 2. Budgeting & Saving (e.g. 20000 per month)
    if any(w in query for w in ["budget", "save", "saving", "earn", "salary", "20000", "10000", "50000", "15000", "income", "manage money"]):
        amount_match = re.search(r'₹?\s*(\d{1,2}(?:,\d{2,3})*(?:\.\d+)?|\d+)\s*(?:k|thousand|rupees|per month|/mo|pm)?', query)
        salary_text = "₹20,000"
        if amount_match and int(amount_match.group(1).replace(",", "")) > 1000:
            salary_text = f"₹{amount_match.group(1)}"

        return (
            f"### 💡 Smart Budgeting & Saving Guide ({salary_text}/month)\n\n"
            f"Managing an income of **{salary_text} per month** effectively is all about consistency and building a solid financial cushion. Here is a practical, step-by-step roadmap:\n\n"
            "#### 1. The 50 / 30 / 20 Budget Rule (Adapted for Beginners)\n"
            "- **50% Needs (Essential Living Costs)**: Rent, groceries, electricity, cooking gas, essential commuting. Try to keep these within 50-60% of your earnings.\n"
            "- **30% Wants (Lifestyle & Family)**: Occasional dining, festival gifts, mobile recharge, personal clothing.\n"
            "- **20% Savings & Debt Repayment**: Building an emergency fund, recurring deposits, or paying off high-interest debt first.\n\n"
            "#### 2. Three Practical Steps to Start Saving Today\n"
            "1. **Build a Mini-Emergency Fund**: Start by saving even ₹500 to ₹1,000 every month in a separate savings account (e.g., a zero-balance PM Jan Dhan account) until you reach 1-3 months of basic expenses.\n"
            "2. **Track Expenses for 30 Days**: Note every daily expense on a notebook or simple tracker. Identifying small daily leaks (like impulse snacks or unused subscriptions) can easily free up ₹1,000–₹2,000/month.\n"
            "3. **Automate Your Savings on Payday**: Move your planned savings on the day you receive your income, rather than saving whatever happens to be left at the end of the month.\n\n"
            "#### 3. Low-Risk Government Savings Schemes to Explore\n"
            "- **Post Office Recurring Deposit (RD)** or **Bank RD**: Start with as little as ₹100/month for guaranteed interest.\n"
            "- **Public Provident Fund (PPF)**: Long-term tax-free compounding starting at ₹500/year.\n\n"
            "*Disclaimer: This information is for financial literacy and educational purposes. Would you like help calculating a custom expense breakdown or understanding how to manage existing loans?*"
        )

    # 3. Debt & Loans
    if any(w in query for w in ["debt", "loan", "emi", "interest", "credit", "repay", "trap", "overdue", "borrow"]):
        return (
            "### 📉 Step-by-Step Guide to Debt Awareness & Management\n\n"
            "Dealing with loans and EMIs can feel overwhelming, but structured repayment strategies can help you regain control:\n\n"
            "#### 1. Prioritize High-Interest Debt (The Avalanche Method)\n"
            "- List all your debts: credit cards, instant app loans, personal loans, informal borrowings.\n"
            "- Pay minimum required EMIs on all debts to avoid penalties.\n"
            "- Direct every spare rupee toward the loan with the **highest interest rate** first. Once that is cleared, move to the next highest.\n\n"
            "#### 2. Beware of Predatory Instant Loan Apps\n"
            "- **Only borrow from RBI-registered NBFCs or Banks**. Check if the lender is listed on the official [RBI Sachet Portal](https://sachet.rbi.org.in).\n"
            "- Never download unverified APKs or give contacts/gallery permissions to instant loan apps.\n"
            "- If harassed by illegal apps, report them immediately to your local cyber police or RBI Ombudsman.\n\n"
            "#### 3. Avoid Debt Stacking\n"
            "- Never take a new high-interest loan just to pay off an existing loan EMI unless it is a formal, lower-interest consolidation with a registered bank.\n\n"
            "*Disclaimer: Educational guidance only. Would you like to share the types of loans (e.g. personal, bank, informal) you want to structure without sharing personal numbers?*"
        )

    # 4. Government Schemes & Public Resources
    if any(w in query for w in ["scheme", "government", "pmjdy", "jan dhan", "bima", "pension", "apy", "mudra", "welfare", "subsidy", "svanidhi"]):
        return (
            "### 🏛️ Verified Public Financial Support & Welfare Schemes\n\n"
            "The Government of India and RBI offer several financial inclusion programs designed for low-income earners, self-employed workers, and families:\n\n"
            "| Scheme Name | Key Benefit | Eligibility / Cost |\n"
            "| :--- | :--- | :--- |\n"
            "| **Pradhan Mantri Jan Dhan Yojana (PMJDY)** | Zero-balance savings account, RuPay debit card, ₹2 Lakh accident cover | Any Indian citizen without a bank account |\n"
            "| **PM Suraksha Bima Yojana (PMSBY)** | ₹2 Lakh accidental death / disability coverage | Age 18–70, only **₹20 / year** |\n"
            "| **PM Jeevan Jyoti Bima Yojana (PMJJBY)** | ₹2 Lakh life insurance coverage for any cause | Age 18–50, only **₹436 / year** |\n"
            "| **Atal Pension Yojana (APY)** | Guaranteed monthly pension of ₹1,000–₹5,000 after age 60 | Age 18–40 unorganized sector workers |\n"
            "| **PM Mudra Yojana (PMMY)** | Business micro-credit up to ₹10 Lakh (Shishu, Kishore, Tarun) | Micro-enterprises, small shopkeepers |\n"
            "| **PM SVANidhi** | Collateral-free working capital loan up to ₹50,000 with 7% interest rebate | Street vendors & urban micro-merchants |\n\n"
            "*You can check our **Verified Resources** tab for direct official government portals. Which scheme would you like detailed eligibility steps for?*"
        )

    # 5. General greeting or financial inquiry
    return (
        "### 🌟 Welcome to Nivaaran — Your Financial Inclusion Assistant\n\n"
        "I'm here to make personal finance, budgeting, and public financial schemes simple, safe, and accessible to everyone.\n\n"
        "Here are key areas I can help you with:\n"
        "- 💰 **Budgeting & Savings**: Practical plans for any income level (e.g., 50/30/20 rule, emergency funds).\n"
        "- 🛡️ **Scam & UPI Safety**: How to protect your bank account and what to do if you suspect fraud.\n"
        "- 📉 **Debt & Loan Awareness**: Strategies to clear high-interest loans and avoid debt traps.\n"
        "- 🏛️ **Government Welfare Schemes**: Eligibility for Jan Dhan, insurance at ₹20/year, Atal Pension, and Mudra business loans.\n"
        "- 📱 **Digital Payments**: Safely navigating UPI, RuPay, and mobile banking.\n\n"
        "How can I assist you with your financial journey today?\n\n"
        "*Disclaimer: Nivaaran provides general financial education and literacy resources. I never ask for your passwords, OTPs, or bank PINs.*"
    )


async def generate_chat_response(
    messages: List[Dict[str, str]],
    model_name: Optional[str] = None
) -> str:
    """
    Generate an AI response using Google Gemini API with multi-model fallback and local reasoning backup.
    `messages` format: list of {"role": "user" | "assistant", "content": "..."}
    """
    api_key = _clean_api_key(os.getenv("GEMINI_API_KEY", GEMINI_API_KEY))
    preferred_model = model_name or os.getenv("GEMINI_MODEL", "gemini-flash-latest")
    user_query = messages[-1]["content"] if messages else ""

    if not api_key:
        logger.info("No Gemini API key provided. Using built-in financial inclusion knowledge engine.")
        return build_fallback_response(user_query, messages[:-1])

    candidate_models = [
        preferred_model,
        "gemini-flash-latest",
        "gemini-3.5-flash",
        "gemini-flash-lite-latest",
        "gemini-pro-latest"
    ]
    # Remove duplicate order while preserving first preference
    seen = set()
    candidate_models = [m for m in candidate_models if not (m in seen or seen.add(m))]

    # 1. Attempt using google.genai SDK
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        # Convert chat history to Gemini contents format
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        config = types.GenerateContentConfig(
            system_instruction=NIVAARAN_SYSTEM_INSTRUCTION,
            temperature=0.7,
            max_output_tokens=2048,
        )

        for candidate in candidate_models:
            try:
                response = client.models.generate_content(
                    model=candidate,
                    contents=contents,
                    config=config
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as model_err:
                logger.warning(f"Model {candidate} failed: {model_err}. Trying next candidate...")

    except Exception as e:
        logger.warning(f"google.genai SDK execution error: {e}. Attempting REST API fallback.")

    # 2. Fallback to direct Gemini REST API call via httpx
    for candidate in candidate_models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{candidate}:generateContent?key={api_key}"
            
            gemini_contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                gemini_contents.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })

            payload = {
                "system_instruction": {
                    "parts": [{"text": NIVAARAN_SYSTEM_INSTRUCTION}]
                },
                "contents": gemini_contents,
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048
                }
            }

            async with httpx.AsyncClient(timeout=30.0) as http_client:
                resp = await http_client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            return parts[0]["text"].strip()
                else:
                    logger.warning(f"Gemini REST returned {resp.status_code} for {candidate}")

        except Exception as e:
            logger.error(f"Gemini REST API error for {candidate}: {e}")

    # If all external API calls fail or timeout, use built-in financial knowledge response
    logger.info("Falling back to local financial education reasoning engine.")
    return build_fallback_response(user_query, messages[:-1])


async def generate_conversation_title(first_message: str) -> str:
    """Generate a clean, concise 3-6 word title for a conversation based on the first prompt."""
    if not first_message:
        return "New Financial Conversation"

    cleaned = re.sub(r'[^\w\s₹$€%]', '', first_message).strip()
    words = cleaned.split()

    if len(words) <= 5:
        title = " ".join(words)
    else:
        title = " ".join(words[:5])

    title = title.capitalize()
    if len(title) > 45:
        title = title[:42] + "..."

    return title if title else "Financial Literacy Session"
