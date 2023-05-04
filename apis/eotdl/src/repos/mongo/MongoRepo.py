from .client import get_db
from bson.objectid import ObjectId
from datetime import datetime, timedelta, time

class MongoRepo():

    def __init__(self):
        self.db = get_db()

    def exists(self, collection, id):
        return self.db[collection].find_one({'_id': ObjectId(id)}) is not None

    def generate_id(self):
        return str(ObjectId())

    def persist(self, collection, data, id=None):
        if id is not None: 
            data['_id'] = ObjectId(id)
            return self.db[collection].insert_one(data)
        return self.db[collection].insert_one(data).inserted_id

    def retrieve(self, collection, value=None, field='id', limit=None, sort=None, order=None):
        if value is None:
            query = self.db[collection].find() # TODO: find_many if field is provided
            if sort is not None: query = query.sort(sort, order)
            if limit is not None: query = query.limit(limit)
            return list(query)
        if field == '_id': value = ObjectId(value)
        query = self.db[collection].find_one({field: value})
        return query
    
    def retrieve_many(self, collection, values, field='id'):
        if field == '_id':
            values = [ObjectId(value) for value in values]
        return list(self.db[collection].find({field: {'$in': values}}))

    def update(self, collection, id, data):
        return self.db[collection].update_one({'_id': ObjectId(id)}, {'$set': data})

    def delete(self, collection, id):
        return self.db[collection].delete_one({'_id': ObjectId(id)})

    def retrieve_all(self, collection):
        return list(self.db[collection].find())
    
    def find_one_by_field(self, collection, field, value, limit):
        if limit is None:
            return self.db[collection].find_one({field: value})
        return self.db[collection].find_one({field: value}).limit(limit)
    
    def find_one_by_name(self, collection, name, limit=None):
        return self.find_one_by_field(collection, 'name', name, limit)
    
    def increase_counter(self, collection, field1, value1, field2, value2=1):
        if field1 == '_id':
            value1 = ObjectId(value1)
        return self.db[collection].update_one({field1: value1}, {'$inc': {field2: value2}})
    
    def find_in_time_range(self, collection, uid, value, field="type", t0=datetime.combine(datetime.today(), time.min), dt=timedelta(days=1)):
        return list(self.db[collection].find({
            'uid': uid,
            field: value,
            'timestamp': {'$gte': t0, '$lt': t0 + dt}
        }))
    
    def find_top(self, collection, field, n=None):
        query = self.db[collection].find().sort(field, -1)
        if n is not None: return list(query.limit(n))
        return list(query)
    
    def append_to_list(self, collection, field1, value1, field2, value2):
        if field1 == '_id':
            value1 = ObjectId(value1)
        return self.db[collection].update_one({field1: value1}, {'$push': {field2: value2}})
    
    def remove_from_list(self, collection, field1, value1, field2, value2):
        if field1 == '_id':
            value1 = ObjectId(value1)
        return self.db[collection].update_one({field1: value1}, {'$pull': {field2: value2}})