#!/usr/bin/env python
import dbus
import signal
import sys

from dbus.mainloop.pyqt5 import DBusQtMainLoop
from PyQt5.QtCore import QCoreApplication

from config_loader import load_config
from signal_runner import SignalRunner

def main():
    # TODO: find a cleaner way of shutting down
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    config = load_config()
    debounce_sec = config['debounce']
    display_name = config['display_name']
    script_working_dir = config['_script_working_dir']
    dbus_interface_name = config['_dbus']['interface_name']
    dbus_path = config['_dbus']['path']
    dbus_signal_name = config['_dbus']['signal_name']
    connect_scripts = config['on_connect']
    disconnect_scripts = config['on_disconnect']

    app = QCoreApplication(sys.argv)
    loop = DBusQtMainLoop(set_as_default=True)
    bus = dbus.SessionBus()

    signal_runner = SignalRunner(debounce_sec, display_name, cwd=script_working_dir)
    for script in connect_scripts:
        signal_runner.add_connect_script(script)
    for script in disconnect_scripts:
        signal_runner.add_disconnect_script(script)

    bus.add_signal_receiver(
        handler_function=signal_runner.run,
        dbus_interface=dbus_interface_name,
        path=dbus_path,
        signal_name=dbus_signal_name
    )

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
