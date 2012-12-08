%define name draklive-install
%define version 1.36
%define release 1
%define iconname ROSAOne-install-icon.png
%define xsetup_level 60

Summary:	Live installer
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.xz
License:	GPL
Group:		System/Configuration/Other
Url:		https://abf.rosalinux.ru/soft/draklive-install
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch
Requires:	drakxtools >= 13.51
Requires:	drakx-installer-matchbox
BuildRequires:	intltool

%description
This tool allows to install Rosa from a running live system.

%prep
%setup -q
%apply_patches

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

mkdir -p %buildroot{%_miconsdir,%_iconsdir,%_liconsdir,%_menudir,%_datadir/libDrakX/pixmaps/{en,ru},%_datadir/libDrakX/advert/{en,ru},%_datadir/applications,%_datadir/icons/hicolor/{16x16,32x32,48x48}/apps}
install data/icons/IC-installone-48.png %buildroot%_liconsdir/%iconname
install data/icons/IC-installone-32.png %buildroot%_iconsdir/%iconname
install data/icons/IC-installone-16.png %buildroot%_miconsdir/%iconname
cp -l %buildroot%_liconsdir/%iconname %buildroot%_datadir/icons/hicolor/48x48/apps/%iconname
cp -l %buildroot%_liconsdir/%iconname %buildroot%_datadir/icons/hicolor/32x32/apps/%iconname
cp -l %buildroot%_liconsdir/%iconname %buildroot%_datadir/icons/hicolor/16x16/apps/%iconname

#install advert to properties directores
install data/icons/en/ROSAOne-*.png %buildroot%_datadir/libDrakX/pixmaps/en/
install data/advert/en/* %buildroot%_datadir/libDrakX/advert/en/
install data/icons/ru/ROSAOne-*.png %buildroot%_datadir/libDrakX/pixmaps/ru/
install data/advert/ru/* %buildroot%_datadir/libDrakX/advert/ru/

install rosa-draklive-install.desktop %buildroot%_datadir/applications/
install -D -m 0755 %{name}.xsetup %buildroot%_sysconfdir/X11/xsetup.d/%{xsetup_level}%{name}.xsetup
install -m 0755 clean_live_hds %buildroot%_sbindir/clean_live_hds
%find_lang %name

%files -f %name.lang
%defattr(-,root,root)
%_sbindir/%name
%_sbindir/%{name}-lock-storage
%_bindir/%{name}-lock-storage
%{_sysconfdir}/pam.d/%{name}-lock-storage
%{_sysconfdir}/security/console.apps/%{name}-lock-storage
%_datadir/mdk/desktop/*/*.desktop
%_datadir/applications/rosa-draklive-install.desktop
%_iconsdir/%iconname
%_liconsdir/%iconname
%_miconsdir/%iconname
%_datadir/icons/hicolor/*/apps/%iconname
%_datadir/libDrakX/pixmaps/en/ROSAOne-*.png
%_datadir/libDrakX/pixmaps/ru/ROSAOne-*.png
%_datadir/libDrakX/advert/*
%_sysconfdir/X11/xsetup.d/??%{name}.xsetup
%dir %_sysconfdir/%{name}.d
%dir %_sysconfdir/%{name}.d/sysconfig
%{_sbindir}/clean_live_hds

%changelog
* Wed Aug 29 2012 akdengi <akdengi> 1.34-6
- now minimal_root function in fs:any not uses arguments anymore. Add patch draklive-install-1.34-fs_minimal_root.patch

* Wed Jun 20 2012 Alexander Kazancev <akdengi> 1.34-5
- xsetup fix for stop crond
- rm mtab and replace it for symlink

* Fri Jun 15 2012 Alexander Kazancev <akdengi> 1.34-1
- new version 1.34
 - switch lock storage to udisk
 - fix sync/umount patch and add clean script (clean_live_hds)
 - add fix patch for background darker over install
 - fix unmout function in xsetup
 - stop crond befor drakliv-install run

