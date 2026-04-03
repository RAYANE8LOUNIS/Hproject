from django.shortcuts import render, get_object_or_404, redirect
from organisation.models import Team, Dependency, Department, TeamType
from django.contrib.auth.models import User


def team_list(request):
    query = request.GET.get('q')

    if query:
        teams = Team.objects.filter(name__icontains=query)
    else:
        teams = Team.objects.all()

    return render(request, 'teams/team_list.html', {
        'teams': teams,
        'query': query
    })


def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    members = team.members.all() if hasattr(team, 'members') else []
    dependencies = Dependency.objects.filter(
        upstream_team=team
    ) | Dependency.objects.filter(
        downstream_team=team
    )

    return render(request, 'teams/team_detail.html', {
        'team': team,
        'members': members,
        'dependencies': dependencies
    })


def create_team(request):
    departments = Department.objects.all()
    team_types = TeamType.objects.all()
    users = User.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        purpose = request.POST.get('purpose')
        department_id = request.POST.get('department')
        team_type_id = request.POST.get('team_type')
        manager_id = request.POST.get('manager')
        slack_channel = request.POST.get('slack_channel')
        email = request.POST.get('email')
        code_repository = request.POST.get('code_repository')
        status = request.POST.get('status')

        department = Department.objects.get(id=department_id)
        team_type = TeamType.objects.get(id=team_type_id)
        manager = User.objects.get(id=manager_id)

        team = Team.objects.create(
            name=name,
            description=description,
            purpose=purpose,
            department=department,
            team_type=team_type,
            manager=manager,
            slack_channel=slack_channel,
            email=email,
            code_repository=code_repository,
            status=status
        )

        member_ids = request.POST.getlist('members')
        if member_ids:
            selected_users = User.objects.filter(id__in=member_ids)
            team.members.set(selected_users)

        return redirect('team_list')

    return render(request, 'teams/create_team.html', {
        'departments': departments,
        'team_types': team_types,
        'users': users
    })