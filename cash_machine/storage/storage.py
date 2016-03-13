from storage_memory import StorageMemory


class Storage(object):
    def __init__(self):
        self.engine = StorageMemory()

    def get(self, table, code):
        return self.engine.get(table, code)

    def set(self, table, code, name, value):
        return self.engine.set(table, code, name, value)

    def get_all(self, table):
        return self.engine.get_all(table)

storage = Storage()
