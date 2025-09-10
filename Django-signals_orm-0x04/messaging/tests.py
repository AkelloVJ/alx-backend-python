from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Message, MessageHistory, Notification, Conversation
import json


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@test.com')
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com')
    
    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, 'Test message')
        self.assertFalse(message.edited)
        self.assertFalse(message.read)
    
    def test_message_threading(self):
        parent = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Parent message'
        )
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply message',
            parent_message=parent
        )
        self.assertEqual(reply.parent_message, parent)
        self.assertIn(reply, parent.replies.all())
    
    def test_unread_messages_manager(self):
        # Create some messages
        Message.objects.create(sender=self.user1, receiver=self.user2, content='Message 1')
        Message.objects.create(sender=self.user1, receiver=self.user2, content='Message 2', read=True)
        Message.objects.create(sender=self.user2, receiver=self.user1, content='Message 3')
        
        # Test unread messages for user2
        unread_count = Message.unread.unread_count(self.user2)
        self.assertEqual(unread_count, 1)
        
        unread_messages = Message.unread.for_user(self.user2)
        self.assertEqual(unread_messages.count(), 1)


class SignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@test.com')
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com')
    
    def test_message_notification_creation(self):
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        
        # Check if notification was created
        notification = Notification.objects.filter(user=self.user2, message=message).first()
        self.assertIsNotNone(notification)
        self.assertFalse(notification.read)
    
    def test_message_edit_history(self):
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )
        
        # Edit the message
        message.content = 'Edited content'
        message.save()
        
        # Check if edit history was created
        history = MessageHistory.objects.filter(message=message).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, 'Original content')
        self.assertTrue(message.edited)
    
    def test_user_deletion_cleanup(self):
        # Create messages and notifications
        message1 = Message.objects.create(sender=self.user1, receiver=self.user2, content='Message 1')
        message2 = Message.objects.create(sender=self.user2, receiver=self.user1, content='Message 2')
        
        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        # Store user1 ID before deletion
        user1_id = self.user1.id
        
        # Delete user1
        self.user1.delete()
        
        # Check if related data was cleaned up
        self.assertFalse(Message.objects.filter(sender_id=user1_id).exists())
        self.assertFalse(Message.objects.filter(receiver_id=user1_id).exists())
        self.assertFalse(Notification.objects.filter(user_id=user1_id).exists())
        self.assertFalse(MessageHistory.objects.filter(edited_by_id=user1_id).exists())


class MessageAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@test.com', password='pass123')
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com', password='pass123')
        self.client = Client()
    
    def test_send_message(self):
        self.client.force_login(self.user1)
        data = {
            'receiver_id': self.user2.id,
            'content': 'Test message'
        }
        response = self.client.post('/api/messages/send/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if message was created
        message = Message.objects.filter(sender=self.user1, receiver=self.user2).first()
        self.assertIsNotNone(message)
        self.assertEqual(message.content, 'Test message')
    
    def test_edit_message(self):
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Original content'
        )
        
        self.client.force_login(self.user1)
        data = {'content': 'Edited content'}
        response = self.client.put(f'/api/messages/{message.id}/edit/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if message was updated
        message.refresh_from_db()
        self.assertEqual(message.content, 'Edited content')
        self.assertTrue(message.edited)
    
    def test_mark_message_read(self):
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        
        self.client.force_login(self.user2)
        response = self.client.post(f'/api/messages/{message.id}/read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if message was marked as read
        message.refresh_from_db()
        self.assertTrue(message.read)
    
    def test_unread_messages(self):
        # Create some messages
        Message.objects.create(sender=self.user1, receiver=self.user2, content='Message 1')
        Message.objects.create(sender=self.user1, receiver=self.user2, content='Message 2', read=True)
        
        self.client.force_login(self.user2)
        response = self.client.get('/api/messages/unread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)
        self.assertEqual(len(response.data['messages']), 1)
    
    def test_message_thread(self):
        # Create parent message
        parent = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Parent message'
        )
        
        # Create reply
        reply = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply message',
            parent_message=parent
        )
        
        self.client.force_login(self.user1)
        response = self.client.get(f'/api/messages/{parent.id}/thread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_delete_user_account(self):
        # Create some data
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Test')
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        self.client.force_login(self.user1)
        response = self.client.delete('/api/user/delete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if user and related data were deleted
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())
        self.assertFalse(Message.objects.filter(sender=self.user1).exists())


class CacheTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@test.com', password='pass123')
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com', password='pass123')
        self.client = Client()
        
        # Create conversation
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)
        
        # Create messages
        Message.objects.create(sender=self.user1, receiver=self.user2, content='Message 1')
        Message.objects.create(sender=self.user2, receiver=self.user1, content='Message 2')
    
    def test_conversation_messages_caching(self):
        self.client.force_login(self.user1)
        
        # First request
        response1 = self.client.get(f'/api/conversations/{self.conversation.id}/messages/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Second request (should be cached)
        response2 = self.client.get(f'/api/conversations/{self.conversation.id}/messages/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        
        # Both responses should be identical
        self.assertEqual(response1.data, response2.data)