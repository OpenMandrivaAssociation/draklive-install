%define name draklive-install
%define version 1.31
%define release %mkrel 16
%define iconname MandrivaOne-install-icon.png
%define xsetup_level 60

Summary:	Live installer
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.lzma
License:	GPL
Group:		System/Configuration/Other
Url:		https://svn.mandriva.com/svn/soft/drakx/trunk/live/draklive-install/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch
Requires:	drakxtools >= 13.51
Requires:	drakx-installer-matchbox
BuildRequires:	intltool
Patch0: draklive-install-1.31.checksize.patch
Patch1: draklive-install.disablepowersave.patch
Patch2: draklive-install-1.31.imagerotate.patch
Patch3: draklive-install-1.31.ru.locale.patch

%description
This tool allows to install Mandriva from a running live system.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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

mkdir -p %buildroot{%_miconsdir,%_iconsdir,%_liconsdir,%_menudir,%_datadir/libDrakX/pixmaps/,%_datadir/libDrakX/advert/,%_datadir/applications,%_datadir/icons/hicolor/{16x16,32x32,48x48}/apps}
install data/icons/IC-installone-48.png %buildroot%_liconsdir/%iconname
install data/icons/IC-installone-32.png %buildroot%_iconsdir/%iconname
install data/icons/IC-installone-16.png %buildroot%_miconsdir/%iconname
cp -l %buildroot%_liconsdir/%iconname %buildroot%_datadir/icons/hicolor/48x48/apps/%iconname
cp -l %buildroot%_liconsdir/%iconname %buildroot%_datadir/icons/hicolor/32x32/apps/%iconname
cp -l %buildroot%_liconsdir/%iconname %buildroot%_datadir/icons/hicolor/16x16/apps/%iconname
install data/icons/MandrivaOne-*.png %buildroot%_datadir/libDrakX/pixmaps/
install data/advert/* %buildroot%_datadir/libDrakX/advert/
install mandriva-draklive-install.desktop %buildroot%_datadir/applications/
install -D -m 0755 %{name}.xsetup %buildroot%_sysconfdir/X11/xsetup.d/%{xsetup_level}%{name}.xsetup
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
%_datadir/libDrakX/advert/*
%_sysconfdir/X11/xsetup.d/??%{name}.xsetup
%dir %_sysconfdir/%{name}.d
%dir %_sysconfdir/%{name}.d/sysconfig


%changelog
* Thu Aug 25 2011 Alex Burmashev <burmashev@mandriva.org> 1.31-10mdv2011.0
+ Revision: 697137
- updated ru locale

* Thu Aug 25 2011 Alex Burmashev <burmashev@mandriva.org> 1.31-9
+ Revision: 696557
- added an imgrotate ability

* Mon Aug 22 2011 Alex Burmashev <burmashev@mandriva.org> 1.31-8
+ Revision: 696106
- removed minsysreqs, added patch for faster install

* Wed Aug 10 2011 Denis Koryavov <dkoryavov@mandriva.org> 1.31-7
+ Revision: 693826
- Changed phase for the last step and minsysreg: ram = 640

* Tue Aug 09 2011 Alex Burmashev <burmashev@mandriva.org> 1.31-6
+ Revision: 693720
+ rebuild (emptylog)

* Tue Aug 09 2011 Alex Burmashev <burmashev@mandriva.org> 1.31-5
+ Revision: 693714
- disable powersaving for installation

* Thu Aug 04 2011 Alex Burmashev <burmashev@mandriva.org> 1.31-4
+ Revision: 693201
- fixed a typo in a new patch

* Tue Aug 02 2011 Alex Burmashev <burmashev@mandriva.org> 1.31-3
+ Revision: 692788
- added patch for correct time after first boot

* Wed Jun 29 2011 Alex Burmashev <burmashev@mandriva.org> 1.31-2
+ Revision: 688170
- updated picture for installer

* Mon Jun 27 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.31-1
+ Revision: 687509
- 1.31:
- add support for check_min_sys_requirements

* Mon Jun 27 2011 Alex Burmashev <burmashev@mandriva.org> 1.30-3
+ Revision: 687477
- added requirements check patch

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.30-2
+ Revision: 663856
- mass rebuild

* Tue Feb 22 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.30-1
+ Revision: 639242
- 1.30:
- make remove_unused_packages a configurable option

* Wed Aug 25 2010 Olivier Blin <blino@mandriva.org> 1.29-3mdv2011.0
+ Revision: 573329
- rebuild with new emi

* Fri Jul 02 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.29-2mdv2010.1
+ Revision: 549742
- don't install empty console helper file, but put meaningful data in it
  This should fix draklive-install not starting on GNOME Ones

* Wed Jun 02 2010 Pascal Terjan <pterjan@mandriva.org> 1.29-1mdv2010.1
+ Revision: 546941
- do not run makedev, needed devices are now copied before

* Wed May 26 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.28-1mdv2010.1
+ Revision: 546136
- 1.28
- use sligthly taller window for draklive-install so that diskdrake wizard
  isn't cut off

* Wed May 26 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.27-1mdv2010.1
+ Revision: 546068
- 1.27
- when starting install directly after boot, make sure we start
  draklive-install with the right locale set
- call set_wm_hints_if_needed to get correctly sized windows when running
  draklive-install directly after boot
- add 2010.1 ad

* Fri Apr 30 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.26-1mdv2010.1
+ Revision: 541290
- 1.26
- rename Live Install to Hard Disk Install
- add StartupNotify to draklive-install desktop files
- run scripts from /etc/draklive-install.d/run.d after install if cleanups
  are needed in the chrooted tree

* Wed Jan 13 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.25-1mdv2010.1
+ Revision: 490839
- add support for installation when source directory isn't /

* Wed Oct 28 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.23-1mdv2010.0
+ Revision: 459720
- 1.23:
- update advertising screen

* Mon Oct 12 2009 Olivier Blin <blino@mandriva.org> 1.22-1mdv2010.0
+ Revision: 456865
- 1.22
- keep pre-configured desktop session

* Fri Oct 09 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.21-1mdv2010.0
+ Revision: 456369
- 1.21:
- don't set gettext domain too late (caused badly displayed accents when running draklive-install) (Thierry Vignaud)

* Mon Oct 05 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.20-1mdv2010.0
+ Revision: 454069
- 1.20:
- adjust to drakxtools changes wrt default display manager choice

* Thu Oct 01 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.19-1mdv2010.0
+ Revision: 452242
- 1.19:
- use lzma compression
- make sure pterjan's fix for partitioning is included

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.18-2mdv2010.0
+ Revision: 413381
- rebuild

* Fri Apr 24 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.18-1mdv2009.1
+ Revision: 368993
- 1.18:
  * translate draklive-install desktop files
  * use 2009.1 advertising

* Wed Apr 22 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.17-1mdv2009.1
+ Revision: 368680
- 1.17:
- correctly exclude live_device when booting from hybrid USB image

* Wed Apr 15 2009 Thierry Vignaud <tv@mandriva.org> 1.16.2-1mdv2009.1
+ Revision: 367388
- updated translations

* Mon Mar 30 2009 Thierry Vignaud <tv@mandriva.org> 1.16.1-1mdv2009.1
+ Revision: 362298
- updated translations

* Fri Nov 21 2008 Olivier Blin <blino@mandriva.org> 1.16-1mdv2009.1
+ Revision: 305516
- 1.16
- do not hard re-enabled services list, read it from /etc/draklive-install.d/services

* Wed Oct 01 2008 Olivier Blin <blino@mandriva.org> 1.15-1mdv2009.0
+ Revision: 290335
- use consolehelper to run draklive-install (and hal-lock as root)
- install desktop files in /usr/share/mdk/desktop instead of specific
  KDE/GNOME locations
- 1.15
- use draklive-install-lock-storage from /usr/bin in desktop files

* Tue Sep 23 2008 Olivier Blin <blino@mandriva.org> 1.14-1mdv2009.0
+ Revision: 287516
- 1.14
- update advertising image

* Mon Sep 22 2008 Thierry Vignaud <tv@mandriva.org> 1.13.1-1mdv2009.0
+ Revision: 287022
- updated translations

* Wed Sep 17 2008 Frederic Crozat <fcrozat@mandriva.com> 1.13-2mdv2009.0
+ Revision: 285484
- Requires drakx-installer-matchbox

* Fri Sep 05 2008 Olivier Blin <blino@mandriva.org> 1.13-1mdv2009.0
+ Revision: 281254
- 1.13
- use new drakxtools code to remove unused packages

* Mon Aug 18 2008 Olivier Blin <blino@mandriva.org> 1.12-1mdv2009.0
+ Revision: 273391
- 1.12
- run remove-unselected-locales and remove-unused-hardware-packages
  before install

* Tue Jul 29 2008 Olivier Blin <blino@mandriva.org> 1.11-1mdv2009.0
+ Revision: 252764
- 1.11
- appear toplevel of the "Tools" menu in KDE

* Fri Jul 11 2008 Olivier Blin <blino@mandriva.org> 1.10-1mdv2009.0
+ Revision: 233705
- 1.10
- adapt kdm configuration to KDE4

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Jun 02 2008 Olivier Blin <blino@mandriva.org> 1.9-1mdv2009.0
+ Revision: 214351
- 1.9
- do not install bootloader on live device (useful for Mandriva Flash)
- get list of files to be removed from
  /etc/draklive-install.d/remove.d/
- do not allow update-menus to create home directory with invalid
  perms
- allow to specify custom copy source in
  /etc/sysconfig/draklive-install
  (to copy unmodified distro from Mandriva Flash)
- clean fstab in the live system (since partitions UUIDs of the
  installed system have been modified)
- remove hds from harddrake config in live system too so that they get
  reconfigured at next reboot
- umount partitions later
  (because g-v-m might have mounted them in the meantime)
- use wrapper to lock media managers during live install
  (not to get popups/automounts about new partitions)

* Thu Apr 03 2008 Olivier Blin <blino@mandriva.org> 1.8-1mdv2008.1
+ Revision: 192065
- 1.8
- do not crash when no valid devices is found (#36377)

* Fri Mar 21 2008 Olivier Blin <blino@mandriva.org> 1.6-1mdv2008.1
+ Revision: 189295
- 1.6
- fix unmounting disks in live root
- go on unmounting when one umount fails
- log when umount fails
- sync /var/log in installed root when needed

* Thu Mar 20 2008 Olivier Blin <blino@mandriva.org> 1.5-1mdv2008.1
+ Revision: 189124
- 1.5
- fix checking that available space is enough

* Thu Mar 20 2008 Olivier Blin <blino@mandriva.org> 1.4-1mdv2008.1
+ Revision: 189075
- package /etc/draklive-install.d and /etc/draklive-install.d/sysconfig
- 1.4
- check available space before formatting and installing (#22764)
- display error message and exit if install (files copy) failed
  (#22764)
- print an error message when the partitioning fails instead of dying
- run partition step in a loop while errors occur
- detect disks later to make startup faster
- do not hardcode first boot config files, copy them from
  /etc/draklive-install.d/sysconfig
- read live user from /etc/draklive-install.d/user
- add more wait messages
- update advert (from Hilhne)

* Fri Feb 29 2008 Olivier Blin <blino@mandriva.org> 1.3-1mdv2008.1
+ Revision: 176783
- 1.3
- mount /proc and /sys before install (for mkinitrd to find drivers)
- create devices early to have a consistent root before calling other
  programs (so that /dev/null does not become a plain file when
  accessed by other programs, thanks rtp!)
- don't die when unmounting fails
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 08 2007 Olivier Blin <blino@mandriva.org> 1.2-1mdv2008.1
+ Revision: 95747
- 1.2
- better fix for mdkonline
- 1.1
- fix reenabling mdkonline after install
- 1.0
- copy rpm db from /tmp/rpm/real if it exists
- do not try to "clean" rpm db anymore

* Sat Oct 06 2007 Olivier Blin <blino@mandriva.org> 0.9-1mdv2008.0
+ Revision: 95663
- 0.9
- add some padding between ad an progress bar
- rediscover hardddisks at first boot
- remove autologin before first boot and user finish-install's
  USER_AUTOLOGIN_FIRST instead (or else kdm's consolekit support will
  segfault, because we remove the autologin user during xsetup)

* Fri Oct 05 2007 Olivier Blin <blino@mandriva.org> 0.8-1mdv2008.0
+ Revision: 95633
- 0.8
- update ad
- use xdg-user-dir to detect desktop directory of guest user
  when removing desktop entries
- brute force clean of rpm db to fix draklive-install removal

* Thu Oct 04 2007 Olivier Blin <blino@mandriva.org> 0.7-1mdv2008.0
+ Revision: 95441
- 0.7
- really fix "reboot needed" warning (#33986)
- umount all partitions before starting install
- remove /etc/modprobe.d/mandriva-live after install

* Fri Sep 28 2007 Olivier Blin <blino@mandriva.org> 0.6-1mdv2008.0
+ Revision: 93784
- require a new drakxtools version to allow not poping wait messages
- 0.6
- fix "reboot needed" warning (#33986)
- enable mdkonline after install (#34000)
- use new pop_wait_messages option from interactive::gtk
  not to use hack that does not work anymore (made the installer crash)


* Tue Mar 27 2007 Olivier Blin <oblin@mandriva.com> 0.5-1mdv2007.1
+ Revision: 149018
- 0.5: use shared bootloader code (so that resume= is correctly set)
- copy icons in fdo location to make them sharper on the desktop (thanks Titi for the hint)
- 0.4

* Wed Feb 28 2007 Olivier Blin <oblin@mandriva.com> 0.3-1mdv2007.1
+ Revision: 127223
- 0.3 (see NEWS file for details)
- 0.3 (see NEWS file for details)

* Tue Feb 06 2007 Olivier Blin <oblin@mandriva.com> 0.2-1mdv2007.1
+ Revision: 116878
- 0.2
- fix progress bar (#27889)
- use fs::partitioning and fs::partitioning_wizard instead of copying installer code
- allow to run draklive-install at live boot with "install" parameter on the kernel command line (using xsetup.d)
- update/clean menus
- add menu entry (merge commit 86397)
- Import draklive-install

* Wed Sep 20 2006 Olivier Blin <oblin@mandriva.com> 0.1-10mdv2007.0
- reenable crond after live-install

* Sat Sep 16 2006 Olivier Blin <oblin@mandriva.com> 0.1-9mdv2007.0
- detect swap devices so that they can be unmounted
  (thanks Pixel for the debugging, #25538)

* Wed Sep 06 2006 Olivier Blin <oblin@mandriva.com> 0.1-8mdv2007.0
- create /mnt and its top-level-directories (#25137)
- don't grab focus if a window manager is running (#23454) and, as
  a side effect, don't die when switching to another desktop (#23453)

* Fri Jun 16 2006 Olivier Blin <oblin@mandriva.com> 0.1-7mdv2007.0
- remove useless update-menus calls

* Sun Mar 05 2006 Olivier Blin <oblin@mandriva.com> 0.1-6mdk
- allow to use grub as a bootloader (#21318, fix typo)

* Mon Feb 27 2006 Olivier Blin <oblin@mandriva.com> 0.1-5mdk
- updates translations

* Fri Feb 24 2006 Olivier Blin <oblin@mandriva.com> 0.1-4mdk
- make sure the cancel button is available in this pseudo-drakboot-boot
- make the wizard really die when it is cancelled
- use a smaller welcome image

* Fri Feb 24 2006 Olivier Blin <oblin@mandriva.com> 0.1-3mdk
- use correct size for small icon

* Thu Feb 23 2006 Olivier Blin <oblin@mandriva.com> 0.1-2mdk
- make partition tools not fail finding fs tools (#21260)
- update po files

* Fri Dec 16 2005 Olivier Blin <oblin@mandriva.com> 0.1-1mdk
- initial release

