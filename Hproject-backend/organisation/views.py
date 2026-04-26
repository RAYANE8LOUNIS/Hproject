from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Department, Team, Dependency, AuditLog
from .forms import DepartmentForm, DependencyForm


# ───────────── DEPARTMENTS ─────────────

@login_required
def department_list(request):
    query = request.GET.get('q', '')

    departments = Department.objects.select_related('leader').prefetch_related('teams')

    if query:
        departments = departments.filter(
            Q(name__icontains=query) |
            Q(specialisation__icontains=query) |
            Q(leader__first_name__icontains=query) |
            Q(leader__last_name__icontains=query)
        )

    return render(request, 'organisation/department_list.html', {
        'departments': departments,
        'query': query,
    })


@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    teams = department.teams.select_related('manager', 'team_type').prefetch_related('members')

    return render(request, 'organisation/department_detail.html', {
        'department': department,
        'teams': teams,
    })


@login_required
def department_create(request):
    if not request.user.is_staff:
        return redirect('organisation:department_list')

    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()

            AuditLog.objects.create(
                user=request.user,
                action='created',
                model_name='Department',
                object_id=department.pk,
                description=f'Department "{department.name}" created.'
            )

            return redirect('organisation:department_detail', pk=department.pk)
    else:
        form = DepartmentForm()

    return render(request, 'organisation/department_form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
def department_edit(request, pk):
    if not request.user.is_staff:
        return redirect('organisation:department_list')

    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()

            AuditLog.objects.create(
                user=request.user,
                action='updated',
                model_name='Department',
                object_id=department.pk,
                description=f'Department "{department.name}" updated.'
            )

            return redirect('organisation:department_detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'organisation/department_form.html', {
        'form': form,
        'action': 'Edit'
    })


@login_required
def department_delete(request, pk):
    if not request.user.is_staff:
        return redirect('organisation:department_list')

    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        name = department.name

        AuditLog.objects.create(
            user=request.user,
            action='deleted',
            model_name='Department',
            object_id=department.pk,
            description=f'Department "{name}" deleted.'
        )

        department.delete()
        return redirect('organisation:department_list')

    return render(request, 'organisation/department_confirm_delete.html', {
        'department': department
    })


# ───────────── TEAMS ─────────────

@login_required
def team_list(request):
    query = request.GET.get('q', '')

    teams = Team.objects.select_related('department', 'manager', 'team_type').prefetch_related('members')

    if query:
        teams = teams.filter(
            Q(name__icontains=query) |
            Q(department__name__icontains=query) |
            Q(manager__first_name__icontains=query) |
            Q(manager__last_name__icontains=query)
        )

    return render(request, 'organisation/team_list.html', {
        'teams': teams,
        'query': query,
    })


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)

    upstream = Dependency.objects.filter(upstream_team=team)
    downstream = Dependency.objects.filter(downstream_team=team)

    return render(request, 'organisation/team_detail.html', {
        'team': team,
        'upstream_dependencies': upstream,
        'downstream_dependencies': downstream,
    })


# ───────────── AUDIT LOG ─────────────

@login_required
def audit_log(request):
    if not request.user.is_staff:
        return redirect('organisation:department_list')

    logs = AuditLog.objects.select_related('user').order_by('-timestamp')

    return render(request, 'organisation/audit_log.html', {
        'logs': logs
    })