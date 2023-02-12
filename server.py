from aiohttp import web
from telegram_bot import TelegramBot
from analytics import Analytics

class Server: 
    def __init__(self, config, telegram: TelegramBot, analytics: Analytics):
        self.telegram = telegram
        self.analytics = analytics
        self.host = config['host']
        self.port = config['port']
        self.app = web.Application()
        self.app.add_routes([
            web.get('/analytics/templates', self.handle_analytics_templates),
            web.get('/analytics/categories', self.handle_analytics_categories)
        ])

    async def handle_analytics_templates(self, request):
        report = self.analytics.run_report("reel_name", 15)
        await self.telegram.send_report(report, title='Popular templates')
        return web.Response(text='ok')

    async def handle_analytics_categories(self, request):
        report = self.analytics.run_report("category_name", 15)
        await self.telegram.send_report(report, title='Popular categories')
        return web.Response(text='ok')

    def run(self):
        web.run_app(self.app, host=self.host, port=self.port)