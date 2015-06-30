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
        grpBox.setStyle(self.style)
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
    #    stateLayout = QtGui.QHBoxLayout()
    #    self.stateOnRadioButton = QtGui.QRadioButton
    #
    #    nullWidget.setLayout(stateLayout)


# luanch window
if __name__ == '__main__':
    # get job info
    nHairToolset('someWin', [600,800], getMayaMainPtr())
