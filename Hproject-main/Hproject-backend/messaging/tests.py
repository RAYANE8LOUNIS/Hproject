from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from organisation.models import Team, Department
from .models import Message


class MessageModelTest(TestCase):
    """Tests for the Message model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', email='test@sky.com'
        )
        self.dept = Department.objects.create(name='Engineering')
        self.team = Team.objects.create(
            name='Frontend Development',
            department=self.dept,
            status='active',
        )

    def test_create_draft_message(self):
        """Test creating a draft message."""
        msg = Message.objects.create(
            sender=self.user,
            team=self.team,
            subject='Test Subject',
            body='Test body content.',
            status='draft',
        )
        self.assertEqual(msg.status, 'draft')
        self.assertTrue(msg.is_draft)
        self.assertFalse(msg.is_sent)
        self.assertIsNone(msg.sent_at)
        self.assertFalse(msg.is_read)

    def test_create_sent_message(self):
        """Test creating a sent message with timestamp."""
        now = timezone.now()
        msg = Message.objects.create(
            sender=self.user,
            team=self.team,
            subject='Sent Message',
            body='This has been sent.',
            status='sent',
            sent_at=now,
        )
        self.assertEqual(msg.status, 'sent')
        self.assertTrue(msg.is_sent)
        self.assertFalse(msg.is_draft)
        self.assertEqual(msg.sent_at, now)

    def test_message_str(self):
        """Test string representation of a message."""
        msg = Message.objects.create(
            sender=self.user,
            team=self.team,
            subject='Hello Team',
            body='Body.',
        )
        self.assertIn('testuser', str(msg))
        self.assertIn('Frontend Development', str(msg))
        self.assertIn('Hello Team', str(msg))

    def test_message_ordering(self):
        """Test that messages are ordered newest first."""
        msg1 = Message.objects.create(
            sender=self.user, team=self.team,
            subject='First', body='First message.',
        )
        msg2 = Message.objects.create(
            sender=self.user, team=self.team,
            subject='Second', body='Second message.',
        )
        messages = Message.objects.all()
        self.assertEqual(messages[0], msg2)
        self.assertEqual(messages[1], msg1)

    def test_cascade_delete_user(self):
        """Test that deleting a user deletes their messages."""
        Message.objects.create(
            sender=self.user, team=self.team,
            subject='Will be deleted', body='Gone.',
        )
        self.assertEqual(Message.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Message.objects.count(), 0)

    def test_cascade_delete_team(self):
        """Test that deleting a team deletes messages to it."""
        Message.objects.create(
            sender=self.user, team=self.team,
            subject='Will be deleted', body='Gone.',
        )
        self.assertEqual(Message.objects.count(), 1)
        self.team.delete()
        self.assertEqual(Message.objects.count(), 0)


class MessageViewTest(TestCase):
    """Tests for messaging views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='sarah', password='testpass123',
            first_name='Sarah', last_name='Johnson',
            email='sarah@sky.com',
        )
        self.other_user = User.objects.create_user(
            username='john', password='testpass123',
            first_name='John', last_name='Anderson',
        )
        self.dept = Department.objects.create(name='Engineering')
        self.team = Team.objects.create(
            name='Frontend Development',
            department=self.dept,
            status='active',
        )
        # Add sarah to the team so she can receive messages
        self.team.members.add(self.user)

    # ─── Authentication ─────────────────────────

    def test_inbox_requires_login(self):
        """Test that inbox redirects unauthenticated users."""
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_compose_requires_login(self):
        """Test that compose redirects unauthenticated users."""
        response = self.client.get(reverse('messaging:compose'))
        self.assertEqual(response.status_code, 302)

    # ─── Inbox ───────────────────────────────────

    def test_inbox_renders(self):
        """Test inbox page loads successfully."""
        self.client.login(username='sarah', password='testpass123')
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Teams')

    def test_inbox_shows_messages_for_user_teams(self):
        """Test that inbox shows messages addressed to user's teams."""
        self.client.login(username='sarah', password='testpass123')
        Message.objects.create(
            sender=self.other_user, team=self.team,
            subject='Important Update', body='Read this.',
            status='sent', sent_at=timezone.now(),
        )
        response = self.client.get(reverse('messaging:inbox'))
        self.assertContains(response, 'Important Update')

    def test_inbox_hides_draft_messages(self):
        """Test that drafts don't appear in inbox."""
        self.client.login(username='sarah', password='testpass123')
        Message.objects.create(
            sender=self.other_user, team=self.team,
            subject='Draft Message', body='Not sent yet.',
            status='draft',
        )
        response = self.client.get(reverse('messaging:inbox'))
        self.assertNotContains(response, 'Draft Message')

    def test_inbox_unread_count(self):
        """Test that unread count is passed to template."""
        self.client.login(username='sarah', password='testpass123')
        Message.objects.create(
            sender=self.other_user, team=self.team,
            subject='Unread', body='New.', status='sent',
            sent_at=timezone.now(), is_read=False,
        )
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.context['inbox_count'], 1)

    # ─── Compose ─────────────────────────────────

    def test_compose_renders(self):
        """Test compose page loads with form."""
        self.client.login(username='sarah', password='testpass123')
        response = self.client.get(reverse('messaging:compose'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select Team')
        self.assertContains(response, 'Subject')

    def test_compose_send_message(self):
        """Test sending a message via compose form."""
        self.client.login(username='sarah', password='testpass123')
        response = self.client.post(reverse('messaging:compose'), {
            'team': self.team.pk,
            'subject': 'Hello Frontend Team',
            'body': 'This is a test message.',
            'send': 'true',
        })
        self.assertRedirects(response, reverse('messaging:send_success'))
        msg = Message.objects.get(subject='Hello Frontend Team')
        self.assertEqual(msg.sender, self.user)
        self.assertEqual(msg.status, 'sent')
        self.assertIsNotNone(msg.sent_at)

    def test_compose_save_draft(self):
        """Test saving a message as draft."""
        self.client.login(username='sarah', password='testpass123')
        response = self.client.post(reverse('messaging:compose'), {
            'team': self.team.pk,
            'subject': 'Draft Subject',
            'body': 'Draft body.',
            'save_draft': 'true',
        })
        self.assertRedirects(response, reverse('messaging:drafts'))
        msg = Message.objects.get(subject='Draft Subject')
        self.assertEqual(msg.status, 'draft')
        self.assertIsNone(msg.sent_at)

    def test_compose_validation_error(self):
        """Test that form validates required fields."""
        self.client.login(username='sarah', password='testpass123')
        response = self.client.post(reverse('messaging:compose'), {
            'team': '',
            'subject': '',
            'body': '',
            'send': 'true',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.count(), 0)

    # ─── Sent ────────────────────────────────────

    def test_sent_renders(self):
        """Test sent page loads."""
        self.client.login(username='sarah', password='testpass123')
        response = self.client.get(reverse('messaging:sent'))
        self.assertEqual(response.status_code, 200)

    def test_sent_shows_only_user_messages(self):
        """Test sent only shows messages from the logged-in user."""
        self.client.login(username='sarah', password='testpass123')
        Message.objects.create(
            sender=self.user, team=self.team,
            subject='My Sent Message', body='Sent.',
            status='sent', sent_at=timezone.now(),
        )
        Message.objects.create(
            sender=self.other_user, team=self.team,
            subject='Other Sent Message', body='Not mine.',
            status='sent', sent_at=timezone.now(),
        )
        response = self.client.get(reverse('messaging:sent'))
        self.assertContains(response, 'My Sent Message')
        self.assertNotContains(response, 'Other Sent Message')

    # ─── Drafts ──────────────────────────────────

    def test_drafts_renders(self):
        """Test drafts page loads."""
        self.client.login(username='sarah', password='testpass123')
        response = self.client.get(reverse('messaging:drafts'))
        self.assertEqual(response.status_code, 200)

    def test_drafts_shows_only_user_drafts(self):
        """Test drafts only shows current user's drafts."""
        self.client.login(username='sarah', password='testpass123')
        Message.objects.create(
            sender=self.user, team=self.team,
            subject='My Draft', body='WIP.', status='draft',
        )
        Message.objects.create(
            sender=self.other_user, team=self.team,
            subject='Other Draft', body='Not mine.', status='draft',
        )
        response = self.client.get(reverse('messaging:drafts'))
        self.assertContains(response, 'My Draft')
        self.assertNotContains(response, 'Other Draft')

    # ─── Message Detail ──────────────────────────

    def test_detail_as_sender(self):
        """Test viewing a message as the sender."""
        self.client.login(username='sarah', password='testpass123')
        msg = Message.objects.create(
            sender=self.user, team=self.team,
            subject='View This', body='Detail test.',
            status='sent', sent_at=timezone.now(),
        )
        response = self.client.get(reverse('messaging:message_detail', args=[msg.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View This')
        self.assertContains(response, 'Detail test.')

    def test_detail_marks_as_read(self):
        """Test that viewing a message as recipient marks it read."""
        msg = Message.objects.create(
            sender=self.other_user, team=self.team,
            subject='Unread Msg', body='Should become read.',
            status='sent', sent_at=timezone.now(), is_read=False,
        )
        self.client.login(username='sarah', password='testpass123')
        self.client.get(reverse('messaging:message_detail', args=[msg.pk]))
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)

    def test_detail_permission_denied(self):
        """Test that non-sender, non-recipient cannot view message."""
        other_team = Team.objects.create(
            name='Other Team', department=self.dept, status='active',
        )
        msg = Message.objects.create(
            sender=self.other_user, team=other_team,
            subject='Private', body='Cannot see.',
            status='sent', sent_at=timezone.now(),
        )
        self.client.login(username='sarah', password='testpass123')
        response = self.client.get(reverse('messaging:message_detail', args=[msg.pk]))
        self.assertRedirects(response, reverse('messaging:inbox'))

    # ─── Edit Draft ──────────────────────────────

    def test_edit_draft(self):
        """Test editing and re-saving a draft."""
        self.client.login(username='sarah', password='testpass123')
        msg = Message.objects.create(
            sender=self.user, team=self.team,
            subject='Old Subject', body='Old body.', status='draft',
        )
        response = self.client.post(reverse('messaging:edit_draft', args=[msg.pk]), {
            'team': self.team.pk,
            'subject': 'Updated Subject',
            'body': 'Updated body.',
            'save_draft': 'true',
        })
        self.assertRedirects(response, reverse('messaging:drafts'))
        msg.refresh_from_db()
        self.assertEqual(msg.subject, 'Updated Subject')
        self.assertEqual(msg.status, 'draft')

    def test_edit_draft_then_send(self):
        """Test editing a draft and sending it."""
        self.client.login(username='sarah', password='testpass123')
        msg = Message.objects.create(
            sender=self.user, team=self.team,
            subject='Draft to Send', body='Will be sent.', status='draft',
        )
        response = self.client.post(reverse('messaging:edit_draft', args=[msg.pk]), {
            'team': self.team.pk,
            'subject': 'Draft to Send',
            'body': 'Now sent.',
            'send': 'true',
        })
        self.assertRedirects(response, reverse('messaging:send_success'))
        msg.refresh_from_db()
        self.assertEqual(msg.status, 'sent')
        self.assertIsNotNone(msg.sent_at)

    def test_cannot_edit_other_users_draft(self):
        """Test that users cannot edit someone else's draft."""
        self.client.login(username='sarah', password='testpass123')
        msg = Message.objects.create(
            sender=self.other_user, team=self.team,
            subject='Not Mine', body='Cannot edit.', status='draft',
        )
        response = self.client.get(reverse('messaging:edit_draft', args=[msg.pk]))
        self.assertEqual(response.status_code, 404)

    # ─── Delete ──────────────────────────────────

    def test_delete_draft(self):
        """Test deleting a draft message."""
        self.client.login(username='sarah', password='testpass123')
        msg = Message.objects.create(
            sender=self.user, team=self.team,
            subject='Delete Me', body='Gone.', status='draft',
        )
        response = self.client.post(reverse('messaging:delete_message', args=[msg.pk]))
        self.assertRedirects(response, reverse('messaging:drafts'))
        self.assertEqual(Message.objects.count(), 0)

    def test_delete_sent_message(self):
        """Test deleting a sent message."""
        self.client.login(username='sarah', password='testpass123')
        msg = Message.objects.create(
            sender=self.user, team=self.team,
            subject='Sent Delete', body='Gone.',
            status='sent', sent_at=timezone.now(),
        )
        response = self.client.post(reverse('messaging:delete_message', args=[msg.pk]))
        self.assertRedirects(response, reverse('messaging:sent'))
        self.assertEqual(Message.objects.count(), 0)

    def test_cannot_delete_other_users_message(self):
        """Test that users cannot delete someone else's message."""
        self.client.login(username='sarah', password='testpass123')
        msg = Message.objects.create(
            sender=self.other_user, team=self.team,
            subject='Not Mine', body='Cannot delete.', status='sent',
            sent_at=timezone.now(),
        )
        response = self.client.post(reverse('messaging:delete_message', args=[msg.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Message.objects.count(), 1)

    def test_delete_confirmation_page(self):
        """Test that GET on delete shows confirmation page."""
        self.client.login(username='sarah', password='testpass123')
        msg = Message.objects.create(
            sender=self.user, team=self.team,
            subject='Confirm Delete', body='Are you sure?', status='draft',
        )
        response = self.client.get(reverse('messaging:delete_message', args=[msg.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confirm Delete')
        self.assertEqual(Message.objects.count(), 1)

    # ─── Success Page ────────────────────────────

    def test_success_page_renders(self):
        """Test success page loads."""
        self.client.login(username='sarah', password='testpass123')
        response = self.client.get(reverse('messaging:send_success'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Message sent successfully')
