import time

import digitalocean
from digitalocean import SSHKey
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
        self.droplets = []
        self.ssh_key_store = {}

    def run(self, config) -> dict:
        self.setup(config)
        print(f'Hello {self.manager.get_account()}!')
        # droplets = []
        # self.resolve_ssh_keys()
        # self.resolve_instance_names()
        # for instance_def in self.config["instances"]:
        #     self.droplets.append(self.create_droplet(instance_def))
        # self.wait_droplet_creation_process(self.droplets)
        ips = {}
        # for droplet in self.droplets:
        for droplet in self.manager.get_all_droplets():
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
        keys = [self.ssh_key_store[ssh_key_name] for ssh_key_name in instance_def.get("ssh_keys")]
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
        self.compare_keys_with_do()
        self.ssh_key_store = {key.name: key for key in self.manager.get_all_sshkeys()}
        self.validate_instance_ssh_keys()

    def validate_instance_ssh_keys(self):
        for instance in self.config["instances"]:
            for ssh_key_name in instance.get("ssh_keys"):
                if ssh_key_name not in self.ssh_key_store.keys():
                    raise Exception(f'Key {ssh_key_name} is not found for {instance["name"]} instance')

    def compare_keys_with_do(self):
        do_ssh_keys_dict = {key.name: key.public_key for key in self.manager.get_all_sshkeys()}
        for key in self.config["keys"]:
            if key["name"] not in do_ssh_keys_dict.keys():
                self.add_key(key)
            else:
                if key["public_key"].strip() != do_ssh_keys_dict[key["name"]].strip():
                    print(type(key["public_key"]))
                    print(type(do_ssh_keys_dict[key["name"]]))
                    raise Exception('Key {} conflicts with DigitalOcean key!'.format(key["name"]))

    def rollback(self):
        for droplet in self.droplets:
            droplet.destroy()
            print(f'{droplet} has been destroyed.')

    def resolve_instance_names(self):
        all_droplets = self.manager.get_all_droplets()
        droplet_names = {droplet.name for droplet in all_droplets}
        for instance_def in self.config["instances"]:
            if instance_def["name"] in droplet_names:
                raise Exception(f'{instance_def["name"]} already exists!')

    def add_key(self, key):
        user_ssh_key = key["public_key"]
        key = SSHKey(token=self.access_token,
                     name=key["name"],
                     public_key=user_ssh_key.strip())
        key.create()

