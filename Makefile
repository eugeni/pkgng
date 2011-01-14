PACKAGE = pkgng
VERSION = 0.01
GITPATH = git://github.com:eugeni/pkgng.git

all: version

version:
	echo "version='$(VERSION)'" > version.py

clean:
	-find . -name '*.o' -o -name '*.py[oc]' -o -name '*~' | xargs rm -f

install: all
	install -d $(RPM_BUILD_ROOT)/usr/share/pkgng
	install -d $(RPM_BUILD_ROOT)/usr/bin
	install -m755 pkgng.py $(RPM_BUILD_ROOT)/usr/share/pkgng
	install -m644 *.qml $(RPM_BUILD_ROOT)/usr/share/pkgng
	ln -s /usr/share/pkgng/pkgng.py $(RPM_BUILD_ROOT)/usr/bin/pkgng

cleandist:
	rm -rf $(PACKAGE)-$(VERSION) $(PACKAGE)-$(VERSION).tar.bz2

dist: gitdist

gitdist: cleandist
	git archive --prefix $(PACKAGE)-$(VERSION)/ HEAD | bzip2 -9 > $(PACKAGE)-$(VERSION).tar.bz2
