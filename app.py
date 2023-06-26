import yaml
from server import Server
from telegram_bot import TelegramBot
from analytics import Analytics
from database import Database

class App:
    def __init__(self, config):
        self.bot = TelegramBot(config['telegram'])
        self.analytics = Analytics(config['analytics'])
        self.database = Database(config['database'])

        self.server = Server(config['server'])
        self.server.add_routes(config['properties'])
        self.server.register_report_callback(self.send_report)
        self.server.register_sync_callback(self.sync_property)
        self.server.register_names_callback(self.set_names)
        self.server.data_source = self.get_data
        
    def run(self):
        self.server.run()

    async def sync_property(self, property):
        report = self.analytics.run_report(property.dimension, property.event_filter, property.limit)
        await self.database.update_property(property.endpoint, report)

    async def send_report(self, property):
        report = await self.database.fetch_diff_property(property.endpoint)
        await self.bot.send_report(report, title=property.title)
    
    async def set_names(self, property, names):
        await self.database.update_names(property, names)

    async def get_data(self, property):
        return await self.database.fetch_property(property)
    
if __name__ == '__main__':
    with open("data/config.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
    app = App(config)
    app.run()
