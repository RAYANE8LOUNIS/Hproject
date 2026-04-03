from django.shortcuts import render, get_object_or_404
from organisation.models import Team, Dependency


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