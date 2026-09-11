#!/usr/bin/env python3
"""
Automated Test Suite for Nivaaran Backend.
Tests Auth, Database Models, JWT Security, Conversation CRUD, AI Safety Prompts, and Public Resources.
"""

import sys
import os
import asyncio
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
from backend.database import SessionLocal, init_db
from backend.models import User, Conversation, Message, PublicResource
from backend.ai_service import generate_chat_response, generate_conversation_title, build_fallback_response

client = TestClient(app)


def run_all_tests():
    print("========================================")
    print("🚀 Starting Nivaaran Automated Test Suite")
    print("========================================")

    init_db()

    # 1. Health Check
    print("\n[1/7] Testing Health Check Endpoint...")
    resp = client.get("/api/health")
    assert resp.status_code == 200, f"Health check failed: {resp.text}"
    data = resp.json()
    assert data["status"] == "online"
    assert "SDG 1" in data["sdg_goal"]
    print("  ✅ Health check passed:", data)

    # 2. User Registration
    print("\n[2/7] Testing User Registration...")
    test_email = "aniruddh.test@nivaaran.org"
    test_pass = "SecurePass123!"
    
    # Clean up any existing test user
    db = SessionLocal()
    existing = db.query(User).filter(User.email == test_email).first()
    if existing:
        db.delete(existing)
        db.commit()
    db.close()

    resp = client.post("/api/auth/register", json={
        "email": test_email,
        "full_name": "Aniruddh Test User",
        "password": test_pass
    })
    assert resp.status_code == 201, f"Registration failed: {resp.text}"
    reg_data = resp.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == test_email
    token = reg_data["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    print("  ✅ Registration successful! Token generated.")

    # Duplicate registration test
    resp_dup = client.post("/api/auth/register", json={
        "email": test_email,
        "full_name": "Aniruddh Duplicate",
        "password": test_pass
    })
    assert resp_dup.status_code == 400, "Duplicate registration should fail"
    print("  ✅ Duplicate registration correctly rejected with 400.")

    # 3. User Login & /me verification
    print("\n[3/7] Testing User Login & Session Verification...")
    resp_login = client.post("/api/auth/login", json={
        "email": test_email,
        "password": test_pass
    })
    assert resp_login.status_code == 200, f"Login failed: {resp_login.text}"
    login_data = resp_login.json()
    assert login_data["user"]["full_name"] == "Aniruddh Test User"

    # Test /me endpoint with token
    resp_me = client.get("/api/auth/me", headers=auth_headers)
    assert resp_me.status_code == 200
    assert resp_me.json()["email"] == test_email
    print("  ✅ Login and session profile verification successful.")

    # 4. Conversations List & Create
    print("\n[4/7] Testing Conversation CRUD...")
    # List conversations (should include the welcome conversation created at registration)
    resp_list = client.get("/api/conversations", headers=auth_headers)
    assert resp_list.status_code == 200
    conv_list = resp_list.json()
    assert len(conv_list) >= 1
    welcome_id = conv_list[0]["id"]
    print(f"  ✅ Listed {len(conv_list)} existing conversation(s).")

    # Create new conversation
    resp_new_conv = client.post("/api/conversations", json={
        "title": "Budgeting Advice",
        "initial_message": "I make ₹25,000 per month. How should I save?"
    }, headers=auth_headers)
    assert resp_new_conv.status_code == 201, f"Create conv failed: {resp_new_conv.text}"
    new_conv_data = resp_new_conv.json()
    conv_id = new_conv_data["id"]
    assert len(new_conv_data["messages"]) == 2  # user + assistant
    print("  ✅ Created new conversation with initial prompt and AI response.")

    # Rename conversation
    resp_rename = client.patch(f"/api/conversations/{conv_id}", json={
        "title": "₹25k Monthly Budget Plan"
    }, headers=auth_headers)
    assert resp_rename.status_code == 200
    assert resp_rename.json()["title"] == "₹25k Monthly Budget Plan"
    print("  ✅ Renamed conversation successfully.")

    # 5. Sending Follow-up Messages & Regeneration
    print("\n[5/7] Testing Multi-turn Messaging & Response Generation...")
    resp_msg = client.post(f"/api/conversations/{conv_id}/messages", json={
        "content": "What if I have an existing personal loan of ₹15,000 at 14% interest?"
    }, headers=auth_headers)
    assert resp_msg.status_code == 200, f"Send msg failed: {resp_msg.text}"
    msg_data = resp_msg.json()
    assert msg_data["role"] == "assistant"
    assert len(msg_data["content"]) > 30
    print("  ✅ Received follow-up AI message:", msg_data["content"][:100] + "...")

    # Test regenerate
    resp_regen = client.post(f"/api/conversations/{conv_id}/regenerate", headers=auth_headers)
    assert resp_regen.status_code == 200
    regen_data = resp_regen.json()
    assert regen_data["role"] == "assistant"
    print("  ✅ Response regeneration successful.")

    # Delete conversation
    resp_del = client.delete(f"/api/conversations/{conv_id}", headers=auth_headers)
    assert resp_del.status_code == 204
    print("  ✅ Conversation deleted successfully.")

    # 6. Financial Safety & Scam Guardrails
    print("\n[6/7] Testing Financial Safety & Scam Guardrails...")
    scam_test = build_fallback_response("Someone called me asking for my OTP to verify my bank account", [])
    assert "Never Share OTP" in scam_test or "1930" in scam_test
    print("  ✅ Scam safety alert triggered properly with 1930 Helpline advice.")

    # 7. Public Resources Queries
    print("\n[7/7] Testing Verified Public Resources API...")
    resp_res = client.get("/api/resources")
    assert resp_res.status_code == 200
    resources = resp_res.json()
    assert len(resources) >= 10, f"Expected at least 10 seeded resources, got {len(resources)}"
    
    # Filter by category
    resp_cat = client.get("/api/resources?category=Banking")
    assert resp_cat.status_code == 200
    assert all(r["category"] == "Banking" for r in resp_cat.json())

    # Search
    resp_search = client.get("/api/resources?search=Jan Dhan")
    assert resp_search.status_code == 200
    assert len(resp_search.json()) >= 1
    print(f"  ✅ Resources API verified with {len(resources)} verified schemes.")

    print("\n========================================")
    print("🎉 ALL 7 TEST SUITES PASSED FLAWLESSLY!")
    print("========================================")


if __name__ == "__main__":
    run_all_tests()
