from do import DigitalOcean

import argparse


def do_play(token):
    do = DigitalOcean(token)
    # ----
    # for i in range(3):
    #     do.create_droplet(f'node-{i}', 'fra1', 'do-python')
    # do.wait_droplet_creation_process('do-python')
    # ----
    do.destroy_droplets('do-python')
    # ----
    drops = do.manager.get_all_droplets(tag_name='do-python')
    for drop in drops:
        print(drop.status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-token')
    args = parser.parse_args()
    do_play(args.token)
