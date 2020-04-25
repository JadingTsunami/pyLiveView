# Wave Constructor: Generate waveJSON based on text description
#   Copyright (C) 2020      Jading Tsunami
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWebEngineWidgets import *
from PySide2.QtNetwork import *
from PySide2.QtWidgets import *

qa = QApplication(sys.argv)
qw = QWidget()

debug = False

def file_changed(path):
    updateHTML()

shpos = 0
svpos = 0

def debug_print(arg):
    global debug
    if debug:
        print arg

def updateHTML():
    global shpos
    global svpos
    oldh = shpos
    oldv = svpos
    shpos = qw.web.page().scrollPosition().x()
    svpos = qw.web.page().scrollPosition().y()
    debug_print( "Will store %s,%s (max: %s)" % (str(shpos),str(svpos),0))
    if shpos == 0:
        shpos = oldh
    if svpos == 0:
        svpos = oldv
    debug_print( "Stored %s,%s" % (str(shpos),str(svpos)))
    with open(str(sys.argv[1])) as f:
        qw.web.setHtml(''.join(f.readlines()))

def setScroll():
    debug_print( "Restoring %s,%s" % (str(shpos),str(svpos)))
    qw.web.page().runJavaScript("window.scrollTo("+str(shpos)+", "+str(svpos)+");")


fs_watcher = QFileSystemWatcher([str(sys.argv[1])])
fs_watcher.connect(fs_watcher, SIGNAL('fileChanged(QString)'), file_changed)


hbox = QHBoxLayout()

qw.web = QWebEngineView()
qw.web.connect(qw.web.page(), SIGNAL('contentsSizeChanged(QSizeF)'), setScroll )
qw.web.connect(qw.web, SIGNAL('loadFinished(bool)'), setScroll )
updateHTML()

hbox.addWidget(qw.web)

qw.setLayout(hbox)
qa.setStyle(QStyleFactory.create('Cleanlooks'))

qw.setGeometry(0, 0, 600, 800)
qw.setWindowTitle('LiveViewer')
qw.show()

sys.exit(qa.exec_())
