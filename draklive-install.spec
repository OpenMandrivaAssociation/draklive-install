%define iconname	ROSAOne-install-icon.png
%define xsetup_level	60

Summary:	Live installer
Name:		draklive-install
Version:	1.36
Release:	3
License:	GPLv2
Group:		System/Configuration/Other
Url:		https://abf.rosalinux.ru/soft/draklive-install
Source0:	%{name}-%{version}-omv2.tar.xz
BuildArch:      noarch
BuildRequires:	intltool
Requires:	drakxtools >= 13.51
Requires:	drakx-installer-matchbox

%description
This tool allows to install OpenMandriva from a running live system.

%prep
%setup -q -n %name-%version-omv2
%apply_patches

%build
%make

%install
%makeinstall

for product in one flash; do
	install -D -m 0755 %{name}.desktop %{buildroot}%{_datadir}/mdk/desktop/$product/%{name}.desktop
done
install -D -m 0755 %{name} %{buildroot}/%{_sbindir}/%{name}
install -m 0755 %{name}-lock-storage %{buildroot}/%{_sbindir}/

mkdir -p %{buildroot}%{_bindir}
ln -sf consolehelper %{buildroot}%{_bindir}/%{name}-lock-storage
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
ln -sf mandriva-console-auth %{buildroot}%{_sysconfdir}/pam.d/%{name}-lock-storage
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name}-lock-storage <<EOF
USER=<user>
PROGRAM=/usr/sbin/%{name}-lock-storage
FALLBACK=false
SESSION=true
EOF

mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir},%{_datadir}/libDrakX/pixmaps/{en,ru},%{_datadir}/libDrakX/advert/{en,ru},%{_datadir}/applications,%{_datadir}/icons/hicolor/{16x16,32x32,48x48}/apps}
install data/icons/IC-installone-48.png %{buildroot}%{_liconsdir}/%{iconname}
install data/icons/IC-installone-32.png %{buildroot}%{_iconsdir}/%{iconname}
install data/icons/IC-installone-16.png %{buildroot}%{_miconsdir}/%{iconname}
cp -l %{buildroot}%{_liconsdir}/%{iconname} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{iconname}
cp -l %{buildroot}%{_liconsdir}/%{iconname} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{iconname}
cp -l %{buildroot}%{_liconsdir}/%{iconname} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{iconname}

#install advert to properties directores
install data/icons/en/*.png %{buildroot}%{_datadir}/libDrakX/pixmaps/en/
install data/advert/en/* %{buildroot}%{_datadir}/libDrakX/advert/en/
install data/icons/ru/*.png %{buildroot}%{_datadir}/libDrakX/pixmaps/ru/
install data/advert/ru/* %{buildroot}%{_datadir}/libDrakX/advert/ru/

install openmandriva-draklive-install.desktop %{buildroot}%{_datadir}/applications/
install -D -m 0755 %{name}.xsetup %{buildroot}%{_sysconfdir}/X11/xsetup.d/%{xsetup_level}%{name}.xsetup
install -m 0755 clean_live_hds %{buildroot}%{_sbindir}/clean_live_hds
%find_lang %{name}

%files -f %{name}.lang
%{_sysconfdir}/pam.d/%{name}-lock-storage
%{_sysconfdir}/security/console.apps/%{name}-lock-storage
%{_sysconfdir}/X11/xsetup.d/??%{name}.xsetup
%dir %{_sysconfdir}/%{name}.d
%dir %{_sysconfdir}/%{name}.d/sysconfig
%{_bindir}/%{name}-lock-storage
%{_sbindir}/%{name}
%{_sbindir}/clean_live_hds
%{_sbindir}/%{name}-lock-storage
%{_datadir}/mdk/desktop/*/*.desktop
%{_datadir}/applications/openmandriva-draklive-install.desktop
%{_datadir}/icons/hicolor/*/apps/%{iconname}
%{_datadir}/libDrakX/pixmaps/en/*.png
%{_datadir}/libDrakX/pixmaps/ru/*.png
%{_datadir}/libDrakX/advert/*
%{_iconsdir}/%{iconname}
%{_liconsdir}/%{iconname}
%{_miconsdir}/%{iconname}

