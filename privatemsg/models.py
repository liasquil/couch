from django.utils import timezone
from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages')
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Reference')
    sent_at = models.DateTimeField()
    preceding_message = models.ForeignKey('self', null=True, blank=True)
    
    subject = models.CharField(max_length=150)
    content = models.TextField(max_length=40000)
    deleted_by_sender = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
        return super(Message, self).save(*args, **kwargs)
    
    @property
    def involved_people_set(self):
        return set(self.recipients.all())|set([self.sender])
    
    def get_preceding_messages(self, for_user):
        prmsg = self.preceding_message
        if ((prmsg == None) or                                 # normal exit condition
                for_user not in prmsg.involved_people_set or   # aborts when it reaches foreign msg
                for_user not in self.involved_people_set):     # cannot start at foreign msg (not covered by condition above!)
            return Message.objects.none()
        return prmsg.get_preceding_messages(for_user=for_user)|Message.objects.filter(pk=prmsg.id)
        # Since the preceding msg is older, it has a lower id. So
        # the resulting set will be chronologically ordered with the
        # youngest message last.
    
    def get_subsequent_messages(self, for_user):
        """ Recursively get the largest continuous tree of messages which are all
        on some level replies to the root message (self) and which all
        involve the for_user either as sender or recipient.
        It is not important whether the for_user was involved in the
        root message, though. So you can still get a non-empty tree
        for a root message even if for_user was neither its sender nor 
        recipient.
        """

        # Since we cannot query the ManyToManyField 'recipients' using
        # __contains, we have to take a detour over the references.
        # These are the refs for all msgs which the user *received*
        # and which are immediate replies to 'self'.
        # EXTEND this maybe to take deletion into account.
        refs = Reference.objects.filter(message__preceding_message=self, recipient=for_user)
        ids_of_received_messages = [r.message.id for r in refs]
        directly_subsequent_messages = Message.objects.filter(
            pk__in=ids_of_received_messages
        ) | Message.objects.filter(preceding_message=self, sender=for_user)

        # The exit condition is implied by the possibility of the Queryset
        # being empty, thus not being  iterated over
        indirectly_subsequent_messages = Message.objects.none()
        for m in directly_subsequent_messages:
            indirectly_subsequent_messages = indirectly_subsequent_messages|m.get_subsequent_messages(for_user=for_user)
        return directly_subsequent_messages|indirectly_subsequent_messages
        
    
    def __str__(self):
        return self.subject
    
class Reference(models.Model):
    message = models.ForeignKey(Message)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    read_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)