from datetime import datetime
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

class WebScrapper:
    def __init__(self) -> None:
        self.url_for_matches = 'https://www.hltv.org/team/8297/furia#tab-matchesBox'
        self.url_for_events = 'https://www.hltv.org/team/8297/furia#tab-eventsBox'
        self.url_for_lineup = 'https://www.hltv.org/team/8297/furia#tab-rosterBox'
        self.url_for_player_stats = 'https://www.hltv.org/stats/players/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """Fetches the page content and returns a BeautifulSoup object."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

    def get_upcoming_events(self) -> List[Dict[str, str]]:
        soup = self._get_soup(self.url_for_events)
        if not soup:
            return []

        events = []
        divs = soup.find_all('div', class_='sub-tab-content-events')

        for evento in divs:
            event_name = evento.find('div', class_='eventbox-eventname').get_text(strip=True)
            event_date = evento.find('div', class_='eventbox-date').get_text(strip=True)
            events.append({'name': event_name, 'date': event_date})

        return events

    def get_previous_five_matches(self) -> List[Dict[str, str]]:
        soup = self._get_soup(self.url_for_matches)
        if not soup:
            return []

        matches = []
        tables = soup.find_all('table', class_='table-container match-table')

        for table in tables:
            event_name = table.find('thead').find_next_sibling('thead').find('a').text
            rows = table.find_all('tr', class_='team-row')

            for row in rows:
                date_str = row.find('td', class_='date-cell').get_text(strip=True)

                try:
                    match_date = datetime.strptime(date_str, '%d/%m/%Y')
                except ValueError:
                    continue

                if match_date < datetime.now():
                    teams = row.find('td', class_='team-center-cell')
                    team1 = teams.find_all('a', class_='team-name team-1')[0].text
                    team1_logo = teams.find_all('img', class_='team-logo')[0]['src']
                    score1 = teams.find_all('span', class_='score')[0].text
                    score2 = teams.find_all('span', class_='score')[1].text
                    team2 = teams.find_all('a', class_='team-name team-2')[0].text
                    team2_logo = teams.find_all('img', class_='team-logo')[1]['src']

                    matches.append({
                        'event': event_name,
                        'date': match_date.strftime('%Y-%m-%d'),
                        'team1': team1,
                        'team1_logo': team1_logo,
                        'score1': score1,
                        'score2': score2,
                        'team2': team2,
                        'team2_logo': team2_logo,
                    })
        return matches[:5]

    def get_upcoming_matches(self) -> List[Dict[str, str]]:
        soup = self._get_soup(self.url_for_matches)
        if not soup:
            return []

        matches = []
        tables = soup.find_all('table', class_='table-container match-table')

        for table in tables:
            event_name = table.find('thead').find_next_sibling('thead').find('a').text
            rows = table.find_all('tr', class_='team-row')

            for row in rows:
                date_str = row.find('td', class_='date-cell').get_text(strip=True)

                try:
                    match_date = datetime.strptime(date_str, '%d/%m/%Y')
                except ValueError:
                    continue

                if match_date > datetime.now():
                    teams = row.find('td', class_='team-center-cell')
                    team1 = teams.find_all('a', class_='team-name team-1')[0].text
                    team1_logo = teams.find_all('img', class_='team-logo')[0]['src']
                    score1 = teams.find_all('span', class_='score')[0].text
                    score2 = teams.find_all('span', class_='score')[1].text
                    team2 = teams.find_all('a', class_='team-name team-2')[0].text
                    team2_logo = teams.find_all('img', class_='team-logo')[1]['src']

                    matches.append({
                        'event': event_name,
                        'date': match_date.strftime('%Y-%m-%d'),
                        'team1': team1,
                        'team1_logo': team1_logo,
                        'score1': score1,
                        'score2': score2,
                        'team2': team2,
                        'team2_logo': team2_logo,
                    })
        return matches

    def get_current_lineup(self) -> List[Dict[str, str]]:
        soup = self._get_soup(self.url_for_lineup)
        if not soup:
            return []

        players = []
        table = soup.find('table', class_='table-container players-table')

        if table:
            rows = table.find('tbody').find_all('tr')

            for row in rows:
                player = {}
                player_name_cell = row.find('td', class_='playersBox-first-cell')
                if player_name_cell:
                    player['name'] = player_name_cell.find('div', class_='text-ellipsis').get_text(strip=True)
                players.append(player)
        else:
            print("Tabela não encontrada.")
        
        return players

    def get_player_stats(self, player: str) -> Dict[str, str]:
        soup = self._get_soup(self.url_for_player_stats + player)
        if not soup:
            return {}

        player_stats = {}
        nickname = soup.find('h1', class_='summaryNickname text-ellipsis')
        if nickname:
            player_stats['nickname'] = nickname.get_text(strip=True)

        real_name = soup.find('div', class_='summaryRealname text-ellipsis')
        if real_name:
            player_stats['real_name'] = real_name.find('div').get_text(strip=True)

        team = soup.find('div', class_='SummaryTeamname text-ellipsis')
        if team:
            player_stats['team'] = team.find('a').get_text(strip=True)

        age = soup.find('div', class_='summaryPlayerAge')
        if age:
            player_stats['age'] = age.get_text(strip=True).split()[0]

        stats = soup.find_all('div', class_='summaryStatBreakdown')
        for stat in stats:
            stat_name = stat.find('div', class_='summaryStatBreakdownSubHeader').contents[0].strip()
            stat_value = stat.find('div', class_='summaryStatBreakdownDataValue').get_text(strip=True)
            player_stats[stat_name] = stat_value

        return player_stats
