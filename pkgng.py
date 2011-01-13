#!/usr/bin/python
#
# Lists packages
#

import os
import sys
import re
import pickle

from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative

DEBUG_WITH_CACHED_SEARCH=False

class synthesis_parser:
    """class to parse a synthesis hdlist"""
    _list={}
    _path={}
    _operation_re=None
    _requires_re=None
    def __init__(self):
        self._requires_re=re.compile('^([^[]*)(?:\[\*\])*(\[.*])?')
        self._operation_re=re.compile('\[([<>=]*) *(.*)\]')


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
    def get_list(self):
        """ return the list of rpm parsed from the synthesis """
        return self._list

    def get_path(self,rpm):
        """ return the path of the rpm"""
        r=self._list[rpm]
        res= os.path.dirname(self._path[r['source']]['path'])+'/'
        res=res + self._path[r['source']]['rpm']+'/'
        return res+'/'+'%s-%s-%s.%s.rpm' % (rpm,r['version'],r['release'],r['arch'])
    
    def open_listing(self,f):
        """ open a synthetis, by taking the url as argument. support ftp:// and http://, and simple file."""    
        # TODO and https ?
        if f.startswith('http://'):
                r=self.open_from_http(f)
        elif f.startswith('ftp://'):
                r=self.open_from_ftp(f)
        else:
                r=self.open_from_disk(f)
        return r

    def open_from_ftp(self,f):
        return self.open_from_http(f)
        
    #TODO used native python library, once urllib will be usable with gzip
    # use file detection
    def uncompress(self,f,cmd_line):
        """ open a compressed file """
        return cmd_line + ' | zcat '



    def open_from_http(self,f):
        """ read a file from http """
        # let's the fun begin, with popen
        cmd_line='wget -q -O - %s' % f;
        return os.popen(self.uncompress(f,cmd_line))

    def open_from_disk(self,f):
        cmd_line=' cat %s ' % f
        return os.popen(self.uncompress(f,cmd_line))


    def add_hdlist(self,name_source,path,path_to_rpm='.'):
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
    @QtCore.Slot(QtCore.QObject)
    def thingSelected(self, wrapper):
        print 'User clicked on:', wrapper._name

def list(si, pattern):
    packages = {}
    for item in si._list:
        if item.find(pattern) >= 0:
            cat = si._list[item]['group']
            descr = si._list[item]['summary']
            if cat not in packages:
                packages[cat] = []
            packages[cat].append((item, descr))

    return packages

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <pattern>" % sys.argv[0]
        sys.exit(1)
    # initialize synthesis

    # speedup stuff
    if DEBUG_WITH_CACHED_SEARCH:
        if os.access("list.dump", os.R_OK):
            print 'cached'
            cached=True
            fd = open("list.dump", "r")
            si = pickle.load(fd)
            si._list = pickle.load(fd)
            fd.close()
    else:
        cached=False
    si=synthesis_parser()
    si.add_hdlist('main','/var/lib/urpmi/Main/synthesis.hdlist.cz','../RPMS/')

    # initialize gui
    app = QtGui.QApplication(sys.argv)

    m = QtGui.QMainWindow()

    view = QtDeclarative.QDeclarativeView()
    glw = QtGui.QWidget()
    view.setViewport(glw)
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    things = []
    pkgs = list(si, sys.argv[1])
    if not cached:
        fd = open("list.dump", "w")
        pickle.dump(si, fd)
        ll = {}
    for cat in pkgs:
        things.append(ThingWrapper(cat, "Packages of category %s" % cat, is_title=True))
        for pkg, descr in pkgs[cat]:
            things.append(ThingWrapper(pkg, descr))
            if not cached:
                ll[pkg] = si._list[pkg]
    if not cached:
        # lets save a short list
        pickle.dump(ll, fd)
    fd.close()

    controller = Controller()
    thingList = ThingListModel(things)

    rc = view.rootContext()

    rc.setContextProperty('controller', controller)
    rc.setContextProperty('pythonListModel', thingList)

    view.setSource('pkgng.qml')

    m.setCentralWidget(view)

    m.show()

    app.exec_()
