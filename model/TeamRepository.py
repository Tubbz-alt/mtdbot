from model import (
    Team,
    TeamHistory,
    UserRepository
)


def get_all_teams():
    return Team.select()


def register_new_team(
        users
):
    team = Team.create()
    for member in users:
        member.team = team
        UserRepository.update_user(member)
        TeamHistory.create(
            user=member,
            team=team
        )
