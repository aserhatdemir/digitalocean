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
        config = self.parse(self.file_name)
        self.load_pub_keys(config)
        return config

    def parse(self, file_name) -> dict:
        with open(file_name, 'r') as f:
            return json.load(f)

    def load_pub_keys(self, config):
        for key in config["keys"]:
            with open(key["public_key"], 'r') as f:
                public_key = f.read()
                key["public_key"] = public_key

