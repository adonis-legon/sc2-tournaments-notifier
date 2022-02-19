from datetime import datetime
import pytest

from src.app.scraper import get_tournaments, TournamentQueryType


@pytest.fixture(name="upcoming_and_ongoing")
def fixture_upcoming_and_ongoing():
    '''function to create the upcoming and ongoing test function parameters'''
    return [TournamentQueryType.UPCOMING, TournamentQueryType.ONGOING]


def test_upcoming_and_ongoing_tournaments_are_after_today(upcoming_and_ongoing):
    '''tes for upcoming and ongoing events'''
    today = datetime.now()
    tournaments = get_tournaments(upcoming_and_ongoing)

    for tournament_query_type_item in tournaments.items():
        for tournament_link_item in tournament_query_type_item[1].items():
            assert tournament_link_item[1]['date_from'] >= today
