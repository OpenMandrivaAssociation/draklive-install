%define name draklive-install
%define version 1.31
%define release %mkrel 4
%define iconname MandrivaOne-install-icon.png
%define xsetup_level 60

Summary:	Live installer
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.lzma
Source1:        minsysreqs
License:	GPL
Group:		System/Configuration/Other
Url:		https://svn.mandriva.com/svn/soft/drakx/trunk/live/draklive-install/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch
Requires:	drakxtools >= 13.51
Requires:	drakx-installer-matchbox
BuildRequires:	intltool
Patch0: draklive-install.time_fix.patch

%description
This tool allows to install Mandriva from a running live system.

%prep
%setup -q
%patch0 -p1

%build
%make

%install
rm -rf %buildroot

%makeinstall

for product in one flash; do
  install -D -m 0755 %name.desktop %buildroot%_datadir/mdk/desktop/$product/%name.desktop
done
install -D -m 0755 %name %buildroot/%_sbindir/%name
install -m 0755 %{name}-lock-storage %buildroot/%_sbindir/

mkdir -p %buildroot%_bindir
ln -sf consolehelper %buildroot%_bindir/%{name}-lock-storage
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
ln -sf mandriva-console-auth %{buildroot}%{_sysconfdir}/pam.d/%{name}-lock-storage
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name}-lock-storage <<EOF
USER=<user>
PROGRAM=/usr/sbin/%{name}-lock-storage
FALLBACK=false
SESSION=true
EOF

mkdir -p %buildroot{%_miconsdir,%_iconsdir,%_liconsdir,%_menudir,%_datadir/libDrakX/pixmaps/,%_datadir/applications,%_datadir/icons/hicolor/{16x16,32x32,48x48}/apps}
install data/icons/IC-installone-48.png %buildroot%_liconsdir/%iconname
install data/icons/IC-installone-32.png %buildroot%_iconsdir/%iconname
install data/icons/IC-installone-16.png %buildroot%_miconsdir/%iconname
cp -l %buildroot%_liconsdir/%iconname %buildroot%_datadir/icons/hicolor/48x48/apps/%iconname
cp -l %buildroot%_liconsdir/%iconname %buildroot%_datadir/icons/hicolor/32x32/apps/%iconname
cp -l %buildroot%_liconsdir/%iconname %buildroot%_datadir/icons/hicolor/16x16/apps/%iconname
install data/icons/MandrivaOne-*.png %buildroot%_datadir/libDrakX/pixmaps/
install mandriva-draklive-install.desktop %buildroot%_datadir/applications/
install -D -m 0755 %{name}.xsetup %buildroot%_sysconfdir/X11/xsetup.d/%{xsetup_level}%{name}.xsetup
install -m 0755 %SOURCE1 %buildroot%_sysconfdir/
%find_lang %name

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)
%_sbindir/%name
%_sbindir/%{name}-lock-storage
%_bindir/%{name}-lock-storage
%{_sysconfdir}/pam.d/%{name}-lock-storage
%{_sysconfdir}/security/console.apps/%{name}-lock-storage
%_datadir/mdk/desktop/*/*.desktop
%_datadir/applications/mandriva-draklive-install.desktop
%_iconsdir/%iconname
%_liconsdir/%iconname
%_miconsdir/%iconname
%_datadir/icons/hicolor/*/apps/%iconname
%_datadir/libDrakX/pixmaps/MandrivaOne-*.png
%_sysconfdir/X11/xsetup.d/??%{name}.xsetup
%_sysconfdir/minsysreqs
%dir %_sysconfdir/%{name}.d
%dir %_sysconfdir/%{name}.d/sysconfig
