'''module for web scraping methods'''

from datetime import datetime
from enum import Enum

import requests
from bs4 import BeautifulSoup


class TournamentQueryType(Enum):
    """
    Enum for the type of Tournament Query
    """
    UPCOMING = 1
    ONGOING = 2
    COMPLETED = 3

    def __str__(self):
        '''method to convert from TournamentQueryType to string'''

        if self.value == TournamentQueryType.UPCOMING.value:
            return 'upcoming'

        if self.value == TournamentQueryType.ONGOING.value:
            return 'ongoing'

        if self.value == TournamentQueryType.COMPLETED.value:
            return 'completed'

        return None


def get_tournaments(query_types=None):
    '''method to scrape the website for getting the query types passed from parameters'''

    if query_types is None:
        query_types = [TournamentQueryType.UPCOMING]

    home_url = "https://liquipedia.net"

    soup = BeautifulSoup(requests.get(
        home_url + "/starcraft2/Main_Page").content, "html.parser")

    tournaments = {}
    for query_type in query_types:
        tournaments_links = [home_url + e["href"] for e in soup.select(
            f'#tournaments-menu-{str(query_type)} > li > a.dropdown-item')]

        tournaments[query_type] = {}
        for tournament_link in tournaments_links:
            soup = BeautifulSoup(requests.get(
                tournament_link).content, "html.parser")

            tournaments[query_type][tournament_link] = {}

            date_from_elements = soup.find_all('div', string='Start Date:')
            if date_from_elements and len(date_from_elements) > 0:
                date_from_str = date_from_elements[0].find_next('div').text
                tournaments[query_type][tournament_link]['date_from'] = datetime.fromisoformat(
                    date_from_str).date()

            date_to_elements = soup.find_all('div', string='End Date:')
            if date_to_elements and len(date_to_elements) > 0:
                date_to_str = date_to_elements[0].find_next('div').text
                tournaments[query_type][tournament_link]['date_to'] = datetime.fromisoformat(
                    date_to_str).date()

    return tournaments
