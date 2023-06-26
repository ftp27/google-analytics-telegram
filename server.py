from aiohttp import web
from database import PropertyEncoder
import json

class AnalyticsProperty:
    def __init__(self, config):
        self.title = config['title']
        self.dimension = config['dimension']
        self.event_filter = config.get('event_filter', None)
        self.limit = config['limit']
        self.endpoint = config['endpoint']
        self.plugin = config.get('plugin', None)

class Server: 
    report_callback = []
    sync_callback = []
    names_callback = []
    data_source = {}

    def __init__(self, config):
        self.host = config.get('host', '0.0.0.0')
        self.port = config.get('port', 8080)
        self.app = web.Application()
        self.app.add_routes([
            web.get('/report/{property}', self.handle_report),
            web.get('/data/{property}', self.handle_data),
            web.get('/sync/{property}', self.handle_sync),
            web.post('/names/{property}', self.handle_names),
        ])
        self.properties = {}
    
    def add_routes(self, properties):
        for property in properties:
            item = AnalyticsProperty(property)
            self.properties[item.endpoint] = item

    def register_report_callback(self, callback):
        self.report_callback.append(callback)

    def register_sync_callback(self, callback):
        self.sync_callback.append(callback)

    def register_names_callback(self, callback):
        self.names_callback.append(callback)
        
    async def handle_report(self, request):
        property_id = request.match_info['property']
        if property_id in self.properties:
            property = self.properties[property_id]
            for callback in self.report_callback:
                await callback(property)
            return web.Response(text='ok')
        else:
            raise web.HTTPNotFound()
        
    async def handle_data(self, request):
        property_id = request.match_info['property']
        data = await self.data_source(property_id)
        if data == None:
            raise web.HTTPNotFound()
        else:
            return web.Response(text=json.dumps(data, cls=PropertyEncoder), content_type='application/json')
        
    async def handle_sync(self, request):
        property_id = request.match_info['property']
        if property_id in self.properties:
            property = self.properties[property_id]
            for callback in self.sync_callback:
                await callback(property)
            return web.Response(text='ok')
        else:
            raise web.HTTPNotFound()
        
    async def handle_names(self, request):
        property_id = request.match_info['property']
        if request.body_exists:
            body = await request.json()
            for callback in self.names_callback:
                await callback(property_id, body)
            return web.Response(text='ok')
        else:
            web.HTTPBadRequest()
        
    def run(self):
        web.run_app(self.app, host=self.host, port=self.port)