import subprocess
import threading

from pathlib import Path

class SignalRunner:

    def __init__(self, debounce_sec, display_name, cwd=Path.home()):
        self.timer = None
        self.debounce_sec = debounce_sec
        self.display_name = display_name
        self.cwd = cwd

        self.connect_scripts = []
        self.disconnect_scripts = []
    
    def add_connect_script(self, path):
        self.connect_scripts.append(path)

    def add_disconnect_script(self, path):
        self.disconnect_scripts.append(path)

    def run(self, *args):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.debounce_sec, self.__inner_run, args=args)
        self.timer.start()

    def __inner_run(self, *args):
        if self.timer:
            self.timer.cancel()
        self.timer = None

        kscreen_dict = args[0]
        find_display = (o for o in kscreen_dict['outputs'] if o['name'] == self.display_name)
        display_dict = next(find_display)

        script_paths = None
        if display_dict['connected']:
            print(f'>>> {self.display_name} connected')
            script_paths = self.connect_scripts
        else:
            print(f'>>> {self.display_name} disconnected')
            script_paths = self.disconnect_scripts

        for fpath in script_paths:
            print(f'    running {fpath}')
            subprocess.run(fpath, shell=True, cwd=self.cwd)