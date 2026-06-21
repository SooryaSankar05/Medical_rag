from src.database.user_repository import (
    create_user,
    get_user_by_username,
    verify_user_credentials
)

# Test 1: Create a user
print("Test 1: Creating user...")
try:
    user = create_user("testuser", "testpass123")
    print(f"✓ User created: {user.username} with ID: {user.id}")
except Exception as e:
    print(f"✗ Error creating user: {e}")

# Test 2: Get user by username
print("\nTest 2: Getting user by username...")
user = get_user_by_username("testuser")
if user:
    print(f"✓ User found: {user.username} with ID: {user.id}")
else:
    print("✗ User not found")

# Test 3: Verify correct credentials
print("\nTest 3: Verifying correct credentials...")
result = verify_user_credentials("testuser", "testpass123")
if result:
    print("✓ Credentials verified successfully")
else:
    print("✗ Credential verification failed")

# Test 4: Verify incorrect credentials
print("\nTest 4: Verifying incorrect credentials...")
result = verify_user_credentials("testuser", "wrongpass")
if not result:
    print("✓ Incorrect credentials rejected as expected")
else:
    print("✗ Incorrect credentials accepted (should fail)")

# Test 5: Verify non-existent user
print("\nTest 5: Verifying non-existent user...")
result = verify_user_credentials("nonexistent", "testpass123")
if not result:
    print("✓ Non-existent user rejected as expected")
else:
    print("✗ Non-existent user accepted (should fail)")

# Test 6: Duplicate username check
print("\nTest 6: Testing duplicate username check...")
try:
    create_user("testuser", "anotherpass")
    print("✗ Duplicate username was allowed (should fail)")
except ValueError as e:
    print(f"✓ Duplicate username rejected: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")

# Test 7: Create another user to verify uniqueness
print("\nTest 7: Creating another unique user...")
try:
    user2 = create_user("testuser2", "testpass456")
    print(f"✓ Second user created: {user2.username} with ID: {user2.id}")
except Exception as e:
    print(f"✗ Error creating second user: {e}")

print("\n=== All authentication tests completed ===")
