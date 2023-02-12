from aiohttp import web
from telegram_bot import TelegramBot
from analytics import Analytics

class AnalyticsProperty:
    def __init__(self, config):
        self.title = config['title']
        self.dimension = config['dimension']
        self.limit = config['limit']
        self.endpoint = config['endpoint']

class Server: 
    def __init__(self, config, telegram: TelegramBot, analytics: Analytics):
        self.telegram = telegram
        self.analytics = analytics
        self.host = config['host']
        self.port = config['port']
        self.app = web.Application()
        self.app.add_routes([
            web.get('/analytics/{property}', self.handle_analytics)
        ])
        self.properties = {}
    
    def add_routes(self, properties):
        for property in properties:
            item = AnalyticsProperty(property)
            self.properties[item.endpoint] = item
        
    async def handle_analytics(self, request):
        property_id = request.match_info['property']
        if property_id in self.properties:
            property = self.properties[property_id]
            report = self.analytics.run_report(property.dimension, property.limit)
            await self.telegram.send_report(report, title=property.title)
            return web.Response(text='ok')
        else:
            raise web.HTTPNotFound()
        
    def run(self):
        web.run_app(self.app, host=self.host, port=self.port)