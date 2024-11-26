import json

class StorageManager:
    def __init__(self, filepath):
        self.filepath = filepath

    def _load_data(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_data(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f)

    def get_all(self):
        return self._load_data()

    def save(self, item):
        data = self.get_all()
        data.append(item)
        self._save_data(data)

        return item

# Log al incomming
class RequestsStorageManager(StorageManager):
    def __init__(self):
        StorageManager.__init__(self, "../logs/requests_log.json")

# Log some requests
class ClassificationsStorageManager(StorageManager):
    def __init__(self):
        StorageManager.__init__(self, "../logs/classifications.json")

    def get_unclassified_logs(self):
        classifications = self.get_all()
        unclassified_requests = {
            json.dumps(c["request"], sort_keys=True) 
            for c in classifications if c.get("is_safe") is None
        }
    
        return [
            log for log in self.get_all()
            if json.dumps(log, sort_keys=True) in unclassified_requests
        ]

