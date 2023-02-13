import yaml
from server import Server
from telegram_bot import TelegramBot
from analytics import Analytics

if __name__ == '__main__':
    with open("data/config.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)

    bot = TelegramBot(config['telegram'])
    analytics = Analytics(config['analytics'])
    server = Server(config['server'], bot, analytics)
    server.add_routes(config['properties'])
    server.run()