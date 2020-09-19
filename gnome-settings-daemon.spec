%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

Summary:	GNOME Settings Daemon
Name:		gnome-settings-daemon
Version:	3.38.0
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://www.gnome.org/
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:  pkgconfig(alsa)
BuildRequires:	pkgconfig(colord) >= 0.1.12
BuildRequires:	pkgconfig(dbus-1) >= 1.1.2
BuildRequires:	pkgconfig(dbus-glib-1) >= 0.74
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gcr-base-3)
BuildRequires:	pkgconfig(geoclue-2.0) >= 2.1.2
BuildRequires:	pkgconfig(geocode-glib-1.0) >= 3.10.0
BuildRequires:	pkgconfig(gio-2.0) >= 2.26.0
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.29.14
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.1.5
BuildRequires:	pkgconfig(gsettings-desktop-schemas) >= 3.3.0
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.3.4
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(gweather-3.0) >= 3.9.5
BuildRequires:	pkgconfig(ibus-1.0) >= 1.4.99.2012100
BuildRequires:	pkgconfig(kbproto)
BuildRequires:	pkgconfig(lcms2) >= 2.2
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(libgnomekbd) >= 2.91.1
BuildRequires:	pkgconfig(libgnomekbdui) >= 2.91.1
BuildRequires:	pkgconfig(libnm)
BuildRequires:  pkgconfig(mm-glib)
BuildRequires:	pkgconfig(libnotify) >= 0.7.3
BuildRequires:	pkgconfig(libpulse) >= 0.9.16
BuildRequires:	pkgconfig(libpulse-mainloop-glib) >= 0.9.16
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libwacom)
BuildRequires:	pkgconfig(libxklavier) >= 5.0
BuildRequires:	pkgconfig(nss) >= 3.11.2,
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.103
BuildRequires:	pkgconfig(systemd)
BuildRequires:  pkgconfig(udev)
BuildRequires:	pkgconfig(upower-glib) >= 0.9.1
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xorg-wacom)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	cups-devel
BuildRequires:	intltool
BuildRequires:	ldetect-lst
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext-devel
BuildRequires:	meson
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(com_err)
Requires:	system-config-printer-udev

Conflicts:	gnome-control-center < 2.21.90
Conflicts:	gnome-color-manager < 3.1.2-1
Conflicts:	gnome-power-manager < 3.1.90
# ovitters: GNOME 3.8+ does not support fallback mode (gnome-panel, etc)
Conflicts:	gnome-panel < 3.7.0

# For the media-keys 'plugin'.
# It handles extra keyboard buttons (Calculator, screenshot, shutdown, etc) as
# well as some keyboard bindings. The plugin calls these following programs
# explicitly (see plugins/media-keys/gsd-media-keys-manager.c)
#
# The plugin can be disabled per user; so if user wants really minimal
# functionality, they can disable the plugin using gsettings. As such, putting
# these programs as Suggests instead of Requires
Recommends:	gcalctool
Recommends:	gnome-power-manager
Recommends:	gnome-screenshot
Recommends:	gnome-session
# XXX - also wants one of:
# 1. tracker-needle.desktop (preferred)
# 2. gnome-search-tool.desktop (fallback)

# ibus support
Recommends:	ibus-gtk3
Recommends:	ibus-gtk


%description
GNOME settings daemon manages the configuration of the desktop in the
background.

%package devel
Summary:	Include files for the GNOME settings daemon
Group:		Development/GNOME and GTK+
Conflicts:	libgnome-window-settings-devel < 2.21.5

%description devel
Include files for the GNOME settings daemon

%prep
%setup -q
%autopatch -p1

%build
export CC=gcc
export CXX=g++
%meson
%meson_build

%install
%meson_install

#we don't want these
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang %{name} --with-gnome --all-name

%pre
if [ -d %{_libexecdir}/%{name} ]
  then rm -rf %{_libexecdir}/%{name}
fi

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS
%dir %{_libdir}/gnome-settings-daemon-3.0

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.power.gschema.xml

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.housekeeping.gschema.xml

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.media-keys.gschema.xml


%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.wacom.gschema.xml

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.sharing.gschema.xml

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.xsettings.gschema.xml

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.color.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/libgsd.so

%{_libexecdir}/gsd-a11y-settings
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.A11ySettings.desktop

%{_libexecdir}/gsd-color
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Color.desktop

%{_libexecdir}/gsd-datetime
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Datetime.desktop

%{_libexecdir}/gsd-dummy

%{_libexecdir}/gsd-housekeeping
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Housekeeping.desktop

%{_libexecdir}/gsd-keyboard
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Keyboard.desktop

%{_libexecdir}/gsd-media-keys
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.MediaKeys.desktop

%{_libexecdir}/gsd-power
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Power.desktop

%{_libexecdir}/gsd-print-notifications
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.PrintNotifications.desktop

%{_libexecdir}/gsd-rfkill
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Rfkill.desktop

%{_libexecdir}/gsd-screensaver-proxy
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.ScreensaverProxy.desktop

%{_libexecdir}/gsd-sharing
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Sharing.desktop

%{_libexecdir}/gsd-smartcard
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Smartcard.desktop

%{_libexecdir}/gsd-sound
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Sound.desktop

%{_libexecdir}/gsd-wacom
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Wacom.desktop

%{_libexecdir}/gsd-xsettings
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.XSettings.desktop

%{_libexecdir}/gsd-backlight-helper
%{_libexecdir}/gsd-printer
%{_libexecdir}/gsd-wacom-led-helper
%{_libexecdir}/gsd-wacom-oled-helper
%{_libexecdir}/gsd-wwan
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Wwan.desktop
%{_libexecdir}/gsd-usb-protection
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.UsbProtection.desktop
%{_sysconfdir}/xdg/Xwayland-session.d/00-xrdb

%{_datadir}/gnome-settings-daemon/

/lib/udev/rules.d/61-gnome-settings-daemon-rfkill.rules

%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.power.policy
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.wacom.policy

%{_datadir}/GConf/gsettings/gnome-settings-daemon.convert

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.wwan.gschema.xml

%_userunitdir/*.service
%_userunitdir/*.target
%_userunitdir/gnome-session-initialized.target.wants/*.target
%_userunitdir/gnome-session-x11-services.target.wants/gsd-xsettings.target

%files devel
%{_includedir}/gnome-settings-daemon-3.0
%{_libdir}/pkgconfig/gnome-settings-daemon.pc
