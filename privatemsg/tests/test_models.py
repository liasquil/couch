from django.test import TestCase

from privatemsg.models import Message, Reference
from accounts.models import CustomUser
from accounts.tests.utils import (
    create_user,
)

class MessageTests(TestCase):
    
    
    def setUp(self):
        pass
    
    def send_message(self, sender, preceding_message, subject, content, recipients):
        msg = Message.objects.create(
            sender=sender,
            preceding_message=preceding_message,
            subject=subject,
            content=content
        )
        for r in recipients:
            Reference.objects.create(message=msg, recipient=r)
        return msg
    
    
    def test_sender_delete(self):
        user = CustomUser.objects.create(username='user', email='user@example.com')
        partner1 = CustomUser.objects.create(username='partner1', email='p1@example.com')
        partner2 = CustomUser.objects.create(username='partner2', email='p2@example.com')
        msg = self.send_message(user, None, 'Delmsg test', '----', (partner1, partner2))
        references = msg.references.all()
        self.assertEqual(len(references), 2)  # just to make sure I set up the test correctly
        msg.sender_delete()
        try:
            updated_msg = Message.objects.get(pk=msg.id)
        except Message.DoesNotExist:
            self.fail("Call to remove() deleted the message's database entry.")
        self.assertEqual(msg.deleted_by_sender, True)
        updated_references = updated_msg.references.all()
        self.assertEqual(set(references), set(updated_references))
    
    def test_get_thread_returns_full_thread_if_user_is_involved_in_every_message(self):
        pass
    
    def test_get_thread_cuts_at_foreign_message(self):
        pass
    
    def test_get_preceding_messages_returns_full_linear_series(self):
        # 'linear' means that branches are not considered
        user = CustomUser.objects.create(username='user', email='user@example.com')
        partner1 = CustomUser.objects.create(username='partner1', email='p1@example.com')
        partner2 = CustomUser.objects.create(username='partner2', email='p2@example.com')
        m0 = self.send_message(user, None, 'Subject0', '----', (partner1, partner2))
        m1 = self.send_message(partner1, m0, 'Subject1', '----', (user, partner2))
        branch0 = self.send_message(partner2, m0, 'Branch0', 'Should be ignored', (user, partner1))
        branch1 = self.send_message(user, branch0, 'Reply to Branch0', 'Also to ignore', (partner2,))
        m2 = self.send_message(partner2, m1, 'Subject2', 'Without partner 1, should be contained', (user,))
        m3 = self.send_message(user, m2, 'Subject3', '----', (partner1, partner2))
        m4 = self.send_message(partner1, m3, 'Subject4', 'Now without partner2, should be contained', (user,))
        m5 = self.send_message(user, m4, 'Subject5', '----', (partner1, partner2))
        m6 = self.send_message(user, m5, 'Subject6', 'Reply to own message, should be contained', (partner1,))
        m7 = self.send_message(partner1, m6, 'Subject7', '----', (user, partner2))
        m8 = self.send_message(user, m7, 'Subject8', '----', (partner1, partner2))
        m9 = self.send_message(partner2, m8, 'Subject9', 'Subsequent, so it should be ignored', (user, partner1))
        
        messages = [m0,m1,m2,m3,m4,m5,m6,m7,m8,m9]
        
        calculated_series = [m.get_preceding_messages(for_user=user) for m in messages]
        for i,s in enumerate(calculated_series):
            self.assertEqual(list(s), messages[:i])
        
    
    def test_get_preceding_messages_cuts_at_foreign_message(self):
        user = CustomUser.objects.create(username='user', email='user@example.com')
        partner1 = CustomUser.objects.create(username='partner1', email='p1@example.com')
        partner2 = CustomUser.objects.create(username='partner2', email='p2@example.com')
        
        m0 = self.send_message(user, None, 'Subject1', '----', (partner1, partner2))
        m1 = self.send_message(partner1, m0, 'Subject2', 'User not involved', (partner2,))
        m2 = self.send_message(partner2, m1, 'Subject3', 'Now again to everyone', (user, partner1))
        m3 = self.send_message(user, m2, 'Subject3', '----', (partner1, partner2))
        m4 = self.send_message(partner1, m3, 'Subject4', '----', (user,))
        m5 = self.send_message(partner1, m4, 'Subject5', 'Not involved again', (partner2,))
        
        messages = [m0,m1,m2,m3,m4,m5]
        calculated_series = [m.get_preceding_messages(for_user=user) for m in messages]
        self.assertEqual(list(calculated_series[0]), [])
        self.assertEqual(list(calculated_series[1]), [])
        self.assertEqual(list(calculated_series[2]), [])
        self.assertEqual(list(calculated_series[3]), [m2])
        self.assertEqual(list(calculated_series[4]), [m2,m3])
        self.assertEqual(list(calculated_series[5]), [])
        
    
    def test_get_subsequent_messages_returns_full_tree(self):
        user = CustomUser.objects.create(username='user', email='user@example.com')
        partner1 = CustomUser.objects.create(username='partner1', email='p1@example.com')
        partner2 = CustomUser.objects.create(username='partner2', email='p2@example.com')
        
        m0 = self.send_message(user, None, 'Subject0', '----', (partner1, partner2))
        
        m1 = self.send_message(partner1, m0, 'Subject1', 'branch0', (user, partner2))
        m2 = self.send_message(partner2, m1, 'Subject2', '----', (user, partner1))
        
        m3 = self.send_message(partner2, m0, 'Subject3', 'branch1', (user,))
        m4 = self.send_message(user, m3, 'Subject3', '----', (partner1, partner2))
        m5 = self.send_message(partner1, m4, 'Subject4', '----', (user,))
        m6 = self.send_message(partner1, m5, 'Subject5', 'Reply to own msg', (user, partner2))
        
        m7 = self.send_message(user, m4, 'Subject7', 'branch1-0', (partner2,))
        m8 = self.send_message(partner1, m4, 'Subject8', 'branch1-1', (user, partner2))
        m9 = self.send_message(user, m8, 'Subject9', '----', (partner2,))
        
        messages = [m0,m1,m2,m3,m4,m5,m6,m7,m8,m9]
        calculated_series = [m.get_subsequent_messages(for_user=user) for m in messages]
        # The subseq. msgs are ordered as trees, not linear, so compare sets here
        self.assertEqual(set(calculated_series[0]), set(messages[1:]))
        self.assertEqual(set(calculated_series[1]), set([m2]))
        self.assertEqual(set(calculated_series[2]), set([]))
        self.assertEqual(set(calculated_series[3]), set(messages[4:]))
        self.assertEqual(set(calculated_series[4]), set(messages[5:]))
        self.assertEqual(set(calculated_series[5]), set([m6]))
        self.assertEqual(set(calculated_series[6]), set([]))
        self.assertEqual(set(calculated_series[7]), set([]))
        self.assertEqual(set(calculated_series[8]), set([m9]))
        self.assertEqual(set(calculated_series[9]), set([]))
        
    
    def test_get_subsequent_messages_cuts_at_foreign_message(self):
        user = CustomUser.objects.create(username='user', email='user@example.com')
        partner1 = CustomUser.objects.create(username='partner1', email='p1@example.com')
        partner2 = CustomUser.objects.create(username='partner2', email='p2@example.com')
        
        m0 = self.send_message(user, None, 'Subject0', '----', (partner1, partner2))
        
        m1 = self.send_message(partner1, m0, 'Subject1', 'branch0', (user, partner2))
        m2 = self.send_message(partner2, m1, 'Subject2', '----', (user, partner1))
        m3 = self.send_message(partner2, m2, 'Subject3', 'foreign-->ignore', (partner1,))
        # This one should be ignored when starting at m0 or so, but included for m3
        m4 = self.send_message(partner1, m3, 'Subject4', 'after foreign', (user, partner2))
        
        m5 = self.send_message(partner2, m0, 'Subject5', 'branch1', (user,))
        m6 = self.send_message(user, m5, 'Subject6', 'reply only to uninvolved person--should be no problem', (partner1,))
        m7 = self.send_message(partner1, m6, 'Subject7', '----', (user, partner2))
        
        m8 = self.send_message(user, m5, 'Subject8', 'branch1-0', (partner2,))
        m9 = self.send_message(partner2, m8, 'Subject9', '----', (user,partner1))
        m10 = self.send_message(partner1, m9, 'Subject10', 'foreign-->ignore', (partner2,))
        
        m11 = self.send_message(user, m5, 'Subject11', 'branch1-1', (partner1,partner2))
        
        messages = [m0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11]
        calculated_series = [m.get_subsequent_messages(for_user=user) for m in messages]
        # The subseq. msgs are ordered as trees, not linear, so compare sets here
        self.assertEqual(set(calculated_series[0]), set([messages[i] for i in (1,2,5,6,7,8,9,11)]))  # 1,2,5,6,7,8,9,11
        self.assertEqual(set(calculated_series[1]), set([messages[2]]))
        self.assertEqual(set(calculated_series[2]), set([]))
        self.assertEqual(set(calculated_series[3]), set([messages[4]]))
        self.assertEqual(set(calculated_series[4]), set([]))
        self.assertEqual(set(calculated_series[5]), set([messages[i] for i in (6,7,8,9,11)]))
        self.assertEqual(set(calculated_series[6]), set([messages[7]]))
        self.assertEqual(set(calculated_series[7]), set([]))
        self.assertEqual(set(calculated_series[8]), set([messages[9]]))
        self.assertEqual(set(calculated_series[9]), set([]))
        self.assertEqual(set(calculated_series[10]), set([]))
        self.assertEqual(set(calculated_series[11]), set([]))
    
    def test_get_preceding_messages_cuts_at_sender_deleted_message_for_sender_and_cuts_not_for_recipient(self):
        user = create_user('user', 'user@example.com')
        partner1 = create_user('partner1', 'p1@example.com')
        partner2 = create_user('partner2', 'p2@example.com')
        
        m0 = self.send_message(user, None, 'Subject0', '----', (partner1, partner2))
        m1 = self.send_message(partner1, m0, 'Subject1', '----', (user, partner2))
        m2 = self.send_message(user, m1, 'Subject2', '----', (partner1, partner2))
        m3 = self.send_message(partner2, m0, 'Subject3', '----', (user, partner1))
        m2.sender_delete()
        messages = [m0,m1,m2,m3]
        
        series0 = m3.get_preceding_messages(for_user=user)
        series1 = m3.get_preceding_messages(for_user=partner1)
        series2 = m3.get_preceding_messages(for_user=partner2)
        
        self.assertEqual(set(series0), {m3}, "get_preceding_messages() for sender did not abort at message he deleted.")
        self.assertEqual(set(series1), set(messages), "get_preceding_messages() for recipient aborted at only sender-deleted message")
        self.assertEqual(set(series2), set(messages), "get_preceding_messages() for recipient aborted at only sender-deleted message")