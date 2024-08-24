import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class Web_scrapper():
    def __init__(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.service = Service("/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

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

    def get_upcoming_events(self):
        try:
            # Configurações do Selenium para executar o Chrome em modo headless (sem interface gráfica)
            options = Options()
            options.headless = True

            # Inicializa o WebDriver do Chrome
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            
            # Acessa a URL dos eventos
            driver.get(self.url_for_events)
            
            # Espera o carregamento do conteúdo relevante (pode-se ajustar isso com WebDriverWait, se necessário)
            
            # Extrai os eventos da página
            events = []
            event_elements = driver.find_elements(By.CLASS_NAME, 'sub-tab-content-events')

            for evento in event_elements:
                try:
                    event_name = evento.find_element(By.CLASS_NAME, 'eventbox-eventname').text.strip()
                    event_date = evento.find_element(By.CLASS_NAME, 'eventbox-date').text.strip()
                    
                    events.append({
                        'name': event_name,
                        'date': event_date
                    })
                except NoSuchElementException as e:
                    print(f"Erro ao processar o evento: {e}")

            driver.quit()

            return events

        except Exception as e:
            print(f"Erro ao fazer o scraping dos eventos: {e}")
            return []

    def get_previous_five_matches(self):
        try:
            response = requests.get(self.url_for_matches, headers=self.headers)
            response.raise_for_status()  # Lança uma exceção para códigos de status HTTP de erro
            soup = BeautifulSoup(response.content, 'html.parser')
            matches = []
            tables = soup.find_all('table', class_='table-container match-table')

            for table in tables:
                event_name = table.find('thead').find_next_sibling('thead').find('a').text
                rows = table.find_all('tr', class_='team-row')

                for row in rows:
                    date_str = row.find('td', class_='date-cell').get_text(strip=True)

                    try:
                        match_date = datetime.strptime(date_str, '%d/%m/%Y')
                    except ValueError as e:
                        print(f"Erro ao converter a data: {e}")
                        continue

                    current_date = datetime.now()

                    if match_date < current_date:
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

        except requests.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return []
        except Exception as e:
            print(f"Erro ao processar partidas anteriores: {e}")
            return []

    def get_upcoming_matches(self):
        try:
            response = requests.get(self.url_for_matches, headers=self.headers)
            response.raise_for_status()  # Lança uma exceção para códigos de status HTTP de erro
            soup = BeautifulSoup(response.content, 'html.parser')
            matches = []
            tables = soup.find_all('table', class_='table-container match-table')

            for table in tables:
                event_name = table.find('thead').find_next_sibling('thead').find('a').text
                rows = table.find_all('tr', class_='team-row')

                for row in rows:
                    date_str = row.find('td', class_='date-cell').get_text(strip=True)

                    try:
                        match_date = datetime.strptime(date_str, '%d/%m/%Y')
                    except ValueError as e:
                        print(f"Erro ao converter a data: {e}")
                        continue

                    current_date = datetime.now()

                    if match_date > current_date:
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

        except requests.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return []
        except Exception as e:
            print(f"Erro ao processar partidas futuras: {e}")
            return []

    def get_current_lineup(self):
        try:
            response = requests.get(self.url_for_lineup, headers=self.headers)
            response.raise_for_status()  # Lança uma exceção para códigos de status HTTP de erro
            soup = BeautifulSoup(response.content, 'html.parser')

            table = soup.find('table', class_='table-container players-table')

            if table is not None:
                rows = table.find('tbody').find_all('tr')
                players = []

                for row in rows:
                    player = {}

                    player_name_cell = row.find('td', class_='playersBox-first-cell')
                    if player_name_cell:
                        player['name'] = player_name_cell.find('div', class_='text-ellipsis').get_text(strip=True)
                    players.append(player)
                
                return players

            else:
                print("Tabela não encontrada.")
                return []

        except requests.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return []
        except Exception as e:
            print(f"Erro ao processar a lineup atual: {e}")
            return []

    def get_player_stats(self, player: str):
        try:
            response = requests.get(self.url_for_player_stats + player, headers=self.headers)
            response.raise_for_status()  # Lança uma exceção para códigos de status HTTP de erro
            soup = BeautifulSoup(response.content, 'html.parser')

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
                stat_name = stat.find('div', class_='summaryStatBreakdownSubHeader').contents[0].strip()  # Pega apenas o nome
                stat_value = stat.find('div', class_='summaryStatBreakdownDataValue').get_text(strip=True)
                player_stats[stat_name] = stat_value

            return player_stats

        except requests.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return {}
        except Exception as e:
            print(f"Erro ao processar estatísticas do jogador: {e}")
            return {}
