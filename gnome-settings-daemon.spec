# disable underlinking, it doesn't work well with plugins
%define _disable_ld_no_undefined 1

Summary: GNOME Settings Daemon
Name: gnome-settings-daemon
Version: 2.27.91
Release: %mkrel 1
License: GPLv2+
Group: Graphical desktop/GNOME
BuildRequires:	gnome-desktop-devel >= 2.25.3
BuildRequires:  libxklavier-devel >= 4.0
BuildRequires:  libxxf86misc-devel
BuildRequires:  libgstreamer-plugins-base-devel
BuildRequires:  libxscrnsaver-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	libgnomekbd-devel >= 2.21.4
BuildRequires:	libnotify-devel
BuildRequires:	scrollkeeper
BuildRequires:	intltool
BuildRequires:  pulseaudio-devel
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
# (fc) 2.23.6-2mdv don't use X server dpi by default, use 96 instead, should work better with very small screens
Patch3:		gnome-settings-daemon-2.23.6-dpi.patch
# (cg) 2.26.0-2mdv Fedora patches for touchpad support
Patch4: gnome-settings-daemon-2.24.0-fix-touchpad.patch
Patch6: gnome-settings-daemon-2.27.4-touchpad-defaults.patch

Requires: gstreamer0.10-plugins-base
Requires: gstreamer0.10-plugins-good
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.gnome.org/softwaremap/projects/control-center/

Requires: gnome-screensaver
Requires: gnome-desktop >= 2.23.2
Requires: gnome-themes
Requires: metacity
Suggests: mandriva-theme
Conflicts: gnome-control-center < 2.21.90

%description
GNOME settings daemon manages the configuration of the desktop in the
background.


%package devel
Summary:	Include files for the GNOME settings daemon
Group:		Development/GNOME and GTK+
Conflicts: libgnome-window-settings-devel < 2.21.5

%description devel
Include files for the GNOME settings daemon

%prep
%setup -q 
%patch3 -p1 -b .dpi
%patch4 -p1 -b .touchpad-fix
%patch6 -p1 -b .touchpad-edgescroll

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%{find_lang} %name-2.0 --with-gnome --all-name

rm -f %buildroot%_libdir/%name-2.0/*a

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -d %{_libexecdir}/%name ]
  then rm -rf %{_libexecdir}/%name 
fi

%post
%define schemas apps_gnome_settings_daemon_keybindings apps_gnome_settings_daemon_housekeeping desktop_gnome_font_rendering desktop_gnome_keybindings desktop_gnome_peripherals_touchpad gnome-settings-daemon apps_gnome_settings_daemon_xrandr
%post_install_gconf_schemas %schemas
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %schemas

%postun
%clean_icon_cache hicolor

%files -f %{name}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/xdg/autostart/gnome-settings-daemon.desktop
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_housekeeping.schemas
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_xrandr.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_keybindings.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_peripherals_touchpad.schemas
%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas
%_datadir/gnome-control-center/keybindings/50-accessibility.xml
%_datadir/%name
%_datadir/icons/hicolor/*/apps/*
%{_libexecdir}/%name
%dir %{_libdir}/%name-2.0
%{_libdir}/%name-2.0/*.so
%{_libdir}/%name-2.0/a11y-keyboard.gnome-settings-plugin
%{_libdir}/%name-2.0/background.gnome-settings-plugin
%{_libdir}/%name-2.0/clipboard.gnome-settings-plugin
%{_libdir}/%name-2.0/dummy.gnome-settings-plugin
%{_libdir}/%name-2.0/font.gnome-settings-plugin
%{_libdir}/%name-2.0/housekeeping.gnome-settings-plugin
%{_libdir}/%name-2.0/keybindings.gnome-settings-plugin
%{_libdir}/%name-2.0/keyboard.gnome-settings-plugin
%{_libdir}/%name-2.0/media-keys.gnome-settings-plugin
%{_libdir}/%name-2.0/mouse.gnome-settings-plugin
%{_libdir}/%name-2.0/sound.gnome-settings-plugin
%{_libdir}/%name-2.0/typing-break.gnome-settings-plugin
%{_libdir}/%name-2.0/xrandr.gnome-settings-plugin
%{_libdir}/%name-2.0/xrdb.gnome-settings-plugin
%{_libdir}/%name-2.0/xsettings.gnome-settings-plugin
%_datadir/dbus-1/services/*

%files devel
%defattr(-, root, root)
%doc ChangeLog
%{_includedir}/*
%{_libdir}/pkgconfig/*

