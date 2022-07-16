import os
from motor.motor_asyncio import AsyncIOMotorClient


class DatabaseMongoDB:
    """database class Mongo DB."""
    def __init__(self, conn_str: str, database: str, collection: str):
        """Init method for DatabaseMongoDB"""
        self.__client = AsyncIOMotorClient(conn_str)
        self.__db = self.__client[database]
        self.collection = self.__db[collection]

    async def get_all(self):
        cursor = self.collection.find({})
        results = [doc async for doc in cursor]
        results_count = await self.collection.count_documents({})
        return {
            'docs': results,
            'count': results_count
        }

    async def get_by_type(self, invoice_type: dict):
        cursor = self.collection.find({'invoice_type': invoice_type})
        results = [doc async for doc in cursor]
        results_count = await self.collection.count_documents({'invoice_type': invoice_type})
        return {
            'docs': results,
            'count': results_count
        }

    async def insert_one(self, document: dict):
        result = await self.collection.insert_one(document)
        return result

    async def delete_one(self, key: dict):
        result = await self.collection.delete_one(key)
        return result


invoices_mongodb = DatabaseMongoDB(conn_str=f"mongodb+srv://weichner:{os.getenv('database_password')}@cluster0.otcu4ll.mongodb.net/?retryWrites=true&w=majority",
                                   database="invoice_database",
                                   collection='invoices')

