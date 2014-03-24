from django.test import TestCase
from django.test.client import RequestFactory
from django import forms
from django.http import Http404

from accounts.models import CustomUser
from privatemsg.forms import MessageCreationForm
from privatemsg.models import Message, Reference



class MessageCreationFormTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('privatemsg:new')
        self.request.user = CustomUser.objects.create(
            username='request_user', 
            email='requser@example.com'
        )
        self.message_by_request_user = Message.objects.create(
            sender=self.request.user,
            subject='preceding',
            content='message'
        )
        self.other_sender = CustomUser.objects.create(
            username='other_sender',
            email='os@example.com',
        )
        self.message_by_other_sender = Message.objects.create(
            sender=self.other_sender,
            subject='preceding',
            content='message'
        )
    
    def test_clean_recipients_complains_if_recipient_does_not_exist(self):
        existing_user = CustomUser.objects.create(
            username='existent_user',
            email='email@example.com'
        )
        form = MessageCreationForm(request=self.request)
        form.cleaned_data = {}
        # despite one name existing, this should raise an error because of the other one
        form.cleaned_data['recipients'] = 'existent_user, nonexistent_user'
        self.assertRaises(forms.ValidationError, form.clean_recipients)
        
    def test_fetches_exact_userset_from_input(self):
        user1 = CustomUser.objects.create(username='u1', email='e1@example.com')
        user2 = CustomUser.objects.create(username='u2', email='e2@example.com')
        user3 = CustomUser.objects.create(username='u3', email='e3@example.com')
        user4 = CustomUser.objects.create(username='u4', email='e4@example.com')
        form = MessageCreationForm(request=self.request)
        form.cleaned_data = {}
        form.cleaned_data['recipients'] = 'u1, u4, u2'
        self.assertEqual(set([user1,user2,user4]), set(form.clean_recipients()))
        
    def test_relates_to_correct_preceding_message(self):
        preceding_msg = self.message_by_request_user
        form = MessageCreationForm(
            request=self.request,
            preceding_message_id=preceding_msg.id,
            answer_all=False
        )
        self.assertEqual(form.initial['preceding_message'], preceding_msg.id)
        
    def test_complains_when_replying_to_foreign_message(self):
        preceding_msg = self.message_by_other_sender
        recipient = CustomUser.objects.create(username='recipient', email='rec@example.com')
        reference = Reference.objects.create(message=preceding_msg, recipient=recipient)
        with self.assertRaises(Http404, msg="Did not complain when replying to msg one has neither sent nor received."):
            form = MessageCreationForm(
                request=self.request,  # has another user
                preceding_message_id=preceding_msg.id,
                answer_all=False
            )
    
    def test_can_reply_to_own_message_and_is_not_initial_recipient(self):
        preceding_msg = self.message_by_request_user
        recipient = CustomUser.objects.create(username='recipient', email='rec@example.com')
        reference = Reference.objects.create(message=preceding_msg, recipient=recipient)
        form = MessageCreationForm(
            request=self.request, 
            preceding_message_id=preceding_msg.id
        )
        self.assertNotIn(self.request.user.username, form.initial['recipients'])
        form.cleaned_data={'recipients':recipient.username}
        self.assertTrue(form.clean_recipients())
        
    def test_user_is_not_initial_recipient_when_replying_to_somebody_elses_message(self):
        preceding_msg = self.message_by_other_sender
        Reference.objects.create(message=preceding_msg, recipient=self.request.user)
        form = MessageCreationForm(
            request=self.request,
            preceding_message_id=preceding_msg.id,
            answer_all=True
        )
        self.assertNotIn(self.request.user.username, form.initial['recipients'])
        form.cleaned_data={'recipients':self.other_sender.username}
        self.assertTrue(form.clean_recipients())
        
    def test_only_sender_is_initial_recipient_if_answer_all_is_false(self):
        other_recipient = CustomUser.objects.create(
            username='other recipient',
            email='or@example.com'
        )
        preceding_msg = self.message_by_other_sender
        Reference.objects.create(message=preceding_msg, recipient=self.request.user)
        Reference.objects.create(message=preceding_msg, recipient=other_recipient)
        form = MessageCreationForm(
            request=self.request,
            preceding_message_id=preceding_msg.id,
            answer_all=False
        )
        self.assertEqual(form.initial['recipients'], self.other_sender.username)
        
    def test_fetches_subject_from_preceding_message(self):
        #preceding_msg = Message.objects.create(subject='test subj')
        preceding_msg = self.message_by_request_user
        form = MessageCreationForm(
            request=self.request,
            preceding_message_id=preceding_msg.id,
            answer_all=False
        )
        # [-9:] is to cut prefixes like 'Re: '. The 9 is just len('preceding').
        self.assertEqual(form.initial['subject'][-9:], 'preceding')
        
    def test_saves_preceding_message(self):
        preceding_msg = self.message_by_other_sender
        reference = Reference.objects.create(recipient=self.request.user, message=preceding_msg)
        form = MessageCreationForm(
            request=self.request,
            data = {
                'subject': 'test',
                'recipients':self.other_sender.username,
                'content': 'testest',
                'preceding_message': preceding_msg.id
            }
        )
        self.assertTrue(form.is_valid())
        msg = form.save()
        self.assertEqual(msg.preceding_message, preceding_msg)
        
    