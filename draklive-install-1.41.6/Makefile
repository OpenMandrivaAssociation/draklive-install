NAME = draklive-install
VERSION = 1.41.5

dli_confdir = ${sysconfdir}/$(NAME).d
dli_sysconfigdir = $(dli_confdir)/sysconfig

all: openmandriva-draklive-install.desktop draklive-install.desktop
	make -C po

install:
	install -d $(dli_sysconfigdir)
	make -C po install

dist: dis 
dis: clean
	rm -rf ../$(NAME)-$(VERSION)*.tar* $(NAME)-$(VERSION) 
	@if [ -e ".svn" ]; then \
		$(MAKE) dist-svn; \
	elif [ -e ".git" ]; then \
		$(MAKE) dist-git; \
	else \
		echo "Unknown SCM (not SVN nor GIT)";\
		exit 1; \
	fi;
	$(info $(NAME)-$(VERSION).tar.xz is ready)
 
dist-svn: 
	svn export -q -rBASE . $(NAME)-$(VERSION)
	tar cfY ../$(NAME)-$(VERSION).tar.lzma $(NAME)-$(VERSION) 
	rm -rf $(NAME)-$(VERSION) 
 
dist-git: 
	@git archive --prefix=$(NAME)-$(VERSION)/ HEAD | xz -T0 >../$(NAME)-$(VERSION).tar.xz;

check:
	rm -f po/draklive-install.pot
	@make -C po draklive-install.pot

clean:
	make -C po clean
	find -name '*~' -exec rm {} \;

.PHONY: ChangeLog log changelog

log: ChangeLog

changelog: ChangeLog

ChangeLog:
	svn2cl --accum --authors ../../soft/common/username.xml
	rm -f *.bak

%.desktop: %.desktop.in
	intltool-merge --utf8 po \$< \$@ -d -u -c intltool-merge-cache

