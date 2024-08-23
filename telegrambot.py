import os
from dotenv import load_dotenv
import telebot
from web_scraping_hltv import Web_scrapper

menu =  """
👋 Olá, Furioso(a)! 🐾 
Eu sou o bot oficial do FURIA CS2. 🎯
Aqui você fica por dentro de tudo sobre o melhor time 🔥🔥🔥!

🛠️ Comandos Disponíveis:
/nextmatch - Exibe as próximas partidas do FURIA.
/lastmatch - Mostra o resultado das últimas cinco partidas jogadas.
/lineup - Exibe a line atual 
/playerstats - Veja as estatísticas detalhadas de um jogador específico.
/schedule - Confira o calendário do próximo evento.
💥 Vamos torcer juntos! GG WP!
"""
#/reminder [hora] - Defina um lembrete para não perder a próxima partida. maybe do later

load_dotenv()
api_key = os.getenv("API_KEY")
#initializing bot
bot = telebot.TeleBot(api_key)

web_scrapper = Web_scrapper()

@bot.message_handler(commands=["lastmatch"])
def next_match(message):
    matches = web_scrapper.get_previous_five_matches()  # Coleta as partidas futuras
    
    if matches:
        # Formata a resposta com as informações das partidas
        response_message = "Essas são as últimas 5 partidas jogadas pela Furia:\n\n"
        
        for match in matches:
            response_message += (
                f"🗓️ Evento: {match['event']}\n"
                f"📅 Data: {match['date']}\n"
                f"⚔️ {match['team1']} vs {match['team2']}\n"
                f"Placar: {match['score1']} - {match['score2']}\n\n"
            )
        
        bot.reply_to(message, response_message)
    else:
        bot.reply_to(message, "Não há partidas passadas disponíveis no momento.")

@bot.message_handler(commands=["nextmatch"])
def next_match(message):
    matches = web_scrapper.get_upcoming_matches()  # Coleta as partidas futuras
    
    if matches:
        # Formata a resposta com as informações das partidas
        response_message = "Essas são as próximas partidas da Furia:\n\n"
        
        for match in matches:
            response_message += (
                f"🗓️ Evento: {match['event']}\n"
                f"📅 Data: {match['date']}\n"
                f"⚔️ {match['team1']} vs {match['team2']}\n"
                "Não esqueça de torcer muito!"
            )
        
        bot.reply_to(message, response_message)
    else:
        bot.reply_to(message, "Não há partidas futuras disponíveis no momento.")

@bot.message_handler(commands=["lineup"])
def current_players(message):
    line = web_scrapper.get_current_lineup()

    if line:
        response_message = "Essa é a line Furiosa atual 🔥🔥🔥\n\n"
        for player in line:
            response_message += (
                f"🐾 {player['name']}\n" 
            )
        bot.reply_to(message, response_message)
    else:
        bot.reply_to(message, "Parece que tivemos um problema para recuperar essa informação. Sinto Muito!")


@bot.message_handler(commands=["schedule"])
def schedule(message):
    event = web_scrapper.get_upcoming_events()[0]

    if event:
        response_message = "Esses é o próximo evento da Furia! Não esqueça de torcer 🔥:\n\n"
        response_message += (
            f"Nome: {event['name']}\n"
            f"📅 Data: {event['date']}\n\n"
        )
        bot.reply_to(message,response_message )
    else:
        bot.reply_to(message, "Parece que não há eventos disponíveis no momento. Nossos Players precisam descansar")

@bot.message_handler(commands=['playerstats'])
def player_stats(message):
    response_message = """
    Qual jogador você quer saber as estatísticas? 🐾
    /yuurih
    /KSCERATO
    /chelo
    /FalleN
    /skullz   
    """
    bot.reply_to(message, response_message)

@bot.message_handler(commands=['FalleN'])
def player_stats(message):
    stats_fallen = web_scrapper.get_player_stats('2023/fallen')

    response_message = "Essas são as estatísticas atuais do Professor 🔥🔥🐾\n\n"
    if stats_fallen:
        response_message += (
            f"Nick: {stats_fallen['nickname']}\n"
            f"Nome: {stats_fallen['real_name']}\n"
            f"Idade: {stats_fallen['age']}\n\n"

            f"Rating: {stats_fallen['Rating 1.0']}\n"
            f"DPR: {stats_fallen['DPR']}\n"
            f"KAST: {stats_fallen['KAST']}\n"
            f"Impact: {stats_fallen['Impact']}\n"
            f"ADR: {stats_fallen['ADR']}\n"
            f"KPR: {stats_fallen['KPR']}\n"
        )
        bot.reply_to(message,response_message )
    else:
        bot.reply_to(message, "Parece que não estatísticas disponíveis. Sinto Muito!")

