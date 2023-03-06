from peewee import *
from datetime import datetime
from datetime import timezone
from json import JSONEncoder

db = DatabaseProxy()

class Database:
    def __init__(self, config):
        db.initialize(SqliteDatabase(f"data/{config['name']}"))
        db.connect()
        db.create_tables([PropertyItem, PropertyName])

    async def update_property(self, property, report):
        timestamp = datetime.utcnow()
        for (id, value) in report:
            print(f"{property}, {id} - {value}")
            property_item = PropertyItem.create(
                id=id,
                amount=value, 
                property_id=property, 
                timestamp=timestamp
            )
            property_item.save()
    
    async def update_names(self, property: str, data):
        for item in data:
            name_select = PropertyName.select() \
                .where(PropertyName.property_id == property) \
                .where(PropertyName.id == item['id']) 
            if name_select.exists():
                name = name_select.get()
                name.name = item['name']
            else:
                name = PropertyName.create(
                    id = item['id'],
                    name = item['name'],
                    property_id = property
                )
            name.save()

    async def fetch_property_by_time(self, property: str, timestamp):
        query = PropertyItem \
            .select() \
            .where(PropertyItem.property_id == property) \
            .where(PropertyItem.timestamp == timestamp) \
            .order_by(PropertyItem.amount.desc()) 
        
        result = []
        for row in query:
            item = PropertyDisplay(
                row.id,
                row.amount, 
                property, 
                row.id, 
                row.timestamp.isoformat()
            )
            result.append(item)
        return result
    
    async def update_with_names(self, property: str, items):
        for item in items:
            name_select = PropertyName.select() \
                .where(PropertyName.property_id == property) \
                .where(PropertyName.id == item.id) 
            if name_select.exists():
                item.name = name_select.get().name
    
    async def fetch_property(self, property):
        query = PropertyItem \
            .select(PropertyItem.timestamp) \
            .where(PropertyItem.property_id == property) \
            .group_by(PropertyItem.timestamp) \
            .order_by(PropertyItem.timestamp.desc()) \
            .limit(1)
        if not query.exists(): return []
        items = await self.fetch_property_by_time(property, query[0].timestamp)
        await self.update_with_names(property, items)
        return items
        
    async def fetch_diff_property(self, property):
        query = PropertyItem \
            .select(PropertyItem.timestamp) \
            .where(PropertyItem.property_id == property) \
            .group_by(PropertyItem.timestamp) \
            .order_by(PropertyItem.timestamp.desc()) \
            .limit(2)
        if not query.exists(): return []
        data = []
        for row in query:
            data.append(await self.fetch_property_by_time(property, row.timestamp))

        prev = {}
        if len(data) > 1: 
            for index, item in enumerate(data[1]):
                item.index = index
                prev[item.id] = item

        result = []
        for index, item in enumerate(data[0]):
            new_item = PropertyDiffDisplay(item)
            if item.id in prev:
                prev_item = prev[item.id]
                new_item.difference = prev_item.index - index
                new_item.previous = prev_item.timestamp
            result.append(new_item)
        
        await self.update_with_names(property, result)
        return result

class PropertyItem(Model):
    id = CharField()
    amount = IntegerField()
    property_id = CharField()
    timestamp = DateTimeField()

    class Meta:
        database = db

class PropertyName(Model):
    id = CharField()
    name = CharField()
    property_id = CharField()

    class Meta:
        database = db

class PropertyDisplay:
    index = 0
    def __init__(self, id, amount, property, name, timestamp):
        self.id = id
        self.amount = amount
        self.property_id = property
        self.name = name
        self.timestamp = timestamp

class PropertyDiffDisplay(PropertyDisplay):
    def __init__(self, item: PropertyDisplay, diff = 0, previous = None):
        self.id = item.id
        self.amount = item.amount
        self.difference = diff
        self.property_id = item.property_id
        self.name = item.name
        self.current = item.timestamp
        self.previous = previous


class PropertyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PropertyDiffDisplay):
            return { 
                "id": obj.id, 
                "amount": obj.amount,
                "difference": obj.difference,
              #  "property_id": obj.property_id,
                "name": obj.name,
                "current": obj.current,
                "previous": obj.previous,
            }
        if isinstance(obj, PropertyDisplay):
            return { 
                "id": obj.id, 
                "amount": obj.amount,
              #  "property_id": obj.property_id,
                "name": obj.name,
                "timestamp": obj.timestamp,
            }
        return JSONEncoder.default(self, obj)