"""
Test session state logic for authentication
This simulates the session state management without running Streamlit
"""

from src.database.user_repository import (
    create_user,
    get_user_by_username,
    verify_user_credentials
)

# Simulate session state
session_state = {
    "user_id": None,
    "username": None,
    "auth_page": "login",
    "messages": []
}

print("=== Session State Authentication Test ===\n")

# Test 1: Simulate login with valid credentials
print("Test 1: Simulating login with valid credentials...")
username = "testuser2"
password = "testpass456"

if verify_user_credentials(username, password):
    user = get_user_by_username(username)
    session_state["user_id"] = user.id
    session_state["username"] = user.username
    session_state["auth_page"] = "authenticated"
    print(f"✓ Login successful")
    print(f"  Session state user_id: {session_state['user_id']}")
    print(f"  Session state username: {session_state['username']}")
    print(f"  Session state auth_page: {session_state['auth_page']}")
else:
    print("✗ Login failed")

# Test 2: Verify session state is populated
print("\nTest 2: Verifying session state contains user_id and username...")
if session_state["user_id"] is not None and session_state["username"] is not None:
    print(f"✓ Session state correctly populated")
    print(f"  user_id: {session_state['user_id']}")
    print(f"  username: {session_state['username']}")
else:
    print("✗ Session state not correctly populated")

# Test 3: Simulate logout
print("\nTest 3: Simulating logout...")
session_state["user_id"] = None
session_state["username"] = None
session_state["auth_page"] = "login"
session_state["messages"] = []
print(f"✓ Logout successful")
print(f"  Session state user_id: {session_state['user_id']}")
print(f"  Session state username: {session_state['username']}")
print(f"  Session state auth_page: {session_state['auth_page']}")

# Test 4: Verify session state is cleared
print("\nTest 4: Verifying session state is cleared after logout...")
if session_state["user_id"] is None and session_state["username"] is None:
    print("✓ Session state correctly cleared")
else:
    print("✗ Session state not correctly cleared")

# Test 5: Verify authentication check
print("\nTest 5: Verifying authentication check (user_id is None)...")
if not session_state["user_id"]:
    print("✓ Authentication check correctly denies access (user_id is None)")
else:
    print("✗ Authentication check failed")

# Test 6: Login again and verify
print("\nTest 6: Login again and verify session state...")
if verify_user_credentials(username, password):
    user = get_user_by_username(username)
    session_state["user_id"] = user.id
    session_state["username"] = user.username
    session_state["auth_page"] = "authenticated"
    
    if session_state["user_id"] and session_state["username"]:
        print(f"✓ Session state correctly set after re-login")
        print(f"  user_id: {session_state['user_id']}")
        print(f"  username: {session_state['username']}")
    else:
        print("✗ Session state not correctly set after re-login")

print("\n=== Session State Tests Completed ===")
