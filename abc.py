from maya import cmds, OpenMaya, OpenMayaUI
from PySide import QtGui, QtCore
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
        self.style = QtGui.QStyleFactory.create('plastique')
        self.setStyle(self.style)

        # add layout and widgets
        centerWidget = QtGui.QWidget(self)
        self.setCentralWidget(centerWidget)

        # setup central widget to hold all elements
        centerWidget.setLayout(QtGui.QVBoxLayout(centerWidget))
        centerWidget.layout().setContentsMargins(0,0,0,0)

        # create the tabwidget to hold the tabs
        innerTabs = QtGui.QTabWidget()
        innerTabs.setFocusPolicy(QtCore.Qt.NoFocus)
        centerWidget.layout().addWidget(innerTabs)

        # first Tab
        mainControlsTab = QtGui.QWidget()
        innerTabs.addTab(mainControlsTab, 'Main Functions')
        mainControlsLayout = QtGui.QVBoxLayout()
        mainControlsLayout.setSpacing(2)
        mainControlsLayout.setAlignment(QtCore.Qt.AlignTop)
        mainControlsTab.setLayout(mainControlsLayout )

        # rigFix options
        rigFxGrpBox = customGroupBox('RigFx Options', (180,150), 'plastique', 0, 0)
        mainControlsLayout.addWidget((rigFxGrpBox))
        rigFixNameField = self.createLabeledNameField('Name: ', 'Enter a RigFx name...')
        buildRigFxBtn = QtGui.QPushButton('Build RigFx')
        updateSetsBtn = QtGui.QPushButton('Update Sets')
        motionMultBtn = QtGui.QPushButton('MotionMultiplier')
        # populate rigFx groupBox
        rigFxGrpBox.layout().addLayout(rigFixNameField)
        rigFxGrpBox.layout().addWidget(buildRigFxBtn)
        rigFxGrpBox.layout().addWidget(updateSetsBtn)
        rigFxGrpBox.layout().addWidget(motionMultBtn)
        rigFxGrpBox.layout().addStretch(True)

        # second tab
        secondaryControlsTab = QtGui.QWidget(innerTabs)
        innerTabs.addTab(secondaryControlsTab, 'Secondary')


    def centerWindow(self):
        framegeo = self.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        framegeo.moveCenter(center)
        self.move(framegeo.topLeft())


    def createLabeledNameField(self, labelText, placeHolder=None):
        # create horizontal layout to fit both items
        holderLayout = QtGui.QHBoxLayout()
        # create actual the fields
        label = QtGui.QLabel(labelText)
        nameField = QtGui.QLineEdit()
        if placeHolder:
            nameField.setPlaceholderText(placeHolder)

        holderLayout.addWidget(label)
        holderLayout.addWidget(nameField)
        return holderLayout


class customGroupBox(QtGui.QGroupBox):
    def __init__(self, title=None, dimensions=None, style=None, spacing=None, margin=None, layout=QtGui.QVBoxLayout()):
        super(customGroupBox, self).__init__()
        self.setLayout(layout)
        if title:
            self.setTitle(title)
        if dimensions:
            self.setFixedSize(dimensions[0], dimensions[1])
        if style:
            self.setStyle(QtGui.QStyleFactory.create(style))
        if margin:
            self.layout().setContentsMargins(margin, margin, margin, margin)
        if spacing:
            self.layout().setSpacing(spacing)


# luanch window
if __name__ == '__main__':
    try:
        nHairWindow.close()
    except:
        pass

    # get shot info
    # job = os.environ['JOB']
    # shot = os.environ['SHOT']
    # windowTitle = 'Hair Toolset %s%s'%(job, %shot)
    windowTitle = 'Hair Toolset'
    nHairWindow = nHairToolset('nHairWindow',windowTitle, [600,800])
    nHairWindow.centerWindow()
    nHairWindow.show()
