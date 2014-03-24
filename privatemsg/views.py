from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404

import models, forms
from models import Message, Reference
# Create your views here.


@login_required
def new_message(request, preceding_message_id=None, answer_all=False):
    
    if request.method == 'POST':
        form = forms.MessageCreationForm(request.POST, request=request)
        if form.is_valid():
            message = form.save()
            return redirect('privatemsg:outbox')
                
    else:
        
        form = forms.MessageCreationForm(
            request=request, 
            preceding_message_id=preceding_message_id,
            answer_all=answer_all
        )
        
    return render(request, 'privatemsg/new_message.html', {
        'form':form,
    })

@login_required
def inbox(request):
    references = Reference.objects.filter(recipient=request.user, deleted=False).order_by('-id')
    for r in references:
        r.message.preceding_messages = r.message.get_preceding_messages(for_user=request.user).order_by('-id')
    return render(request, 'privatemsg/inbox.html', {
        'references':references,
    })

@login_required
def outbox(request):
    sent_messages = models.Message.objects.filter(sender=request.user, deleted_by_sender=False).order_by('-id')
    for m in sent_messages:
        m.preceding_messages = m.get_preceding_messages(for_user=request.user).order_by('-id')
    return render(request, 'privatemsg/outbox.html', {
        'sent_messages':sent_messages,
    })

@login_required
def delete(request, message_id):
    message = get_object_or_404(Message,pk=message_id)
    if message.sender == request.user:
        message.deleted_by_sender = True
        message.save()
        return redirect('privatemsg:outbox')
    else:
        try:
            r = Reference.objects.get(message=message, recipient=request.user)
            r.deleted = True
            r.save()
            return redirect('privatemsg:inbox')
        except Reference.DoesNotExist:
            raise Http404