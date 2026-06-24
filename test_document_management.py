from src.database.document_repository import (
    save_document,
    get_documents_by_user,
    delete_document,
    get_document_by_id
)
from src.database.user_repository import (
    get_user_by_username
)

print("=== Document Management Tests ===\n")

# Get test users
user1 = get_user_by_username("testuser2")
if not user1:
    print("✗ Test user not found. Please create testuser2 first.")
    exit(1)

user1_id = user1.id
print(f"Using test user 1: {user1.username} (ID: {user1_id})")

user2 = get_user_by_username("testuser")
if not user2:
    print("✗ Test user 2 not found. Please create testuser first.")
    exit(1)

user2_id = user2.id
print(f"Using test user 2: {user2.username} (ID: {user2_id})\n")

# Test 1: Save document
print("Test 1: Saving document...")
try:
    doc = save_document(
        user1_id,
        "test_document.pdf",
        "data/raw/test_document.pdf"
    )
    print(f"✓ Document saved with ID: {doc.id}")
    print(f"  Filename: {doc.filename}")
    print(f"  Filepath: {doc.filepath}")
except Exception as e:
    print(f"✗ Error saving document: {e}")

# Test 2: Duplicate upload prevention
print("\nTest 2: Testing duplicate upload prevention...")
try:
    save_document(
        user1_id,
        "test_document.pdf",
        "data/raw/test_document.pdf"
    )
    print("✗ Duplicate upload was allowed (should fail)")
except ValueError as e:
    print(f"✓ Duplicate upload prevented: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")

# Test 3: Save another document for user1
print("\nTest 3: Saving another document for user1...")
try:
    doc2 = save_document(
        user1_id,
        "test_document2.pdf",
        "data/raw/test_document2.pdf"
    )
    print(f"✓ Second document saved with ID: {doc2.id}")
except Exception as e:
    print(f"✗ Error saving document: {e}")

# Test 4: Save document for user2
print("\nTest 4: Saving document for user2...")
try:
    doc3 = save_document(
        user2_id,
        "user2_document.pdf",
        "data/raw/user2_document.pdf"
    )
    print(f"✓ Document for user2 saved with ID: {doc3.id}")
except Exception as e:
    print(f"✗ Error saving document: {e}")

# Test 5: Verify same filename can be uploaded by different users
print("\nTest 5: Testing same filename for different users...")
try:
    doc4 = save_document(
        user2_id,
        "test_document.pdf",
        "data/raw/user2_test_document.pdf"
    )
    print(f"✓ Same filename allowed for different users (ID: {doc4.id})")
except ValueError as e:
    print(f"✗ Same filename blocked for different user: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")

# Test 6: Ownership verification - user1 tries to delete user2's document
print("\nTest 6: Testing ownership verification (user1 deletes user2's doc)...")
try:
    result = delete_document(doc3.id, user1_id)
    print("✗ User1 was able to delete user2's document (should fail)")
except PermissionError as e:
    print(f"✓ Ownership verification works: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")

# Test 7: User can delete their own document
print("\nTest 7: Testing user can delete their own document...")
try:
    result = delete_document(doc2.id, user1_id)
    if result:
        print("✓ User successfully deleted their own document")
    else:
        print("✗ Deletion failed")
except Exception as e:
    print(f"✗ Error deleting own document: {e}")

# Test 8: Verify document is deleted
print("\nTest 8: Verifying document is deleted from user's list...")
try:
    documents = get_documents_by_user(user1_id)
    doc_ids = [d.id for d in documents]
    if doc2.id not in doc_ids:
        print("✓ Document no longer in user's list after deletion")
    else:
        print("✗ Document still in list after deletion")
except Exception as e:
    print(f"✗ Error verifying deletion: {e}")

# Test 9: Get documents by user
print("\nTest 9: Getting documents by user...")
try:
    documents = get_documents_by_user(user1_id)
    print(f"✓ Retrieved {len(documents)} documents for user1")
    for doc in documents:
        print(f"  - {doc.filename} (ID: {doc.id})")
except Exception as e:
    print(f"✗ Error getting documents: {e}")

# Test 10: Verify document order (most recent first)
print("\nTest 10: Verifying document order (most recent first)...")
try:
    documents = get_documents_by_user(user1_id)
    if documents and documents[0].filename == "test_document.pdf":
        print("✓ Documents are ordered correctly (most recent first)")
    else:
        print("✗ Document order is incorrect")
except Exception as e:
    print(f"✗ Error verifying document order: {e}")

# Cleanup
print("\nCleaning up test data...")
try:
    documents = get_documents_by_user(user1_id)
    for doc in documents:
        if "test_document" in doc.filename:
            delete_document(doc.id, user1_id)
    
    documents = get_documents_by_user(user2_id)
    for doc in documents:
        if "test_document" in doc.filename or "user2" in doc.filename:
            delete_document(doc.id, user2_id)
    
    print("✓ Test data cleaned up")
except Exception as e:
    print(f"✗ Error cleaning up: {e}")

print("\n=== Document Management Tests Completed ===")
