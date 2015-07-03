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
        self.style = QtGui.QStyleFactory.create('plastique')
        self.setStyle(self.style)

        # add layout and widgets
        centerWidget = QtGui.QWidget(self)
        self.setCentralWidget(centerWidget)

        # setup central widget to hold all elements
        centerWidget.setLayout(QtGui.QVBoxLayout(centerWidget))
        #centerWidget.layout().setContentsMargins(0,0,0,0)

        # create the tabwidget to hold the tabs
        innerTabs = QtGui.QTabWidget()
        innerTabs.setFocusPolicy(QtCore.Qt.NoFocus)
        centerWidget.layout().addWidget(innerTabs)

        # first Tab
        mainControlsTab = QtGui.QWidget()
        innerTabs.addTab(mainControlsTab, 'Main Functions')
        mainControlsLayout = QtGui.QVBoxLayout()
        mainControlsLayout.setAlignment(QtCore.Qt.AlignTop)
        mainControlsTab.setLayout(mainControlsLayout)

        # rigFix options group box
        rigFxGrpBox = customGroupBox('RigFx Options', (200,150), self.style.objectName(), 0, 0)
        rigFixNameField = self.createLabeledNameField('Name: ', 'enter a rigFx name...')
        buildRigFxBtn = QtGui.QPushButton('Build RigFx')
        updateSetsBtn = QtGui.QPushButton('Update Sets')
        motionMultBtn = QtGui.QPushButton('MotionMultiplier')
        # populate rigFx groupBox
        rigFxGrpBox.layout().addLayout(rigFixNameField)
        rigFxGrpBox.layout().addWidget(buildRigFxBtn)
        rigFxGrpBox.layout().addWidget(updateSetsBtn)
        rigFxGrpBox.layout().addWidget(motionMultBtn)
        rigFxGrpBox.layout().addStretch(True)

        # nHair groups options groupBox
        nHairGroupsGrpBox = customGroupBox('nHair Groups', (200,300), self.style.objectName(), 0, 0)
        nHairGroupList = QtGui.QListWidget()
        nHairGroupCreationField = self.createLabeledNameField('Group Name:', 'name your group...')
        nHairGroupCreateBtn = QtGui.QPushButton('Create')
        nHairGroupDeleteBtn = QtGui.QPushButton('Delete')
        nHairGroupControlsBtn = QtGui.QPushButton('Create Controls')
        nHairGroupWindControlsBtn = QtGui.QPushButton('Create Wind Controls')
        # add the nHair group elements to the corresponding groupbox
        nHairGroupsGrpBox.layout().addWidget(nHairGroupList)
        nHairGroupsGrpBox.layout().addLayout(nHairGroupCreationField)
        nHairGroupsGrpBox.layout().addWidget(nHairGroupCreateBtn)
        nHairGroupsGrpBox.layout().addWidget(nHairGroupControlsBtn)
        nHairGroupsGrpBox.layout().addWidget(nHairGroupWindControlsBtn)

        # little nucleus groupbox
        nucleusGroupBox = customGroupBox('Nucleus', (200, 48), self.style.objectName(), 0, 0, QtGui.QHBoxLayout())
        nucleusGroupBox.layout().setAlignment(QtCore.Qt.AlignCenter)
        nucleusSateLabel = QtGui.QLabel('State: ')
        nucleusOnRadioBtn = QtGui.QRadioButton('On')
        nucleusOffRadioBtn = QtGui.QRadioButton('Off')
        nucleusOnRadioBtn.setChecked(True)

        # add widgets to groupBox
        nucleusGroupBox.layout().addWidget(nucleusSateLabel)
        nucleusGroupBox.layout().addItem(QtGui.QSpacerItem(20,2))
        nucleusGroupBox.layout().addWidget(nucleusOnRadioBtn)
        nucleusGroupBox.layout().addItem(QtGui.QSpacerItem(20,2))
        nucleusGroupBox.layout().addWidget(nucleusOffRadioBtn)

        # nHair groupBox
        nHairToolBox = customGroupBox('nHair Tools', [200,200], self.style.objectName(), 0, 0, QtGui.QGridLayout())
        nHairToolBox.layout().setAlignment(QtCore.Qt.AlignTop)
        createHairBtn = customIconButton(':/hairCreate.png',(40,40), 'Create Hair')
        paintHairBtn = customIconButton(':/hairPaint.png',(40,40), 'Paint Hair Tool')
        mkDynCurvesBtn = customIconButton(':/hairDynamicCurves.png',(40,40), 'Make Selected Curves Dynamic')
        interactiveBtn = customIconButton(':/interactivePlayback.png',(40,40), 'Interactive Playback')

        # add them to groupBox
        nHairToolBox.layout().addWidget(createHairBtn, 0,0)
        nHairToolBox.layout().addWidget(paintHairBtn, 0,1)
        nHairToolBox.layout().addWidget(mkDynCurvesBtn, 0,2)
        nHairToolBox.layout().addWidget(interactiveBtn, 0,3)

        # add main Widgets to the first tab
        mainControlsLayout.addWidget(rigFxGrpBox)
        mainControlsLayout.addWidget(nHairGroupsGrpBox)
        mainControlsLayout.addWidget(nucleusGroupBox)
        mainControlsLayout.addWidget(nHairToolBox)

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
    def __init__(self, title=None, dimensions=None, style=None, spacing=None, margin=None, layout=None):
        super(customGroupBox, self).__init__()

        if layout:
            self.setLayout(layout)
        else:
            self.setLayout(QtGui.QVBoxLayout())

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


class customIconButton(QtGui.QToolButton):
    def __init__(self, iconPath, size=(40,40), hint=None, flatFlag=False):
        super(customIconButton, self).__init__()
        self.setFixedSize(size[0],size[1])
        self.setIconSize(QtCore.QSize(100,100))
        self.setIcon(QtGui.QIcon(iconPath))
        #self.setFlat(flatFlag)
        if hint:
            self.setToolTip(hint)


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
