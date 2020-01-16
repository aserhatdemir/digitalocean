class ShellExecutor:
    def run(self, config, ips):
        # fetch script files
        for setup in config['setup']:
            for node in setup['nodes']:
                for script in setup['scripts']:
                    self.run_script(node, script, ips)

    def run_script(self, node, script, ips):
        pass
