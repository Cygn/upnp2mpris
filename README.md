# upnp2mpris
This a wrapper for UPNP/DLNA renderers in your network to appear as MPRIS2 compatible DBus objects. You can then use most mediacontroller desktop widgets as remotes.
You can for example control a remote KODI instance from your desktop. If you are using Gnome3 media share feautre, it may also provide a controlpoint for Rygel. 

Tested with gnome-shell-extension-mediaplayer, plasma widget and it even works with KDE-Connect from a smartphone.

It uses dleyna-renderer implementation so it's limited on what's available on dleyna. Unfortunatley it doesn't cover all MPRIS dbus specification. 
Obviously dleyna-renderer-service is needed.