@bot.message_handler(commands=['yuurih'])
def player_stats(message):
    stats_yuurih = web_scrapper.get_player_stats('12553/yuurih')

    response_message = "Essas são as estatísticas atuais do Yuurih 🔥🔥🐾\n\n"
    if stats_yuurih:
        response_message += (
            f"Nick: {stats_yuurih['nickname']}\n"
            f"Nome: {stats_yuurih['real_name']}\n"
            f"Idade: {stats_yuurih['age']}\n\n"

            f"Rating: {stats_yuurih['Rating 2.0']}\n"
            f"DPR: {stats_yuurih['DPR']}\n"
            f"KAST: {stats_yuurih['KAST']}\n"
            f"Impact: {stats_yuurih['Impact']}\n"
            f"ADR: {stats_yuurih['ADR']}\n"
            f"KPR: {stats_yuurih['KPR']}\n"
        )
        bot.reply_to(message,response_message )
    else:
        bot.reply_to(message, "Parece que não estatísticas disponíveis. Sinto Muito!")

@bot.message_handler(commands=['KSCERATO'])
def player_stats(message):
    stats_ks = web_scrapper.get_player_stats('15631/kscerato')

    response_message = "Essas são as estatísticas atuais do KSCERATO 🔥🔥🐾\n\n"
    if stats_ks:
        response_message += (
            f"Nick: {stats_ks['nickname']}\n"
            f"Nome: {stats_ks['real_name']}\n"
            f"Idade: {stats_ks['age']}\n\n"

            f"Rating: {stats_ks['Rating 2.0']}\n"
            f"DPR: {stats_ks['DPR']}\n"
            f"KAST: {stats_ks['KAST']}\n"
            f"Impact: {stats_ks['Impact']}\n"
            f"ADR: {stats_ks['ADR']}\n"
            f"KPR: {stats_ks['KPR']}\n"
        )
        bot.reply_to(message,response_message )
    else:
        bot.reply_to(message, "Parece que não estatísticas disponíveis. Sinto Muito!")

@bot.message_handler(commands=['chelo'])
def player_stats(message):
    stats_chelo = web_scrapper.get_player_stats('10566/chelo')

    response_message = "Essas são as estatísticas atuais do Chelo 🔥🔥🐾\n\n"
    if stats_chelo:
        response_message += (
            f"Nick: {stats_chelo['nickname']}\n"
            f"Nome: {stats_chelo['real_name']}\n"
            f"Idade: {stats_chelo['age']}\n\n"

            f"Rating: {stats_chelo['Rating 1.0']}\n"
            f"DPR: {stats_chelo['DPR']}\n"
            f"KAST: {stats_chelo['KAST']}\n"
            f"Impact: {stats_chelo['Impact']}\n"
            f"ADR: {stats_chelo['ADR']}\n"
            f"KPR: {stats_chelo['KPR']}\n"
        )
        bot.reply_to(message,response_message )
    else:
        bot.reply_to(message, "Parece que não estatísticas disponíveis. Sinto Muito!")

@bot.message_handler(commands=['skullz'])
def player_stats(message):
    stats_skullz = web_scrapper.get_player_stats('18676/skullz')

    response_message = "Essas são as estatísticas atuais do Skullz 🔥🔥🐾\n\n"
    if stats_skullz:
        response_message += (
            f"Nick: {stats_skullz['nickname']}\n"
            f"Nome: {stats_skullz['real_name']}\n"
            f"Idade: {stats_skullz['age']}\n\n"

            f"Rating: {stats_skullz['Rating 2.0']}\n"
            f"DPR: {stats_skullz['DPR']}\n"
            f"KAST: {stats_skullz['KAST']}\n"
            f"Impact: {stats_skullz['Impact']}\n"
            f"ADR: {stats_skullz['ADR']}\n"
            f"KPR: {stats_skullz['KPR']}\n"
        )
        bot.reply_to(message,response_message )
    else:
        bot.reply_to(message, "Parece que não estatísticas disponíveis. Sinto Muito!")
        
        
def check_for_base_response(message):
    return True

@bot.message_handler(func=check_for_base_response)
def base_response(message):
    bot.reply_to(message, menu)

