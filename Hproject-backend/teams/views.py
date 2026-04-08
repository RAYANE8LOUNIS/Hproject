from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from organisation.models import Team, Dependency
from django.contrib.auth.decorators import login_required


@login_required
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


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    members = team.members.all()
    upstream_dependencies = Dependency.objects.filter(upstream_team=team)
    downstream_dependencies = Dependency.objects.filter(downstream_team=team)

    return render(request, 'teams/team_detail.html', {
        'team': team,
        'members': members,
        'upstream_dependencies': upstream_dependencies,
        'downstream_dependencies': downstream_dependencies
    })


@login_required
def email_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'teams/email_team.html', {
        'team': team
    })


@login_required
def schedule_meeting(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    members = team.members.all()

    success_message = None
    submitted_data = None

    if request.method == 'POST':
        title = request.POST.get('title')
        meeting_date = request.POST.get('meeting_date')
        meeting_time = request.POST.get('meeting_time')
        platform = request.POST.get('platform')
        message = request.POST.get('message')
        selected_members = request.POST.getlist('members')

        selected_usernames = [member.username for member in members if str(member.id) in selected_members]

        submitted_data = {
            'title': title,
            'meeting_date': meeting_date,
            'meeting_time': meeting_time,
            'platform': platform,
            'message': message,
            'selected_usernames': selected_usernames,
        }

        success_message = f"Meeting for {team.name} scheduled successfully."

    return render(request, 'teams/schedule_meeting.html', {
        'team': team,
        'members': members,
        'success_message': success_message,
        'submitted_data': submitted_data,
    })


def api_teams(request):
    teams = Team.objects.select_related("department", "team_type", "manager").all()

    data = []
    for team in teams:
        data.append({
            "id": team.id,
            "name": team.name,
            "manager": team.manager.username if team.manager else "Manager",
            "department": team.department.name if team.department else "Department",
            "team_type": team.team_type.name if team.team_type else "No Team Type",
            "members": team.members.count(),
            "repositories": 1 if team.code_repository else 0,
            "status": team.get_status_display(),
        })

    return JsonResponse(data, safe=False)


def api_team_detail(request, team_id):
    team = get_object_or_404(
        Team.objects.select_related("department", "team_type", "manager"),
        id=team_id
    )

    members = [
        {
            "id": member.id,
            "username": member.username,
        }
        for member in team.members.all()
    ]

    upstream_dependencies = [
        {
            "id": dep.id,
            "team_name": dep.downstream_team.name,
            "description": dep.description,
        }
        for dep in Dependency.objects.filter(upstream_team=team).select_related("downstream_team")
    ]

    downstream_dependencies = [
        {
            "id": dep.id,
            "team_name": dep.upstream_team.name,
            "description": dep.description,
        }
        for dep in Dependency.objects.filter(downstream_team=team).select_related("upstream_team")
    ]

    data = {
        "id": team.id,
        "name": team.name,
        "manager": team.manager.username if team.manager else "Manager",
        "department": team.department.name if team.department else "Department",
        "team_type": team.team_type.name if team.team_type else "No Team Type",
        "status": team.get_status_display(),
        "members_count": team.members.count(),
        "repositories_count": 1 if team.code_repository else 0,
        "description": team.description or "",
        "email": team.email or "",
        "slack_channel": team.slack_channel or "",
        "code_repository": team.code_repository or "",
        "members": members,
        "upstream_dependencies": upstream_dependencies,
        "downstream_dependencies": downstream_dependencies,
    }

    return JsonResponse(data)