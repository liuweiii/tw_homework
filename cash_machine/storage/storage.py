from storage_memory import StorageMemory


class Storage(object):
    def __init__(self):
        self.engine = StorageMemory()

    def get(self, table, code):
        return self.engine.get(table, code)

storage = Storage()
