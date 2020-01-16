from do import DigitalOcean

import argparse
import json


def do_play(token):
    do = DigitalOcean(token)
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


def parse_input(file):
    with open(file, 'r') as f:
        config = json.load(f)
    print(config["instances"])
    print(config["setup"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-token')
    args = parser.parse_args()
    # parse_input(args.file)
    do_play(args.token)
