#!/usr/bin/env python3
"""
Demo script to test the Django Signals and ORM Messaging App functionality.
"""

import os
import sys
import django
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
django.setup()

from messaging.models import Message, Notification, MessageHistory, Conversation


def create_test_users():
    """Create test users for demonstration."""
    print("Creating test users...")
    
    # Create users
    user1, created = User.objects.get_or_create(
        username='alice',
        defaults={'email': 'alice@example.com'}
    )
    user2, created = User.objects.get_or_create(
        username='bob',
        defaults={'email': 'bob@example.com'}
    )
    user3, created = User.objects.get_or_create(
        username='charlie',
        defaults={'email': 'charlie@example.com'}
    )
    
    print(f"✓ Users created: {user1.username}, {user2.username}, {user3.username}")
    return user1, user2, user3


def test_message_creation_and_notifications():
    """Test message creation and automatic notification generation."""
    print("\n" + "="*50)
    print("TESTING: Message Creation and Notifications")
    print("="*50)
    
    user1, user2, user3 = create_test_users()
    
    # Create a message
    print(f"\n{user1.username} sends a message to {user2.username}...")
    message = Message.objects.create(
        sender=user1,
        receiver=user2,
        content="Hello Bob! How are you doing today?"
    )
    print(f"✓ Message created: {message.content[:30]}...")
    
    # Check if notification was automatically created
    notification = Notification.objects.filter(user=user2, message=message).first()
    if notification:
        print(f"✓ Notification automatically created for {user2.username}")
        print(f"  - Notification ID: {notification.id}")
        print(f"  - Created at: {notification.created_at}")
        print(f"  - Read status: {notification.read}")
    else:
        print("✗ No notification found!")


def test_message_editing_and_history():
    """Test message editing and history tracking."""
    print("\n" + "="*50)
    print("TESTING: Message Editing and History")
    print("="*50)
    
    user1, user2, user3 = create_test_users()
    
    # Create a message
    message = Message.objects.create(
        sender=user1,
        receiver=user2,
        content="This is the original message content."
    )
    print(f"✓ Original message: {message.content}")
    
    # Edit the message
    print(f"\n{user1.username} edits the message...")
    original_content = message.content
    message.content = "This is the edited message content."
    message.save()
    
    print(f"✓ Edited message: {message.content}")
    print(f"✓ Message marked as edited: {message.edited}")
    
    # Check edit history
    history = MessageHistory.objects.filter(message=message).first()
    if history:
        print(f"✓ Edit history created:")
        print(f"  - Old content: {history.old_content}")
        print(f"  - Edited at: {history.edited_at}")
        print(f"  - Edited by: {history.edited_by.username}")
    else:
        print("✗ No edit history found!")


def test_threaded_conversations():
    """Test threaded conversations with replies."""
    print("\n" + "="*50)
    print("TESTING: Threaded Conversations")
    print("="*50)
    
    user1, user2, user3 = create_test_users()
    
    # Create parent message
    parent_message = Message.objects.create(
        sender=user1,
        receiver=user2,
        content="Let's discuss the project timeline."
    )
    print(f"✓ Parent message: {parent_message.content}")
    
    # Create replies
    reply1 = Message.objects.create(
        sender=user2,
        receiver=user1,
        content="I think we should aim for next month.",
        parent_message=parent_message
    )
    print(f"✓ Reply 1: {reply1.content}")
    
    reply2 = Message.objects.create(
        sender=user1,
        receiver=user2,
        content="That sounds reasonable. What about the budget?",
        parent_message=parent_message
    )
    print(f"✓ Reply 2: {reply2.content}")
    
    # Test thread retrieval
    thread_messages = [parent_message] + parent_message.get_all_replies()
    print(f"\n✓ Thread contains {len(thread_messages)} messages:")
    for i, msg in enumerate(thread_messages, 1):
        indent = "  " if msg.parent_message else ""
        print(f"  {i}. {indent}{msg.sender.username}: {msg.content}")


