from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from organisation.models import Department, Team


@login_required
def charts(request):
    departments = Department.objects.all().order_by("name")
    teams = Team.objects.all().order_by("name")

    department_names = []
    teams_per_department = []
    repos_per_department = []

    for department in departments:
        department_names.append(department.name)

        department_teams = Team.objects.filter(department=department)

        teams_per_department.append(department_teams.count())
        repos_per_department.append(
            department_teams.exclude(code_repository__isnull=True)
            .exclude(code_repository="")
            .count()
        )

    team_names = []
    member_counts = []

    for team in teams:
        team_names.append(team.name)
        member_counts.append(team.members.count())

    context = {
        "department_names": department_names,
        "teams_per_department": teams_per_department,
        "repos_per_department": repos_per_department,
        "team_names": team_names,
        "member_counts": member_counts,
        "total_departments": departments.count(),
        "total_teams": teams.count(),
        "total_repositories": teams.exclude(code_repository__isnull=True).exclude(code_repository="").count(),
    }

    return render(request, "datavis/charts.html", context)