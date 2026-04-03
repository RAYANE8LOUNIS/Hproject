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