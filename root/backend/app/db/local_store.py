from repository import RepositoryBase


class LocalBrowserStore(RepositoryBase):
    def __init__(self):
        self.mem = {"medications": [], "schedules": [], "doses": []}

    async def insert(self, collection, data):
        self.mem[collection].append(data)
        return data["id"]

    async def find(self, collection, query):
        return [item for item in self.mem[collection]
                if all(item.get(k) == v for k, v in query.items())]

    async def update(self, collection, query, data):
        for item in self.mem[collection]:
            if all(item.get(k) == v for k, v in query.items()):
                item.update(data)
