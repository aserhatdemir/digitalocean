import time
import digitalocean


class DigitalOcean:
    def __init__(self, access_token):
        self.access_token = access_token
        self.manager = digitalocean.Manager(token=self.access_token)
        print(f'Hello {self.manager.get_account()}!')

    def get_region(self, city):  # 'Frankfurt'
        all_regions = self.manager.get_all_regions()
        for region in all_regions:
            if city in region.name:
                if region.available:
                    return region.slug
        return None

    def create_droplet(self, name, region, tag):
        keys = self.manager.get_all_sshkeys()
        print(keys)
        # region = self.get_region(city)
        droplet = digitalocean.Droplet(token=self.access_token,
                                       name=name,
                                       region=region,
                                       image='ubuntu-18-04-x64',
                                       size='s-1vcpu-1gb',
                                       tags=[tag],
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

    def wait_droplet_creation_process(self, tag):
        droplets = self.manager.get_all_droplets(tag_name=tag)
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


def do_play():
    do = DigitalOcean("2c5f9bb27de129cba4f3b83d3ca08632bcbdc3c450c475b41334bb8f439ccb61")
    # ----
    # for i in range(3):
    #     do.create_droplet(f'node-{i}', 'fra1', 'do-python')
    # do.wait_droplet_creation_process('do-python')
    # ----
    # do.destroy_droplets('do-python')
    # ----
    drops = do.manager.get_all_droplets(tag_name='do-python')
    for drop in drops:
        print(drop.status)
    keys = do.manager.get_all_sshkeys()
    for key in keys:
        print(key.public_key)


if __name__ == '__main__':
    do_play()
