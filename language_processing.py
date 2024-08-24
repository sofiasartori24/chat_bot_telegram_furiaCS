import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier

class LanguageProcessing:
    def __init__(self) -> None:
        self.training_data = [
            # Next Matches ("next_match")
            (["quais", "são", "as", "próximas", "partidas", "do", "furia"], "next_match"),
            (["quando", "é", "o", "próximo", "jogo", "do", "furia"], "next_match"),
            (["qual", "é", "a", "próxima", "partida", "que", "o", "furia", "vai", "jogar"], "next_match"),
            (["tem", "jogo", "do", "furia", "vindo", "por", "aí"], "next_match"),
            (["me", "mostra", "o", "próximo", "jogo", "do", "furia"], "next_match"),
            (["o", "que", "vem", "por", "aí", "no", "calendário", "do", "furia"], "next_match"),
            (["quem", "é", "o", "próximo", "adversário", "do", "furia"], "next_match"),
            (["quando", "o", "furia", "joga", "de", "novo"], "next_match"),
            (["tem", "jogo", "marcado", "para", "o", "furia", "nos", "próximos", "dias"], "next_match"),
            (["qual", "é", "a", "agenda", "das", "próximas", "partidas", "do", "furia"], "next_match"),

            # Last Matches ("last_match")
            (["quais", "foram", "as", "últimas", "partidas", "do", "furia"], "last_match"),
            (["como", "o", "furia", "se", "saiu", "nos", "últimos", "jogos"], "last_match"),
            (["me", "mostra", "os", "resultados", "das", "últimas", "partidas", "do", "furia"], "last_match"),
            (["como", "foi", "o", "último", "jogo", "do", "furia"], "last_match"),
            (["quais", "foram", "os", "últimos", "adversários", "do", "furia"], "last_match"),
            (["o", "furia", "ganhou", "os", "últimos", "jogos"], "last_match"),
            (["mostra", "os", "placares", "das", "últimas", "partidas", "do", "furia"], "last_match"),
            (["como", "terminaram", "as", "últimas", "partidas", "que", "o", "furia", "jogou"], "last_match"),
            (["qual", "foi", "o", "resultado", "do", "último", "jogo", "do", "furia"], "last_match"),
            (["tem", "algum", "resultado", "recente", "das", "partidas", "do", "furia"], "last_match"),

            # Lineup ("lineup")
            (["qual", "é", "a", "lineup", "atual", "do", "furia"], "lineup"),
            (["quem", "está", "jogando", "no", "furia", "agora"], "lineup"),
            (["me", "fala", "a", "escalação", "atual", "do", "time"], "lineup"),
            (["qual", "é", "o", "elenco", "do", "furia", "no", "momento"], "lineup"),
            (["quem", "são", "os", "jogadores", "que", "estão", "jogando", "pelo", "furia"], "lineup"),
            (["quem", "está", "na", "equipe", "principal", "do", "furia"], "lineup"),
            (["mostra", "a", "lineup", "do", "furia"], "lineup"),
            (["quem", "são", "os", "titulares", "do", "furia"], "lineup"),
            (["qual", "é", "a", "formação", "atual", "do", "furia"], "lineup"),
            (["quais", "são", "os", "jogadores", "do", "furia", "neste", "campeonato"], "lineup"),

            # Next Events ("schedule")
            (["qual", "é", "o", "calendário", "do", "próximo", "evento", "do", "furia"], "schedule"),
            (["quando", "é", "o", "próximo", "torneio", "do", "furia"], "schedule"),
            (["o", "que", "tem", "marcado", "no", "calendário", "de", "eventos", "do", "furia"], "schedule"),
            (["quais", "são", "os", "próximos", "eventos", "que", "o", "furia", "vai", "participar"], "schedule"),
            (["quando", "o", "furia", "vai", "competir", "novamente"], "schedule"),
            (["me", "mostra", "a", "agenda", "do", "próximo", "evento", "do", "furia"], "schedule"),
            (["o", "que", "tem", "de", "campeonato", "agendado", "para", "o", "furia"], "schedule"),
            (["qual", "é", "o", "próximo", "campeonato", "do", "furia"], "schedule"),
            (["quando", "o", "furia", "joga", "no", "próximo", "evento"], "schedule"),
            (["tem", "algum", "torneio", "vindo", "para", "o", "furia"], "schedule"),

            # Fallen stats ("player_stats_fallen")
            (["quais", "são", "as", "estatísticas", "do", "FalleN"], "player_stats"),
            (["me", "mostra", "as", "stats", "do", "FalleN"], "player_stats"),
            (["quero", "saber", "as", "estatísticas", "do", "FalleN"], "player_stats"),
            (["estatísticas", "detalhadas", "do", "FalleN"], "player_stats"),
            (["como", "o", "FalleN", "tem", "se", "desempenhado"], "player_stats"),
            (["quais", "são", "as", "principais", "estatísticas", "do", "FalleN"], "player_stats"),
            (["me", "mostra", "o", "desempenho", "do", "FalleN"], "player_stats"),
            (["mostra", "as", "estatísticas", "recentes", "do", "FalleN"], "player_stats"),
            (["estatísticas", "atuais", "do", "FalleN"], "player_stats"),
            (["quero", "ver", "as", "stats", "detalhadas", "do", "FalleN"], "player_stats"),

            # Yuurih stats ("player_stats_yuurih")
            (["quais", "são", "as", "estatísticas", "do", "yuurih"], "player_stats"),
            (["me", "mostra", "as", "stats", "do", "yuurih"], "player_stats"),
            (["quero", "saber", "as", "estatísticas", "do", "yuurih"], "player_stats"),
            (["estatísticas", "detalhadas", "do", "yuurih"], "player_stats"),
            (["como", "o", "yuurih", "tem", "se", "desempenhado"], "player_stats"),
            (["quais", "são", "as", "principais", "estatísticas", "do", "yuurih"], "player_stats"),
            (["me", "mostra", "o", "desempenho", "do", "yuurih"], "player_stats"),
            (["mostra", "as", "estatísticas", "recentes", "do", "yuurih"], "player_stats"),
            (["estatísticas", "atuais", "do", "yuurih"], "player_stats"),
            (["quero", "ver", "as", "stats", "detalhadas", "do", "yuurih"], "player_stats"),

            # KSCERATO stats ("player_stats_kscerato")
            (["quais", "são", "as", "estatísticas", "do", "KSCERATO"], "player_stats"),
            (["me", "mostra", "as", "stats", "do", "KSCERATO"], "player_stats"),
            (["quero", "saber", "as", "estatísticas", "do", "KSCERATO"], "player_stats"),
            (["estatísticas", "detalhadas", "do", "KSCERATO"], "player_stats"),
            (["como", "o", "KSCERATO", "tem", "se", "desempenhado"], "player_stats"),
            (["quais", "são", "as", "principais", "estatísticas", "do", "KSCERATO"], "player_stats"),
            (["me", "mostra", "o", "desempenho", "do", "KSCERATO"], "player_stats"),
            (["mostra", "as", "estatísticas", "recentes", "do", "KSCERATO"], "player_stats"),
            (["estatísticas", "atuais", "do", "KSCERATO"], "player_stats"),
            (["quero", "ver", "as", "stats", "detalhadas", "do", "KSCERATO"], "player_stats"),

            # Chelo stats ("player_stats_chelo")
            (["quais", "são", "as", "estatísticas", "do", "chelo"], "player_stats"),
            (["me", "mostra", "as", "stats", "do", "chelo"], "player_stats"),
            (["quero", "saber", "as", "estatísticas", "do", "chelo"], "player_stats"),
            (["estatísticas", "detalhadas", "do", "chelo"], "player_stats"),
            (["como", "o", "chelo", "tem", "se", "desempenhado"], "player_stats"),
            (["quais", "são", "as", "principais", "estatísticas", "do", "chelo"], "player_stats"),
            (["me", "mostra", "o", "desempenho", "do", "chelo"], "player_stats"),
            (["mostra", "as", "estatísticas", "recentes", "do", "chelo"], "player_stats"),
            (["estatísticas", "atuais", "do", "chelo"], "player_stats"),
            (["quero", "ver", "as", "stats", "detalhadas", "do", "chelo"], "player_stats"),

            # Skullz stats ("player_stats_skullz")
            (["quais", "são", "as", "estatísticas", "do", "skullz"], "player_stats"),
            (["me", "mostra", "as", "stats", "do", "skullz"], "player_stats"),
            (["quero", "saber", "as", "estatísticas", "do", "skullz"], "player_stats"),
            (["estatísticas", "detalhadas", "do", "skullz"], "player_stats"),
            (["como", "o", "skullz", "tem", "se", "desempenhado"], "player_stats"),
            (["quais", "são", "as", "principais", "estatísticas", "do", "skullz"], "player_stats"),
            (["me", "mostra", "o", "desempenho", "do", "skullz"], "player_stats"),
            (["mostra", "as", "estatísticas", "recentes", "do", "skullz"], "player_stats"),
            (["estatísticas", "atuais", "do", "skullz"], "player_stats"),
            (["quero", "ver", "as", "stats", "detalhadas", "do", "skullz"], "player_stats"),

            # Help ("help")
            (["quais", "são", "os", "comandos", "disponíveis"], "help"),
            (["me", "mostra", "a", "lista", "de", "comandos"], "help"),
            (["como", "eu", "posso", "usar", "o", "bot"], "help"),
            (["ajuda", "com", "os", "comandos"], "help"),
            (["o", "que", "eu", "posso", "perguntar", "aqui"], "help"),
            (["qual", "é", "a", "lista", "completa", "de", "comandos"], "help"),
            (["ajuda", "com", "os", "comandos", "disponíveis"], "help"),
            (["quais", "comandos", "estão", "disponíveis"], "help"),
            (["como", "funciona", "o", "bot"], "help"),
            (["me", "diga", "quais", "comandos", "eu", "posso", "usar"], "help"),

            # Greetings 
            (["oi"], "greeting"),
            (["olá"], "greeting"),
            (["e", "aí"], "greeting"),
            (["tudo", "bem"], "greeting"),
            (["como", "vai"], "greeting")
        ]
        self.training_set = [(self.extract_features(word_tokenize(" ".join(sentence))), intent) for sentence, intent in self.training_data]
        self.classifier = NaiveBayesClassifier.train(self.training_set)

    def extract_features(self, words):
        return {word: True for word in words}

    def detect_intent(self, user_input):
        features = self.extract_features(word_tokenize(user_input))
        return self.classifier.classify(features)

