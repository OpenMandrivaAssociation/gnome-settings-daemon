Summary: GNOME Settings Daemon
Name: gnome-settings-daemon
Version: 2.22.1
Release: %mkrel 2
License: GPL
Group: Graphical desktop/GNOME
BuildRequires:	gnome-desktop-devel >= 2.21.4
BuildRequires:	libgnomeui2-devel
BuildRequires:	libglade2.0-devel
BuildRequires:  libxklavier-devel >= 3.3
BuildRequires:  libxxf86misc-devel
BuildRequires:  libgstreamer-plugins-base-devel
BuildRequires:  libxscrnsaver-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	libgnomekbd-devel >= 2.21.4
BuildRequires:  perl-XML-Parser
BuildRequires:	scrollkeeper
BuildRequires:	intltool
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
# (fc) 2.22.1-2mdv apply background even if nautilus is enabled (GNOME bug #531487)
Patch0:	gnome-settings-daemon-2.22.1-applybackground.patch
# (fc) 2.22.1-2mdv don't apply background when it is disabled 
Patch1: gnome-settings-daemon-2.22.1-disablebackground.patch
Requires: gstreamer0.10-plugins-base
Requires: gstreamer0.10-plugins-good
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.gnome.org/softwaremap/projects/control-center/

Requires: gnome-screensaver
Requires: gnome-desktop >= 2.1.4
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
%patch0 -p1 -b .applybackground
%patch1 -p1 -b .disablebackground

%build
%configure2_5x --enable-gstreamer=0.10 --disable-esd
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
%define schemas apps_gnome_settings_daemon_keybindings apps_gnome_settings_daemon_screensaver desktop_gnome_font_rendering gnome-settings-daemon
%post_install_gconf_schemas %schemas

%preun
%preun_uninstall_gconf_schemas %schemas



%files -f %{name}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_screensaver.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas
%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas
%_datadir/%name
%{_libexecdir}/%name
%dir %{_libdir}/%name-2.0
%{_libdir}/%name-2.0/*.so
%{_libdir}/%name-2.0/a11y-keyboard.gnome-settings-plugin
%{_libdir}/%name-2.0/background.gnome-settings-plugin
%{_libdir}/%name-2.0/clipboard.gnome-settings-plugin
%{_libdir}/%name-2.0/dummy.gnome-settings-plugin
%{_libdir}/%name-2.0/font.gnome-settings-plugin
%{_libdir}/%name-2.0/keybindings.gnome-settings-plugin
%{_libdir}/%name-2.0/keyboard.gnome-settings-plugin
%{_libdir}/%name-2.0/media-keys.gnome-settings-plugin
%{_libdir}/%name-2.0/mouse.gnome-settings-plugin
%{_libdir}/%name-2.0/screensaver.gnome-settings-plugin
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

