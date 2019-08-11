# kscreen-listener

This is a script meant to run other scripts automatically when I dock/undock my laptop. It listens to D-Bus messages sent by Plasma's KScreen service when there are display connection state changes. It also supports debouncing because my setup is noisy and likes to broadcast a disconnect/reconnect when my monitor comes out of power save mode.

## Dependencies
- python 3
- PyQt 5
- dbus-python

## Config
- Create a directory at `~/.config/kscreen-listener-scripts/`. Scripts specified in the config file are assumed to be here.
- Copy the `kscreen-listenerrc.example` file to `~/.config/kscreen-listenerrc` and edit it appropriately (it's YAML).

## Disabling KScreen Display Management
KScreen can be disabled in Plasma, and it will stop managing resolution changes but still send the D-Bus messages that this script needs. If this sounds desirable, do the following:
- Go to System Settings > Background Services
- Uncheck/stop KScreen 2 in the Startup Services list