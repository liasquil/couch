import re

from django.utils import timezone
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model; UserModel=get_user_model()
from django.http import Http404

from models import Reference, Message
import models


class MessageCreationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        
        preceding_message_id = kwargs.pop('preceding_message_id', None)
        answer_all = kwargs.pop('answer_all', None)
        if preceding_message_id:
            # Here we check permissions to reply to a preceding_message
            # and if positive, calculate some initial form data.
            initial = {}
            try:
                msg = Message.objects.get(pk=preceding_message_id)
                if not msg.sender == self.request.user:
                    # This means the user has neither sent nor received this message
                    # so he shouldn't be able to reply to it
                    ref = Reference.objects.get(message=msg, recipient=self.request.user)
            except (Message.DoesNotExist, Reference.DoesNotExist):
                raise Http404
            
            initial['preceding_message'] = msg.id

            if msg.subject.startswith('Re: '):
                initial['subject'] = 'Re[2]: '+msg.subject[4:]
            elif msg.subject.startswith('Re[') and ']' in msg.subject and msg.subject[3:msg.subject.find(']')].isdigit():
                # Old subject begins with sth like 'Re[48]: '.
                # Our new prefix will be almost the same, just with a number greater by 1:
                bracketpos = msg.subject.find(']')
                initial['subject'] = 'Re[{0}]: '.format(int(msg.subject[3:bracketpos])+1) +\
                    msg.subject[bracketpos+3:]  # Offset is to because of the space
            else:
                initial['subject'] = 'Re: '+msg.subject

            if 'recipients' not in kwargs:  # this condition allows to explicitly enforce another initial set of recipients
                recipients = []
                if msg.sender != self.request.user:
                    recipients.append(msg.sender)
                other_recipients = msg.recipients.exclude(pk__in=(self.request.user.id, msg.sender.id))
                if (answer_all==True or msg.sender == self.request.user) and other_recipients:
                    recipients += list(other_recipients)
                initial['recipients'] = ', '.join(r.username for r in recipients)
            initial.update(kwargs.get('initial', {}))
            kwargs['initial'] = initial
        
        super(MessageCreationForm, self).__init__(*args, **kwargs)
        
    subject = forms.CharField(max_length=150)
    preceding_message = forms.IntegerField(required=False, min_value=1, widget=forms.HiddenInput())
    recipients = forms.CharField(max_length=1000)   # has to be below preceding_message (validation!)
    content = forms.CharField(widget=forms.Textarea, max_length=40000)
    
    def clean_preceding_message(self):
        msg_id = self.cleaned_data.get('preceding_message')
        if msg_id == None:
            return None
        try:
            msg = Message.objects.get(pk=msg_id)
        except Message.DoesNotExist:
            raise forms.ValidationError("That message does not exist.")
        try:
            ref = Reference.objects.get(message=msg, recipient=self.request.user)
        except Reference.DoesNotExist:
            raise forms.ValidationError("This is no message for you.")
        return msg
    
    def clean_recipients(self):
        # all recipients are specified in one textfield, separated by
        # commas and possibly whitespaces. Make a clean list from that.
        proposed_recipients_raw = list(set(self.cleaned_data.get('recipients').split(',')))
        proposed_recipients = [r.strip() for r in proposed_recipients_raw]
        
        invalid_recipients = []
        recipients = []
        for i, r in enumerate(proposed_recipients):
            try:
                db_recipient = UserModel.objects.get(username=r)
                if db_recipient == self.request.user:
                    raise forms.ValidationError("You cannot send a message to yourself.")
                else:
                    recipients.append(db_recipient)
            except UserModel.DoesNotExist:
                invalid_recipients.append(r)
                
        if not invalid_recipients == []:
            raise forms.ValidationError("These recipients do not exist: "+str(invalid_recipients))
        
        preceding_message = self.cleaned_data.get('preceding_message')
        if preceding_message:
            if not preceding_message.involved_people_set & set(recipients):
                raise forms.ValidationError("If you are replying to a message, at least one of your addressees should have been involved in it.")
        
        # EXTEND this by some logic here to restrict to whom a message may be sent
        # i.e. the option to not receive messages at all
        return recipients
    
    def save(self):
        data = self.cleaned_data
        now = timezone.now()
        
        message = models.Message(
            sender = self.request.user,
            sent_at = now,
            subject = data['subject'],
            content = data['content'],
            preceding_message = data.get('preceding_message'),
        )
        message.save()
        
        for r in data['recipients']:
            reference = models.Reference(message=message, recipient=r, read_at=now)
            reference.save()
            
        return message
        
        
        
        
        