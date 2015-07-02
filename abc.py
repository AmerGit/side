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
    def __init__(self, windowId, windowTitle, windowDimensions):
        # initialize main window features
        super(nHairToolset, self).__init__(getMayaMainPtr())

        self.setObjectName(windowId)
        self.setWindowTitle(windowTitle)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setFixedSize(windowDimensions[0], windowDimensions[1])
        # style setup
        #self.setStyle(QtGui.QStyleFactory.create('plastique'))
        a = QtGui.QStyleFactory.create('plastique')
        self.setStyle(a)
        print a

        # add layout and widgets
        self.centerWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centerWidget)
        # main layout for central widget
        self.mainLayout= QtGui.QVBoxLayout(self.centerWidget)
        self.centerWidget.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0,0,0,0)
        # create inner tab
        self.innerTabs = QtGui.QTabWidget(self.centerWidget)
        self.innerTabs.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mainLayout.addWidget(self.innerTabs)

        # first Tab
        self.mainControlsTab = QtGui.QWidget(self.innerTabs)
        self.innerTabs.addTab(self.mainControlsTab, 'Main Functions')
        self.mainControlsLayout = QtGui.QVBoxLayout(self.mainControlsTab)
        self.mainControlsLayout.setSpacing(2)
        self.mainControlsLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainControlsTab.setLayout(self.mainControlsLayout )
        # rigFix options
        self.rigFxGrpBox = self.createRigFixGroupBox()
        self.rigFixNameField = self.createLabeledNameField('Name: ', self.rigFxLayout)
        self.createRigFxButtons(self.rigFxLayout)
        # second tab
        self.secondaryControlsTab = QtGui.QWidget(self.innerTabs)
        self.innerTabs.addTab(self.secondaryControlsTab, 'Secondary')


    def centerWindow(self):
        framegeo = self.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        framegeo.moveCenter(center)
        self.move(framegeo.topLeft())


    def createRigFixGroupBox(self):
        rigFxBox = self.createGroupBox('RigFx Tools', self.mainControlsLayout)
        rigFxBox.setFixedSize(200,180)
        self.rigFxLayout = QtGui.QVBoxLayout()
        self.rigFxLayout.setAlignment(QtCore.Qt.AlignTop)
        rigFxBox.setLayout(self.rigFxLayout)
        self.rigFxName= QtGui.QLabel('Name:')
        return rigFxBox


    def createGroupBox(self, title, parentLayout):
        grpBox = QtGui.QGroupBox(title)
        #grpBox.setStyle(self.style)
        parentLayout.addWidget(grpBox)
        return grpBox


    def createLabeledNameField(self, labelText, parentLayout):
        # create horizontal layout to fit both items
        holderWidget = QtGui.QWidget()
        holderLayout = QtGui.QHBoxLayout(holderWidget)
        holderWidget.setLayout(holderLayout)
        # create actual the fields
        label = QtGui.QLabel(labelText)
        nameField = QtGui.QLineEdit()
        holderLayout.addWidget(label)
        holderLayout.addWidget(nameField)
        parentLayout.addWidget(holderWidget)
        return nameField


    def createRigFxButtons(self, parentLayout):
        self.buildRigFxBtn = QtGui.QPushButton('Build RigFx')
        self.updateSetsBtn = QtGui.QPushButton('Update Sets')
        self.motionMultBtn = QtGui.QPushButton('MotionMultiplier')
        parentLayout.addWidget(self.buildRigFxBtn)
        parentLayout.addWidget(self.updateSetsBtn)
        parentLayout.addWidget(self.motionMultBtn)

    #def createNucleusControls(self):
    #    self.nucleusGroupBox = self.createGroupBox('Nucleus', self.mainControlsLayout)
    #    self.nucleusGroupBoxLayout = QtGui.QVBoxLayout()
    #    self.nucleusGroupBox.setLayout(self.nucleusGroupBoxLayout)
    #    # create state controls
    #    nullWidget = QtGui.QWidget()
    #    stateLa   yout = QtGui.QHBoxLayout()
    #    self.stateOnRadioButton = QtGui.QRadioButton
    #
    #    nullWidget.setLayout(stateLayout)


# luanch window
if __name__ == '__main__':
    try:
        nHairWindow.close()
    except:
        pass

    # get shot info
    # job = os.environ['JOB']
    # shot = os.environ['SHOT']
    # title = 'Hair Toolset %s%s'%(job, %shot) 
    title = 'Hair Toolset'
    nHairWindow = nHairToolset('someWin',title, [600,800])
    nHairWindow.centerWindow()
    nHairWindow.show()
