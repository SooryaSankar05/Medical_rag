from src.database.chat_repository import (
    save_chat,
    load_chat,
    clear_chat
)
from src.database.user_repository import (
    get_user_by_username
)

print("=== Chat History Tests ===\n")

# Get a test user
user = get_user_by_username("testuser2")
if not user:
    print("✗ Test user not found. Please create testuser2 first.")
    exit(1)

user_id = user.id
print(f"Using test user: {user.username} (ID: {user_id})\n")

# Test 1: Save chat
print("Test 1: Saving chat...")
try:
    sources = [
        {"pdf": "test.pdf", "chunk": 1, "score": 0.95, "preview": "Test preview"}
    ]
    chat = save_chat(
        user_id,
        "What is diabetes?",
        "Diabetes is a chronic condition...",
        sources
    )
    print(f"✓ Chat saved with ID: {chat.id}")
except Exception as e:
    print(f"✗ Error saving chat: {e}")

# Test 2: Save another chat
print("\nTest 2: Saving another chat...")
try:
    sources = [
        {"pdf": "test2.pdf", "chunk": 2, "score": 0.87, "preview": "Another preview"}
    ]
    chat = save_chat(
        user_id,
        "What is hypertension?",
        "Hypertension is high blood pressure...",
        sources
    )
    print(f"✓ Second chat saved with ID: {chat.id}")
except Exception as e:
    print(f"✗ Error saving chat: {e}")

# Test 3: Load chat
print("\nTest 3: Loading chat...")
try:
    chats = load_chat(user_id)
    print(f"✓ Loaded {len(chats)} chat messages")
    for i, chat in enumerate(chats, 1):
        print(f"  Message {i}: {chat['question'][:50]}...")
except Exception as e:
    print(f"✗ Error loading chat: {e}")

# Test 4: Verify chat order (most recent first)
print("\nTest 4: Verifying chat order (most recent first)...")
try:
    chats = load_chat(user_id)
    if chats[0]["question"] == "What is hypertension?":
        print("✓ Chats are ordered correctly (most recent first)")
    else:
        print("✗ Chat order is incorrect")
except Exception as e:
    print(f"✗ Error verifying chat order: {e}")

# Test 5: Clear chat
print("\nTest 5: Clearing chat...")
try:
    result = clear_chat(user_id)
    if result:
        print("✓ Chat cleared successfully")
    else:
        print("✗ Chat clear failed")
except Exception as e:
    print(f"✗ Error clearing chat: {e}")

# Test 6: Verify chat is cleared
print("\nTest 6: Verifying chat is cleared...")
try:
    chats = load_chat(user_id)
    if len(chats) == 0:
        print("✓ Chat history is empty after clear")
    else:
        print(f"✗ Chat history still has {len(chats)} messages")
except Exception as e:
    print(f"✗ Error verifying clear: {e}")

# Test 7: Save chat without sources
print("\nTest 7: Saving chat without sources...")
try:
    chat = save_chat(
        user_id,
        "What is asthma?",
        "Asthma is a respiratory condition...",
        None
    )
    print(f"✓ Chat saved without sources, ID: {chat.id}")
except Exception as e:
    print(f"✗ Error saving chat without sources: {e}")

# Test 8: Load and verify sources are preserved
print("\nTest 8: Saving and loading with sources...")
try:
    sources = [
        {"pdf": "doc1.pdf", "chunk": 1, "score": 0.95, "preview": "Preview 1"},
        {"pdf": "doc2.pdf", "chunk": 2, "score": 0.88, "preview": "Preview 2"}
    ]
    chat = save_chat(
        user_id,
        "Test with sources",
        "Test answer",
        sources
    )
    chats = load_chat(user_id)
    if chats and chats[0]["sources"]:
        print(f"✓ Sources preserved: {len(chats[0]['sources'])} sources")
    else:
        print("✗ Sources not preserved")
except Exception as e:
    print(f"✗ Error with sources test: {e}")

# Cleanup
print("\nCleaning up test data...")
try:
    clear_chat(user_id)
    print("✓ Test data cleaned up")
except Exception as e:
    print(f"✗ Error cleaning up: {e}")

print("\n=== Chat History Tests Completed ===")
