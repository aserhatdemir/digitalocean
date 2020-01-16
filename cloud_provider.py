import time

import digitalocean
from digitalocean.baseapi import NotFoundError


class CloudProvider:
    def __init__(self):
        self.config = None

    def run(self, config) -> dict:
        pass


class DigitalOceanCloudProvider(CloudProvider):

    def __init__(self):
        super().__init__()
        self.access_token = None
        self.manager = None
        self.regions = {}
        self.ssh_keys = None

    def run(self, config) -> dict:
        self.setup(config)
        print(f'Hello {self.manager.get_account()}!')
        droplets = []
        self.resolve_ssh_keys()
        for instance_def in self.config["instances"]:
            droplets.append(self.create_droplet(instance_def))
        self.wait_droplet_creation_process(droplets)
        ips = {}
        for droplet in droplets:
            ips[droplet.name] = droplet.ip_address
        return ips

    def setup(self, config):
        self.config = config
        self.access_token = self.config["settings"]["api_token"]
        self.manager = digitalocean.Manager(token=self.access_token)

    def get_region(self, city):  # 'Frankfurt'
        if city in self.regions.keys():
            return self.regions[city]
        all_regions = self.manager.get_all_regions()
        for region in all_regions:
            if city in region.name:
                if region.available:
                    self.regions[city] = region.slug
                    return region.slug
        raise Exception(f'Region: {city} is not available!')

    def create_droplet(self, instance_def):
        region = self.get_region(instance_def["region"])
        keys = self.get_ssh_keys(instance_def["ssh_keys"])
        droplet = digitalocean.Droplet(token=self.access_token,
                                       name=instance_def["name"],
                                       region=region,
                                       image='ubuntu-18-04-x64',
                                       size=instance_def["size"],
                                       tags=instance_def["tags"],
                                       ssh_keys=keys,
                                       backups=False)
        droplet.create()
        print(f'{droplet.name} is created!')
        return droplet

    def destroy_droplets(self, tag):
        droplets = self.manager.get_all_droplets(tag_name=tag)
        for droplet in droplets:
            droplet.destroy()
            print(f'{droplet} has been destroyed.')

    def wait_droplet_creation_process(self, droplets):
        for droplet in droplets:
            actions = droplet.get_actions()
            for action in actions:
                while True:
                    action.load()
                    if action.status == 'completed':
                        print(f'{droplet} creation is {action.status}!')
                        break
                    else:
                        print(f'{droplet} creation is {action.status}!')
                        time.sleep(1)

    def resolve_ssh_keys(self):
        # keys = self.manager.get_all_sshkeys()
        pass

    def get_ssh_keys(self, ssh_key_names):
        return [self.get_ssh_key(ssh_key_name) for ssh_key_name in ssh_key_names]

    def get_ssh_key(self, ssh_key_name):
        if self.ssh_keys is None:
            self.ssh_keys = self.manager.get_all_sshkeys()
        for ssh_key in self.ssh_keys:
            if ssh_key.name == ssh_key_name:
                return ssh_key
        raise Exception(f'{ssh_key_name} not found in ssh keys')

    def rollback(self):
        pass
