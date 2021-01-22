# upnp2mpris
This a wrapper for **UPNP / DLNA** renderers in your local network to appear as **MPRIS2** compatible DBus objects. You can then use most mediacontroller desktop widgets as remotes.
You can for example control a *KODI* instance runing on a *RPi* from your desktop. It may also provide a control point for *Rygel* if you are using Gnome3 media share feature. 

Tested with gnome-shell _Mpris Indicator Button_ extension and it also works with *KDE-Connect* from a smartphone!


It uses *dleyna-renderer* dbus implementation so its interface is limited to which controls it makes available, which unfortunately doesn't cover all MPRIS2 DBus specification. ATM, only play/pause, next/previous and volume control are available.
Obviously **dleyna-renderer-service** is needed.

There is nothing to configure. If your device is visible in the network **upnp2mpris** will pick it up.

### known issues
- dleyna-renderer-server sometimes hangs. you'll have to kill -9 it.
- Multiple renderer discovery doesn't work





