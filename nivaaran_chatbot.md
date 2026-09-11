# Directive: Nivaaran Financial Inclusion Assistant

## Objective
Provide a reliable, conversational, AI-powered financial education and safety chatbot focused on **SDG 1: No Poverty**. Ensure safe financial literacy guidance, scam awareness, budget management, and verified public scheme recommendations.

## Inputs
- User query text & conversation history
- User JWT token for authenticated operations
- Google Gemini API key (`GEMINI_API_KEY`) via `.env`
- Verified public resources database

## Tools and Scripts
- Deterministic seeding: `python3 execution/seed_resources.py`
- Test suite: `python3 execution/test_suite.py`
- Server startup: `python3 execution/run_server.py`

## AI Behavior & Safety Guardrails
1. **Financial Education vs Professional Advice**:
   - Always clarify that Nivaaran is an educational tool, not a certified financial planner.
   - For complex taxes, legal issues, or high-risk investments, advise consulting accredited professionals.
2. **Strict Scam & Credential Protection**:
   - NEVER ask for OTPs, PINs, passwords, CVV, or account numbers.
   - Proactively warn users if scam keywords (e.g., "bank asking for OTP", "lottery prize", "remote screen sharing") appear in chat.
3. **Conversational Style**:
   - Friendly, empathetic, jargon-free, encouraging, and structured with clean markdown bullet points.

## Edge Cases
- **Missing Gemini API Key**: The AI service gracefully falls back to local contextual educational heuristics without crashing.
- **Malformed Inputs**: Handled by Pydantic validation schemas with appropriate HTTP error codes.
