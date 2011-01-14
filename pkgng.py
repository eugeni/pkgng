#!/usr/bin/python
#
# Lists packages
#

import os
import sys
import re
import gzip
from collections import OrderedDict
import threading

from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative

DEBUG_WITH_CACHED_SEARCH=False

class Thread(threading.Thread):
    def __init__(self, f, *args, **kwargs):
        threading.Thread.__init__(self)
        print "configuring thread.."
        self.func = f

    def run(self):
        self.func(*self.args, **self.kwargs)

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self.start()

class Repo:
    """class to parse a synthesis hdlist"""
    _urpmi_cfg = "/etc/urpmi/urpmi.cfg"
    _media_synthesis = "/var/lib/urpmi/%s/synthesis.hdlist.cz"
    _list={}
    _path={}
    _operation_re=None
    _requires_re=None

    def __init__(self):
        self._requires_re=re.compile('^([^[]*)(?:\[\*\])*(\[.*])?')
        self._operation_re=re.compile('\[([<>=]*) *(.*)\]')
        self.medias = {}

    def find_medias(self):
        """Attempts to locate and configure available medias"""
        medias = OrderedDict()
        media_r = re.compile('^(.*) {([\s\S]*?)\s*}', re.MULTILINE)
        ignore_r = re.compile('.*(ignore).*')
        update_r = re.compile('.*(update).*')
        key_r = re.compile('.*key-ids:\s* (.*).*')
        url_r = re.compile('(.*) (.*://.*|/.*$)')
        with open(self._urpmi_cfg, "r") as fd:
            data = fd.read()
            res = media_r.findall(data)
            for media, values in res:
                res2 = url_r.findall(media)
                if res2:
                    # found a media with url, fixing
                    name, url = res2[0]
                    media = name
                media = media.replace('\\', '')
                media = media.strip()
                key = ""
                ignore=False
                update=False
                keys = key_r.findall(values)
                if keys:
                    key = keys[0]
                if ignore_r.search(values):
                    ignore=True
                if update_r.search(values):
                    update=True
                medias[media] = (key, ignore, update)
        return medias

    def media_synthesis(self, media):
        """Returns media synthesis address"""
        return self._media_synthesis % media

    def split_requires(self,req_array):
        """split the requires in a dictionary"""
        res={}
        for i in req_array:
            require=self._requires_re.match(i)
            if require:
                name=require.groups()[0]
                res[name]={}
                condition=require.groups()[1]
                if condition:
                    op=''
                    version=''
                    o=self._operation_re.match(condition)
                    if o:
                        (op,version)=o.groups()[0:2]
                        res[name]['version']=version
                        res[name]['operation']=op
        return res

    def get_listpkgs(self):
        """ return the list of rpm parsed from the synthesis """
        return self._list

    def get_path(self,rpm):
        """ return the path of the rpm"""
        r=self._list[rpm]
        res= os.path.dirname(self._path[r['source']]['path'])+'/'
        res=res + self._path[r['source']]['rpm']+'/'
        return res+'/'+'%s-%s-%s.%s.rpm' % (rpm,r['version'],r['release'],r['arch'])

    def open_listing(self,f):
        """ open a local file synthesis """
        return gzip.open(f, "r")

    def add_hdlistpkgs(self,name_source,path,path_to_rpm='.'):
        """ add the synthesis.hdlist to the list """
        self._path[name_source]={}
        self._path[name_source]['path']=path
        self._path[name_source]['rpm']=path_to_rpm
        f=self.open_listing(path)
        tmp={}
        line=f.readline()
        while line:
            line=line.strip()
            l=line.split('@')[1:]
            if l[0] == 'summary':
                tmp['summary']=l[1]
            for i in ('requires','provides','conflict','obsoletes','suggests'):
                if l[0] == i:
                        tmp[i]=self.split_requires(l[1:])
            if l[0] == 'info':
                rpm=l[1].split('-')
                version=rpm[-2:-1][0]
                name='-'.join(rpm[0:-2])
                tmp['version']=version
                tmp['epoch']=l[2]
                tmp['size']=l[3]
                tmp['group']=l[4]
                tmp['source']=name_source
                tmp['release']='.'.join(rpm[-1].split('.')[0:-1])
                tmp['arch']=rpm[-1].split('.')[-1]
                self._list[name]=tmp
                tmp={}
            line=f.readline()

