Summary: GNOME Settings Daemon
Name: gnome-settings-daemon
Version: 2.21.90.1
Release: %mkrel 1
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

Requires: gstreamer0.10-plugins-base
Requires: gstreamer0.10-plugins-good
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.gnome.org/softwaremap/projects/control-center/

Requires: gnome-screensaver
Requires: gnome-desktop >= 2.1.4
Requires: gnome-themes
Requires: metacity
Conflicts: gnome-control-center < 2.21.5

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

%build
%configure2_5x --enable-gstreamer=0.10 --libexecdir=%_libdir/%name
%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%{find_lang} %name-2.0 --with-gnome --all-name

rm -f %buildroot%_libdir/%name/plugins/*/*a

%clean
rm -rf $RPM_BUILD_ROOT

%post
%define schemas apps_gnome_settings_daemon_default_editor apps_gnome_settings_daemon_keybindings apps_gnome_settings_daemon_screensaver desktop_gnome_font_rendering gnome-settings-daemon
%post_install_gconf_schemas %schemas

%preun
%preun_uninstall_gconf_schemas %schemas



%files -f %{name}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_default_editor.schemas
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_screensaver.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas
%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas
%_datadir/%name
%dir %{_libdir}/%name
%{_libdir}/%name/%name
%dir %{_libdir}/%name/plugins
%{_libdir}/%name/plugins/a11y-keyboard/
%{_libdir}/%name/plugins/dummy/        
%{_libdir}/%name/plugins/media-keys/   
%{_libdir}/%name/plugins/typing-break/
%{_libdir}/%name/plugins/background/      
%{_libdir}/%name/plugins/font/         
%{_libdir}/%name/plugins/mouse/        
%{_libdir}/%name/plugins/xrandr/
%{_libdir}/%name/plugins/clipboard/       
%{_libdir}/%name/plugins/keybindings/  
%{_libdir}/%name/plugins/screensaver/  
%{_libdir}/%name/plugins/xrdb/
%{_libdir}/%name/plugins/default-editor/  
%{_libdir}/%name/plugins/keyboard/     
%{_libdir}/%name/plugins/sound/        
%{_libdir}/%name/plugins/xsettings/
%_datadir/dbus-1/services/*

%files devel
%defattr(-, root, root)
%doc ChangeLog
%{_includedir}/*
%{_libdir}/pkgconfig/*

