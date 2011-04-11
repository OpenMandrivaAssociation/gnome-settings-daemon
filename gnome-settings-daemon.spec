Summary: GNOME Settings Daemon
Name: gnome-settings-daemon
Version: 2.32.1
Release: %mkrel 2
License: GPLv2+
Group: Graphical desktop/GNOME
BuildRequires:	gtk+2-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:  libxklavier-devel >= 5.0
BuildRequires:  libxxf86misc-devel
BuildRequires:  libgstreamer-plugins-base-devel
BuildRequires:  libxscrnsaver-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	libgnomekbd-devel >= 2.31.2
BuildRequires:	libnotify-devel
BuildRequires:	scrollkeeper
BuildRequires:	intltool
BuildRequires:  pulseaudio-devel
BuildRequires:  libcanberra-gtk-devel
BuildRequires:  polkit-1-devel
BuildRequires:  libnss-devel
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Patch0: gnome-settings-daemon-2.32.1-libnotify0.7.patch
# (fc) 2.23.6-2mdv don't use X server dpi by default, use 96 instead, should work better with very small screens
Patch3:		gnome-settings-daemon-2.23.6-dpi.patch
# (cg) 2.26.0-2mdv Fedora patches for touchpad support
Patch4: gnome-settings-daemon-2.28.0-fix-touchpad.patch
Patch6: gnome-settings-daemon-2.27.4-touchpad-defaults.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.gnome.org/

Conflicts: gnome-control-center < 2.21.90
Requires: libgnome2-schemas

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
%patch0 -p1 -b .libnotify
%patch3 -p1 -b .dpi
%patch4 -p1 -b .touchpad-fix
%patch6 -p1 -b .touchpad-edgescroll

%build
%configure2_5x --disable-schemas-install
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std
 xmldir=%buildroot%_datadir/gnome-control-center/keybindings

%{find_lang} %name-2.0 --with-gnome --all-name

rm -f %buildroot%_libdir/%name-2.0/*a

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -d %{_libexecdir}/%name ]
  then rm -rf %{_libexecdir}/%name 
fi

%post
%define schemas apps_gnome_settings_daemon_keybindings apps_gnome_settings_daemon_housekeeping desktop_gnome_font_rendering desktop_gnome_keybindings desktop_gnome_peripherals_smartcard desktop_gnome_peripherals_touchpad gnome-settings-daemon apps_gnome_settings_daemon_xrandr
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
%{_sysconfdir}/gconf/schemas/desktop_gnome_peripherals_smartcard.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_peripherals_touchpad.schemas
%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas
%_sysconfdir/dbus-1/system.d/org.gnome.SettingsDaemon.DateTimeMechanism.conf
%_datadir/gnome-control-center/keybindings/50-accessibility.xml
%_datadir/%name
%_datadir/icons/hicolor/*/actions/*
%_datadir/icons/hicolor/*/apps/*
%{_libexecdir}/%name
%{_libexecdir}/gsd-locate-pointer
%{_libexecdir}/gsd-datetime-mechanism
%dir %{_libdir}/%name-2.0
%{_libdir}/%name-2.0/*.so
%{_libdir}/%name-2.0/a11y-keyboard.gnome-settings-plugin
%{_libdir}/%name-2.0/background.gnome-settings-plugin
%{_libdir}/%name-2.0/clipboard.gnome-settings-plugin
%{_libdir}/%name-2.0/font.gnome-settings-plugin
%{_libdir}/%name-2.0/housekeeping.gnome-settings-plugin
%{_libdir}/%name-2.0/keybindings.gnome-settings-plugin
%{_libdir}/%name-2.0/keyboard.gnome-settings-plugin
%{_libdir}/%name-2.0/media-keys.gnome-settings-plugin
%{_libdir}/%name-2.0/mouse.gnome-settings-plugin
%{_libdir}/%name-2.0/smartcard.gnome-settings-plugin
%{_libdir}/%name-2.0/sound.gnome-settings-plugin
%{_libdir}/%name-2.0/typing-break.gnome-settings-plugin
%{_libdir}/%name-2.0/xrandr.gnome-settings-plugin
%{_libdir}/%name-2.0/xrdb.gnome-settings-plugin
%{_libdir}/%name-2.0/xsettings.gnome-settings-plugin
%_datadir/dbus-1/services/*
%_datadir/dbus-1/system-services/*
%_datadir/polkit-1/actions/org.gnome.settingsdaemon.datetimemechanism.policy

%files devel
%defattr(-, root, root)
%doc ChangeLog
%{_includedir}/*
%{_libdir}/pkgconfig/*

