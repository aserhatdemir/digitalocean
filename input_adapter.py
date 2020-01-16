import json


class InputAdepter:
    def __init__(self, **kwargs):
        pass

    def read(self) -> dict:
        pass


class FileInputAdapter(InputAdepter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_name = kwargs['file_name']

    def read(self, **kwargs) -> dict:
        with open(self.file_name, 'r') as f:
            return json.load(f)
