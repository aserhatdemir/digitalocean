import os


class ShellExecutor:
    def run(self, config, ips):
        node_ssh_key_names_store = {instance["name"]: instance["ssh_keys"] for instance in config["instances"]}
        node_ssh_key_path_store = {ssh_key["name"]: ssh_key["private_key"] for ssh_key in config["keys"]}
        script_name_file_store = {script["name"]: script["file"] for script in config["scripts"]}
        # fetch script files
        for setup in config['setup']:
            for node_name in setup['nodes']:
                node_ssh_key_name = node_ssh_key_names_store[node_name][0]
                private_key = node_ssh_key_path_store[node_ssh_key_name]
                print(ips)
                ip = ips[node_name]
                for script_name in setup['scripts']:
                    script = script_name_file_store[script_name]
                    self.run_script(private_key, script, ip)

    def run_script(self, private_key, script, ip):
        command = f"ssh root@{ip} -o StrictHostKeyChecking=no -i {private_key} 'bash -s' < {script}"
        print(command)
        os.system(command)

# ssh root@MachineB 'bash -s' < local_script.sh
# -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no