def test_custom_manager():
    """Test the custom UnreadMessagesManager."""
    print("\n" + "="*50)
    print("TESTING: Custom Unread Messages Manager")
    print("="*50)
    
    user1, user2, user3 = create_test_users()
    
    # Create messages with different read statuses
    Message.objects.create(sender=user1, receiver=user2, content="Unread message 1")
    Message.objects.create(sender=user1, receiver=user2, content="Unread message 2")
    Message.objects.create(sender=user1, receiver=user2, content="Read message", read=True)
    Message.objects.create(sender=user2, receiver=user1, content="Message to user1")
    
    # Test unread count
    unread_count = Message.unread.unread_count(user2)
    print(f"✓ Unread messages for {user2.username}: {unread_count}")
    
    # Test unread messages retrieval
    unread_messages = Message.unread.for_user(user2)
    print(f"✓ Unread messages for {user2.username}:")
    for msg in unread_messages:
        print(f"  - {msg.sender.username}: {msg.content}")
    
    # Test unread count for user1
    unread_count_user1 = Message.unread.unread_count(user1)
    print(f"✓ Unread messages for {user1.username}: {unread_count_user1}")


def test_conversation_management():
    """Test conversation creation and management."""
    print("\n" + "="*50)
    print("TESTING: Conversation Management")
    print("="*50)
    
    user1, user2, user3 = create_test_users()
    
    # Create conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(user1, user2)
    print(f"✓ Conversation created with participants: {[p.username for p in conversation.participants.all()]}")
    
    # Create messages in conversation
    Message.objects.create(sender=user1, receiver=user2, content="Message in conversation 1")
    Message.objects.create(sender=user2, receiver=user1, content="Message in conversation 2")
    
    # Test conversation methods
    messages = conversation.get_messages()
    print(f"✓ Conversation has {messages.count()} messages")
    
    unread_count = conversation.get_unread_count(user2)
    print(f"✓ Unread messages in conversation for {user2.username}: {unread_count}")


def test_user_deletion_cleanup():
    """Test user deletion and data cleanup."""
    print("\n" + "="*50)
    print("TESTING: User Deletion and Data Cleanup")
    print("="*50)
    
    user1, user2, user3 = create_test_users()
    
    # Create data associated with user1
    message1 = Message.objects.create(sender=user1, receiver=user2, content="Message from user1")
    message2 = Message.objects.create(sender=user2, receiver=user1, content="Message to user1")
    conversation = Conversation.objects.create()
    conversation.participants.add(user1, user2)
    
    print(f"✓ Created data for {user1.username}:")
    print(f"  - Messages sent: {Message.objects.filter(sender=user1).count()}")
    print(f"  - Messages received: {Message.objects.filter(receiver=user1).count()}")
    print(f"  - Notifications: {Notification.objects.filter(user=user1).count()}")
    
    # Store user1 ID for verification
    user1_id = user1.id
    
    # Delete user1
    print(f"\nDeleting {user1.username}...")
    user1.delete()
    
    # Verify cleanup
    print(f"✓ After deletion:")
    print(f"  - Messages sent by user1: {Message.objects.filter(sender_id=user1_id).count()}")
    print(f"  - Messages received by user1: {Message.objects.filter(receiver_id=user1_id).count()}")
    print(f"  - Notifications for user1: {Notification.objects.filter(user_id=user1_id).count()}")
    print(f"  - Message history edited by user1: {MessageHistory.objects.filter(edited_by_id=user1_id).count()}")


def main():
    """Run all demonstration tests."""
    print("🚀 Django Signals and ORM Messaging App Demo")
    print("=" * 60)
    
    try:
        # Run all tests
        test_message_creation_and_notifications()
        test_message_editing_and_history()
        test_threaded_conversations()
        test_custom_manager()
        test_conversation_management()
        test_user_deletion_cleanup()
        
        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
