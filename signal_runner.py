import subprocess
import threading

from pathlib import Path

class SignalRunner:

    STATE_UNKNOWN = -1
    STATE_DISCONNECTED = 0
    STATE_CONNECTED = 1

    def __init__(self, debounce_sec, display_name, cwd=Path.home()):
        self.timer = None
        self.debounce_sec = debounce_sec
        self.display_name = display_name
        self.cwd = cwd

        self.connect_scripts = []
        self.disconnect_scripts = []

        # TODO: The first state change after the script starts will always cause
        #       scripts to run even if it's unnecessary. If the script knew how
        #       to query the display connection state on startup it would
        #       avoid this.
        self.last_state = self.STATE_UNKNOWN
    
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
        new_state = None
        if display_dict['connected']:
            print(f'>>> {self.display_name} connected')
            script_paths = self.connect_scripts
            new_state = self.STATE_CONNECTED
        else:
            print(f'>>> {self.display_name} disconnected')
            script_paths = self.disconnect_scripts
            new_state = self.STATE_DISCONNECTED

        if new_state != self.last_state:
            for fpath in script_paths:
                print(f'    running {fpath}')
                subprocess.run(fpath, shell=True, cwd=self.cwd)
            self.last_state = new_state