from cloud_provider import DigitalOceanCloudProvider
from input_adapter import FileInputAdapter
from shell_executor import ShellExecutor


class ApplicationController:

    def __init__(self, input_adapter, cloud_provider, shell_executor):
        self.input_adapter = input_adapter
        self.cloud_provider = cloud_provider
        self.shell_executor = shell_executor

    def run(self):
        config = self.input_adapter.read()
        print(config)
        ips = self.cloud_provider.run(config)
        self.shell_executor.run(config, ips)


ApplicationController(input_adapter=FileInputAdapter(file_name="input.json"),
                      cloud_provider=DigitalOceanCloudProvider(),
                      shell_executor=ShellExecutor()
                      ).run()
