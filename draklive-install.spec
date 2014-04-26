%define iconname live-install-icon.png
%define xsetup_level 60

Summary:	Live installer
Name:		draklive-install
Version:	1.39
Release:	1
License:	GPLv2
Group:		System/Configuration/Other
Url:		https://abf.io/omv_software/draklive-install
Source0:	%{name}-%{version}.tar.xz
BuildArch:	noarch
BuildRequires:	intltool
Requires:	drakxtools >= 14.43
Requires:	drakx-installer-matchbox
# even if this package is still named perl-Hal-Cdroms, it's been updated since
# to use udisks, so please do *NOT* remove...
Requires:	perl(Hal::Cdroms)

%description
This tool allows to install %{distribution} from a running live system.

%prep
%setup -q
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

mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir},%{_datadir}/libDrakX/pixmaps/{en,ru},%{_datadir}/libDrakX/advert/{en,ru},%{_datadir}/applications,%{_datadir}/icons/hicolor/{16x16,32x32,48x48,128x128}/apps}
install data/icons/live-install-icon-48.png %{buildroot}%{_liconsdir}/live-install-icon.png
install data/icons/live-install-icon-32.png %{buildroot}%{_iconsdir}/live-install-icon.png
install data/icons/live-install-icon-16.png %{buildroot}%{_miconsdir}/live-install-icon.png
install data/icons/live-install-icon-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/live-install-icon.png
cp -l %{buildroot}%{_liconsdir}/live-install-icon.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/live-install-icon.png
cp -l %{buildroot}%{_liconsdir}/live-install-icon.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/live-install-icon.png
cp -l %{buildroot}%{_liconsdir}/live-install-icon.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/live-install-icon.png

#install advert to properties directores
install data/icons/*.png %{buildroot}%{_datadir}/libDrakX/pixmaps/
install data/advert/* %{buildroot}%{_datadir}/libDrakX/advert/

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
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/libDrakX/pixmaps/*.png
%{_datadir}/libDrakX/advert/*
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