class ThingWrapper(QtCore.QObject):
    def __init__(self, name, description, is_title=False):
        QtCore.QObject.__init__(self)
        self._name = name
        self._description = description
        self._is_title = is_title

    def _name(self):
        return self._name

    def _description(self):
        return self._description

    def _is_title(self):
        return self._is_title

    changed = QtCore.Signal()

    name = QtCore.Property(unicode, _name, notify=changed)
    description = QtCore.Property(unicode, _description, notify=changed)
    is_title = QtCore.Property(bool, _is_title, notify=changed)

class ThingListModel(QtCore.QAbstractListModel):
    COLUMNS = ('thing',)

    def __init__(self, things):
        QtCore.QAbstractListModel.__init__(self)
        self._things = things
        self.setRoleNames(dict(enumerate(ThingListModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._things)

    def data(self, index, role):
        if index.isValid() and role == ThingListModel.COLUMNS.index('thing'):
            return self._things[index.row()]
        return None

class Controller(QtCore.QObject):
    def __init__(self, rc, si):
        QtCore.QObject.__init__(self)
        self.rc = rc
        self.si = si

    @QtCore.Slot(QtCore.QObject)
    def thingSelected(self, wrapper):
        print 'User clicked on:', wrapper._name

    @QtCore.Slot(QtCore.QObject)
    def searchPkgs(self, textInput):
        value = textInput.property('text')
        self.search(value, 'listPackagesModel')

    @QtCore.Slot(QtCore.QObject)
    def loadMedias(self, root):
        """Loads medias in background"""
        self.loadScreenData = root.property('loadScreenData')
        load_medias(self.si, self.progress, self.finished)

    def finished(self):
        """Medias finished loading"""
        self.loadScreenData['loadScreen'].setProperty("visible", False)
        self.loadScreenData['loadScreenNext'].setProperty("visible", True)
        searchView = self.loadScreenData['loadScreenNext']
        print searchView.property('searchBox')

    def progress(self, text):
        """Medias are loading, show progress"""
        self.loadScreenData['loadScreenProgress'].setProperty("text", text)

    def search(self, pattern, searchList):
        print searchList
        things = []
        pkgs = listpkgs(self.si, pattern)
        for cat in pkgs:
            things.append(ThingWrapper(cat, "Packages of category %s" % cat, is_title=True))
            for pkg, descr in pkgs[cat]:
                things.append(ThingWrapper(pkg, descr))

        thingList = ThingListModel(things)
        self.rc.setContextProperty(searchList, thingList)

def listpkgs(si, pattern):
    """Lists packages according to a pattern"""
    packages = {}
    for item in si._list:
        if item.find(pattern) >= 0:
            cat = si._list[item]['group']
            descr = si._list[item]['summary']
            if cat not in packages:
                packages[cat] = []
            packages[cat].append((item, descr))

    return packages

@Thread
def load_medias(si, progress, finished):
    """Loads medias in a separate thread, call @progress func to show progress and @finished when done"""
    medias = si.find_medias()
    # TODO: print information while parsing
    for media in medias:
        key, ignore, update = medias[media]

        if ignore:
            print "Media %s ignored" % media
            continue
        if not key:
            print "Media %s does not has a key!" % media
        progress("Loading repository info for %s media.." % media)
        if not os.access(si.media_synthesis(media), os.R_OK):
            print "Unable to access synthesis of %s, ignoring"
            ignore = True
            medias[media] = (key, ignore, update)
            continue
        si.add_hdlistpkgs(media, si.media_synthesis(media), '')
    finished()

if __name__ == "__main__":
    si=Repo()

    # initialize gui
    app = QtGui.QApplication(sys.argv)

    m = QtGui.QMainWindow()

    view = QtDeclarative.QDeclarativeView()
    glw = QtGui.QWidget()
    view.setViewport(glw)
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    things = []
    things.append(ThingWrapper("Package search", "", is_title=True))
    things.append(ThingWrapper("Type something to start searching", "The search will be performed according to package names"))

    rc = view.rootContext()

    controller = Controller(rc, si)
    thingList = ThingListModel(things)

    rc.setContextProperty('controller', controller)
    rc.setContextProperty('listPackagesModel', thingList)

    view.setSource('pkgng.qml')

    m.setCentralWidget(view)

    m.show()

    app.exec_()
