import os
import yaml

from pathlib import Path

DEFAULT_CONFIG = {
    'debounce': 5.0,

    'display_name': 'DP1',

    'on_connect': [],
    'on_disconnect': []
}

PRIVATE_CONFIG = {
    '_rc_path': f'{Path.home()}/.config/kscreen-listenerrc',

    '_script_dir': f'{Path.home()}/.config/kscreen-listener-scripts',
    '_script_working_dir': Path.home(),
    
    '_dbus': {
        'interface_name': 'org.kde.kscreen.Backend',
        'path': '/backend',
        'signal_name': 'configChanged'
    }
}

def load_config():
    # TODO: should probably auto-create the config file and scripts directory
    #       if necessary
    
    config = DEFAULT_CONFIG.copy()
    config = {**config, **yaml.safe_load(open(PRIVATE_CONFIG['_rc_path']))}
    config = {**config, **PRIVATE_CONFIG}

    if not os.path.isdir(config['_script_dir']):
        raise RuntimeError(f'{config["_script_dir"]} directory does not exist')

    prepend_dir = lambda fname: f'{config["_script_dir"]}/{fname}'
    config['on_connect'] = list(map(prepend_dir, config['on_connect']))
    config['on_disconnect'] = list(map(prepend_dir, config['on_disconnect']))

    for fpath in (config['on_connect'] + config['on_disconnect']):
        if not os.path.exists(fpath):
            raise RuntimeError(f'{fpath} script does not exist')

    return config
