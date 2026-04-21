from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Department, Team, TeamType, Dependency, AuditLog



# MODEL TESTS


class DepartmentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='leader', password='pass')
        self.dept = Department.objects.create(
            name='Engineering',
            specialisation='Backend',
            leader=self.user
        )

    def test_department_str(self):
        self.assertEqual(str(self.dept), 'Engineering')

    def test_department_team_count_zero(self):
        self.assertEqual(self.dept.team_count(), 0)

    def test_department_team_count_with_teams(self):
        team_type = TeamType.objects.create(name='Dev')
        Team.objects.create(name='Team A', department=self.dept, team_type=team_type)
        self.assertEqual(self.dept.team_count(), 1)


class TeamModelTest(TestCase):

    def setUp(self):
        self.dept = Department.objects.create(name='Cloud')
        self.team_type = TeamType.objects.create(name='Platform')
        self.manager = User.objects.create_user(username='manager', password='pass')
        self.team = Team.objects.create(
            name='Cloud Core',
            department=self.dept,
            team_type=self.team_type,
            manager=self.manager,
            status='active'
        )

    def test_team_str(self):
        self.assertEqual(str(self.team), 'Cloud Core')

    def test_team_default_status(self):
        self.assertEqual(self.team.status, 'active')

    def test_team_has_department(self):
        self.assertEqual(self.team.department.name, 'Cloud')


class DependencyModelTest(TestCase):

    def setUp(self):
        self.team_a = Team.objects.create(name='Team A')
        self.team_b = Team.objects.create(name='Team B')
        self.dep = Dependency.objects.create(
            upstream_team=self.team_a,
            downstream_team=self.team_b
        )

    def test_dependency_str(self):
        self.assertIn('Team A', str(self.dep))
        self.assertIn('Team B', str(self.dep))

    def test_unique_dependency(self):
        """Cannot create duplicate dependency between same two teams."""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Dependency.objects.create(
                upstream_team=self.team_a,
                downstream_team=self.team_b
            )


# VIEW TESTS


class OrganisationViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='admin@sky.com')
        self.dept = Department.objects.create(name='DevOps', specialisation='Infrastructure')
        self.team_type = TeamType.objects.create(name='SRE')
        self.team = Team.objects.create(name='SRE Core', department=self.dept, team_type=self.team_type)

    # ── Authentication tests 

    def test_overview_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('organisation:organisation_overview'))
        self.assertEqual(response.status_code, 302)

    def test_overview_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:organisation_overview'))
        self.assertEqual(response.status_code, 200)

    # ── Department views 

    def test_department_list_loads(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:department_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DevOps')

    def test_department_detail_loads(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:department_detail', args=[self.dept.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DevOps')

    def test_department_search(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:department_list') + '?q=DevOps')
        self.assertContains(response, 'DevOps')

    def test_department_search_no_results(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:department_list') + '?q=XXXXXXXXX')
        self.assertNotContains(response, 'DevOps')

    def test_department_create_denied_for_non_admin(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:department_create'))
        self.assertEqual(response.status_code, 302)

    def test_department_create_accessible_for_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('organisation:department_create'))
        self.assertEqual(response.status_code, 200)

    def test_department_create_post(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('organisation:department_create'), {
            'name': 'New Dept',
            'description': 'Test',
            'specialisation': 'Testing',
            'leader': ''
        })
        self.assertTrue(Department.objects.filter(name='New Dept').exists())

    def test_department_edit_post(self):
        self.client.login(username='admin', password='adminpass')
        self.client.post(reverse('organisation:department_edit', args=[self.dept.pk]), {
            'name': 'DevOps Updated',
            'description': '',
            'specialisation': 'Infrastructure',
            'leader': ''
        })
        self.dept.refresh_from_db()
        self.assertEqual(self.dept.name, 'DevOps Updated')

    def test_department_delete_post(self):
        self.client.login(username='admin', password='adminpass')
        dept_pk = self.dept.pk
        self.client.post(reverse('organisation:department_delete', args=[dept_pk]))
        self.assertFalse(Department.objects.filter(pk=dept_pk).exists())

    # ── Team views ────────────────────────────

    def test_team_list_loads(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:team_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SRE Core')

    def test_team_detail_loads(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:team_detail', args=[self.team.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SRE Core')

    # ── Dependency views ──────────────────────

    def test_dependency_map_loads(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:dependency_map'))
        self.assertEqual(response.status_code, 200)

    # ── Audit log

    def test_audit_log_denied_for_non_admin(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('organisation:audit_log'))
        self.assertEqual(response.status_code, 302)

    def test_audit_log_accessible_for_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('organisation:audit_log'))
        self.assertEqual(response.status_code, 200)

    def test_audit_log_created_on_department_create(self):
        self.client.login(username='admin', password='adminpass')
        self.client.post(reverse('organisation:department_create'), {
            'name': 'Audit Test Dept',
            'description': '',
            'specialisation': '',
            'leader': ''
        })
        self.assertTrue(AuditLog.objects.filter(model_name='Department', action='created').exists())
