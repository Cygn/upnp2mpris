Name:           upnp2mpris
Version:        1.0
Release:        1
Summary:        a wrapper for UPNP/DLNA renderers in your local network to appear as MPRIS2 compatible DBus objects.

Group:          script
BuildArch:      noarch
License:        GPLv3
URL:            https://github.com/cygn/pdfshrink.git
Source0:        upnp2mpris-1.0.tar.gz
Vendor:         Sinan H <sinan@haliyo.net>
Packager:       Sinan H <sinan@haliyo.net>

Requires: 	    dleyna-renderer

Summary:         A wrapper for UPNP/DLNA renderers in your local network to appear as MPRIS2 compatible DBus objects.

%description
This a wrapper for **UPNP/DLNA** renderers in your local network to appear as **MPRIS2** compatible DBus objects. You can then use most mediacontroller desktop widgets as remotes.
You can for example control a *KODI* instance runing on a *RPi* from your desktop. It may also provide a control point for *Rygel* if you are using Gnome3 media share feature. 

It uses *dleyna-renderer* dbus implementation so its interface is limited to which controls it makes available, which unfortunately doesn't cover all MPRIS2 DBus specification. 

There is nothing to configure. If your device is visible in the network, **upnp2mpris** will pick it up.

### known issues
- dleyna-renderer-server sometimes hangs. you'll have to kill -9 it.
- Multiple renderer discovery doesn't work



%prep
%setup -q
%build
%install
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin/
install -m 0755 upnp2mpris.py $RPM_BUILD_ROOT/usr/bin/upnp2mpris

%files
/usr/bin/upnp2mpris
%doc README.md
%license LICENSE

%changelog
* Wed Jan 20 2021 Sinan H  1.0.0
  - Initial rpm release

