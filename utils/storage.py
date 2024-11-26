import os
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
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

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
        StorageManager.__init__(self, "logs/requests_log.json")

# Log some requests
class ClassificationsStorageManager(StorageManager):
    def __init__(self):
        StorageManager.__init__(self, "logs/classifications.json")

    def get_unclassified_logs(self):
        classifications = self.get_all()

        return [c["request"] for c in classifications if c["is_safe"] is None]

