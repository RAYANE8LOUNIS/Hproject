from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.utils import timezone
from .models import Message
from .forms import MessageForm


def _get_counts(user):
    """Helper to get sidebar badge counts."""
    user_teams = user.teams.all()
    return {
        'inbox_count': Message.objects.filter(
            team__in=user_teams, status='sent', is_read=False
        ).count(),
        'drafts_count': Message.objects.filter(
            sender=user, status='draft'
        ).count(),
    }


@login_required
def inbox(request):
    user_teams = request.user.teams.all()
    inbox_messages = Message.objects.filter(
        team__in=user_teams, status='sent',
    ).select_related('sender', 'team').order_by('-sent_at')

    context = {
        'messages_list': inbox_messages,
        'active_tab': 'inbox',
        **_get_counts(request.user),
    }
    return render(request, 'messaging/inbox.html', context)


@login_required
def sent(request):
    sent_messages = Message.objects.filter(
        sender=request.user, status='sent',
    ).select_related('team').order_by('-sent_at')

    context = {
        'messages_list': sent_messages,
        'active_tab': 'sent',
        **_get_counts(request.user),
    }
    return render(request, 'messaging/sent.html', context)


@login_required
def drafts(request):
    draft_messages = Message.objects.filter(
        sender=request.user, status='draft',
    ).select_related('team').order_by('-updated_at')

    context = {
        'messages_list': draft_messages,
        'active_tab': 'drafts',
        **_get_counts(request.user),
    }
    return render(request, 'messaging/drafts.html', context)


@login_required
def compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user

            if 'send' in request.POST:
                message.status = 'sent'
                message.sent_at = timezone.now()
                message.save()
                django_messages.success(request, 'Message sent successfully.')
                return redirect('messaging:send_success')
            elif 'save_draft' in request.POST:
                message.status = 'draft'
                message.save()
                django_messages.success(request, 'Message saved as draft.')
                return redirect('messaging:drafts')
    else:
        form = MessageForm()

    context = {
        'form': form,
        'active_tab': 'compose',
        **_get_counts(request.user),
    }
    return render(request, 'messaging/compose.html', context)


@login_required
def send_success(request):
    context = {
        'active_tab': 'compose',
        **_get_counts(request.user),
    }
    return render(request, 'messaging/send_success.html', context)


@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)

    user_teams = request.user.teams.all()
    is_sender = message.sender == request.user
    is_recipient = message.team in user_teams

    if not is_sender and not is_recipient:
        django_messages.error(request, 'You do not have permission to view this message.')
        return redirect('messaging:inbox')

    if is_recipient and not message.is_read:
        message.is_read = True
        message.save()

    context = {
        'message': message,
        'is_sender': is_sender,
        'is_recipient': is_recipient,
        'active_tab': 'inbox' if is_recipient else 'sent',
        **_get_counts(request.user),
    }
    return render(request, 'messaging/message_detail.html', context)


@login_required
def edit_draft(request, pk):
    message = get_object_or_404(Message, pk=pk, sender=request.user, status='draft')

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            message = form.save(commit=False)

            if 'send' in request.POST:
                message.status = 'sent'
                message.sent_at = timezone.now()
                message.save()
                django_messages.success(request, 'Message sent successfully.')
                return redirect('messaging:send_success')
            elif 'save_draft' in request.POST:
                message.save()
                django_messages.success(request, 'Draft updated.')
                return redirect('messaging:drafts')
    else:
        form = MessageForm(instance=message)

    context = {
        'form': form,
        'message': message,
        'is_edit': True,
        'active_tab': 'drafts',
        **_get_counts(request.user),
    }
    return render(request, 'messaging/compose.html', context)


@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk, sender=request.user)

    if request.method == 'POST':
        was_draft = message.is_draft
        message.delete()
        django_messages.success(request, 'Message deleted.')
        return redirect('messaging:drafts' if was_draft else 'messaging:sent')

    context = {
        'message': message,
        'active_tab': 'drafts' if message.is_draft else 'sent',
        **_get_counts(request.user),
    }
    return render(request, 'messaging/delete_confirm.html', context)
