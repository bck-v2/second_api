import json
from pyramid.renderers import JSON
from datetime import datetime

class JSONRenderer(JSON):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_adapter(datetime, self.datetime_adapter)

    @staticmethod
    def datetime_adapter(obj, request=None):
        return obj.isoformat()  # Mengonversi datetime menjadi ISO format string