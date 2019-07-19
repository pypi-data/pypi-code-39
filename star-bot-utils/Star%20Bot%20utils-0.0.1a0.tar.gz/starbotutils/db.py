from pymongo import MongoClient

class DataBase(MongoClient):
    def __init__(self, connection="mongodb://localhost:27017/", **kwargs):
        super().__init__(connection, **kwargs)
       
    def get(self, db, col, q={}):
        return self[db][col].find_many(q)

    def delete(self, db, col, q, many=True):
        if many:
            return self[db][col].delete_many(q)
        return self[db][col].delete_one(q)

    def update(self, db, col, data):
        self[db][col].insert_one(data)
        return

    def list(self,db=None):
        if db is None:
            return self.list_database_names()
        return self[db].list_collection_names()

    def drop(self, db, col):
        return self[db][col].drop()
