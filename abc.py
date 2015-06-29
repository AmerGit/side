from maya import cmds
from maya import OpenMaya
from maya import OpenMayaUI
from PySide import QtGui
from PySide import QtCore
from functools import partial
import shiboken
import os

def getMayaMainPtr():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), QtGui.QWidget)


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
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setFixedSize(windowDimensions[0], windowDimensions[1])
        # style setup
        self.style = QtGui.QStyleFactory.create('plastique')

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
        # inner widget
        self.centerWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centerWidget)
        # main layout for central widget
        self.mainLayout= QtGui.QVBoxLayout(self.centerWidget)
        self.centerWidget.setLayout(self.mainLayout)
        # create inner tab
        self.innerTabs = QtGui.QTabWidget(self.centerWidget)
        self.innerTabs.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mainLayout.addWidget(self.innerTabs)
        # first Tab
        self.mainControlsTab = QtGui.QWidget(self.innerTabs)
        self.innerTabs.addTab(self.mainControlsTab, 'Main Functions')

        self.mainControlsLayout = QtGui.QVBoxLayout(self.mainControlsTab)
        self.mainControlsTab.setLayout(self.mainControlsLayout )
        self.rigFxGrpBox = self.createGroupBox('RigFx Tools', self.mainControlsLayout)
        self.mainControlsLayout.addWidget(self.rigFxGrpBox)

        # second tab
        self.secondaryControlsTab = QtGui.QWidget(self.innerTabs)
        self.innerTabs.addTab(self.secondaryControlsTab, 'Secondary')


    def createGroupBox(self, title, parentItem):
        grpBox = QtGui.QGroupBox(title)
        grpBox.setStyle(self.style)
        return grpBox

# luanch window
if __name__ == '__main__':
    # get job info
    nHairToolset('someWin', [600,800], getMayaMainPtr())
