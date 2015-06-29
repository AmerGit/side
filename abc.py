from maya import cmds
from maya import OpenMaya
from maya import OpenMayaUI
from PySide import QtGui
from PySide import QtCore
from shiboken import wrapInstance
from functools import partial
from os import environ

def getMayaMainPtr():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QWidget)


class nHairToolset(QtGui.QMainWindow):
    def __init__(self, windowId, windowDimensions, parentWidget):
        # check if window exists
        if cmds.window(windowId, exists=True):
            cmds.deleteUI(windowId)
        
        # get shot info
        self.job = os.environ['JOB']
        self.shot = os.environ['SHOT']
        
        # initialize main window features
        super(nHairToolset, self).__init__(parentWidget)
        self.setObjectName(windowId)
        self.setWindowTitle('Hair Toolset [%s:%s]'%(self.job, self.shot))
        self.setFixedSize(400,400)
        # style setup
        style = QtGui.QStyleFactory.create('plastique')
        self.setStyle(style)        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # setup central widget for clean layout
        self.centerWidget = QtGui.QWidget()
        self.setCentralWidget(self.centerWidget)
        # add layout and widgets 
        self.createLayout()
        self.centerWindow()
        self.show()
    
    def centerWindow(self):
        framegeo = self.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        framegeo.moveCenter(center)
        self.move(framegeo.topLeft())

    def createLayout(self):
        # create main tabs
        self.tabBar = QtGui.QTabBar(self.centerWidget)
        self.tabBar.setFixedHeight(100)
        self.mainTab = self.tabBar.addTab('Main Tools')
        self.secondorayTab = self.tabBar.addTab('Secondary')
        
    
        # create nHair utils for first tab
        #self.nHairGroup = QtGui.QGroupBox(')
        
# luanch window
if __name__ == '__main__':
    # get job info
    nHairToolset('someWin', [400,400], getMayaMainPtr())    
