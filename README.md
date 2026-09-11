# 🤖 Nivaaran

### Understand Money. Build a Better Future.

Nivaaran is an AI-powered **Financial Inclusion and Financial Literacy Chatbot** developed in alignment with **UN Sustainable Development Goal 1: No Poverty**.

The goal of Nivaaran is to make basic financial knowledge easier to understand and more accessible through a simple, natural, and conversational AI experience.

---

## 🌍 SDG Alignment

### SDG 1: No Poverty

Nivaaran focuses on the financial inclusion aspect of poverty reduction by helping users improve their understanding of everyday financial concepts and make more informed financial decisions.

---

## 💡 What is Nivaaran?

Nivaaran works as a conversational AI assistant that users can interact with naturally, similar to modern AI assistants such as ChatGPT and Gemini.

Users can ask questions about:

- 💰 Budgeting
- 🏦 Banking basics
- 💵 Saving money
- 📊 Expense management
- 💳 Credit and debt awareness
- 🏧 Digital payments
- 📱 UPI safety
- 🚨 Financial scams and fraud
- 📚 Financial terminology
- 🧠 Basic financial literacy
- 🏛️ Public-support resources
- 🔐 Online financial safety

The chatbot explains concepts in simple and beginner-friendly language.

---

## ✨ Key Features

### 🔐 User Authentication

- User registration
- Secure login
- Password hashing
- User sessions
- Logout functionality

### 💬 AI Conversation

- Natural conversational interaction
- Context-aware responses
- Follow-up questions
- Beginner-friendly explanations
- AI typing/loading indicator

### 🗂️ Chat Management

- Create a new chat
- Save conversations
- Chat history
- Continue previous conversations
- Conversation titles
- Delete conversations

### 💡 Financial Education

Nivaaran helps users understand financial concepts without using unnecessarily complicated terminology.

### 🚨 Scam Awareness

The chatbot can educate users about common financial scams such as:

- Phishing
- Fake loan offers
- OTP scams
- Fraudulent payment requests
- Fake investment schemes
- Suspicious links
- Identity theft

### 🛡️ Safety First

Nivaaran does not request sensitive information such as:

- Passwords
- OTPs
- PINs
- CVV
- Full card numbers
- Banking credentials

---

## 🤖 AI Technology

Nivaaran uses the **Google Gemini API** to generate conversational responses.

The API key is stored securely using environment variables/secrets and is not included in the source code.

---

## 🛠️ Technology Stack

### Frontend
- Streamlit / modern web interface

### Backend
- Python

### AI
- Google Gemini API

### Database
- SQLite
- SQLAlchemy

### Authentication
- Secure password hashing
- Session-based authentication

### Development
- Git
- GitHub
- VS Code

---

## 🔒 Financial Safety Disclaimer

Nivaaran is an **educational and financial-literacy assistant**.

It does not provide professional financial, investment, legal, or tax advice.

Information provided by the chatbot should be treated as general educational guidance. Users should consult a qualified professional before making important financial decisions.

---

## 🔑 API Configuration

Create a `.env` file locally and configure your Gemini API key.

Example:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=your_model_here
JWT_SECRET=your_secure_secret_here
