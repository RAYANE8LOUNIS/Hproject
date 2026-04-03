from django.shortcuts import render, get_object_or_404
from organisation.models import Team, Dependency
from django.http import HttpResponse
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
    return HttpResponse(f"Email page for team: {team.name}")


@login_required
def schedule_meeting(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return HttpResponse(f"Schedule meeting page for team: {team.name}")