from maya import cmds, OpenMaya, OpenMayaUI
from PySide import QtGui, QtCore
from functools import partial
import shiboken
import os

def getMayaMainPtr():
    """
    function that grabs the pointer to the maya main window for parenting other widgets under it
    """
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), QtGui.QWidget)


class nHairToolset(QtGui.QMainWindow):
    def __init__(self, windowId, windowTitle, windowDimensions):
        """
        initialization method use to create an instance of the window
        
        @param windowId: used to identify the window to check for existence
        @param windowTitle: title for the window, which will normally be the job and shot info
        @param windowDimensions: tuple or list with width and height
        @return:None
        """
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
        # setup central widget to hold all elements
        centerWidget.setLayout(QtGui.QVBoxLayout(centerWidget))
        self.setCentralWidget(centerWidget)

        # create the tabwidget to hold the tabs
        innerTabs = QtGui.QTabWidget()
        innerTabs.setFocusPolicy(QtCore.Qt.NoFocus)
        centerWidget.layout().addWidget(innerTabs)

        # first Tab
        mainControlsTab = QtGui.QWidget()
        mainControlsTab.setLayout(QtGui.QHBoxLayout())
        mainControlsTab.layout().setAlignment(QtCore.Qt.AlignLeft)
        mainControlsTab.layout()
        #----------------------------------------------------------------------------------------------------------#
        # first column for the main tab
        mainTabColumn1_Layout = QtGui.QVBoxLayout()
        mainTabColumn1_Layout.setAlignment(QtCore.Qt.AlignTop)
        innerTabs.addTab(mainControlsTab, 'Main Functions')

        # rigFix options groupBox
        rigFxGrpBox = customGroupBox('RigFx Options', (240,160), self.style.objectName(), 0, 0)
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
        nHairGroupsGrpBox = customGroupBox('nHair Groups', (240,330), self.style.objectName(), 0, 0)
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
        nHairGroupsGrpBox.layout().addWidget(nHairGroupDeleteBtn)
        nHairGroupsGrpBox.layout().addWidget(nHairGroupControlsBtn)
        nHairGroupsGrpBox.layout().addWidget(nHairGroupWindControlsBtn)

        # little nucleus groupboxer
        nucleusGroupBox = customGroupBox('Nucleus', (240, 48), self.style.objectName(), 0, 0, QtGui.QHBoxLayout())
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
        nHairToolBox = customGroupBox('nHair Tools', [240,200], self.style.objectName(), 0, 0, QtGui.QGridLayout())
        nHairToolBox.layout().setAlignment(QtCore.Qt.AlignTop)
        createHairBtn = customIconButton(':/hairCreate.png',(40,40), 'Create Hair')
        paintHairBtn = customIconButton(':/hairPaint.png',(40,40), 'Paint Hair Tool')
        mkDynCurvesBtn = customIconButton(':/hairDynamicCurves.png',(40,40), 'Make Selected Curves Dynamic')
        interactiveBtn = customIconButton(':/interactivePlayback.png',(40,40), 'Interactive Playback')
        currentPosDispBtn = customIconButton(':/hairDisplayCurrent.png',(40,40), 'Display Current Position')
        startPosDispBtn =  customIconButton(':/hairDisplayStart.png',(40,40), 'Display Start Position')
        restPosDispBtn =  customIconButton(':/hairDisplayRest.png',(40,40), 'Display Rest Position')
        nCacheCreateBtn = customIconButton(':/nClothCacheCreate.png',(40,40), 'Create nCache')
        nCacheDeleteBtn = customIconButton(':/nClothCacheDelete.png',(40,40), 'Delete nCache')
        # add them to groupBox
        nHairToolBox.layout().addWidget(createHairBtn, 0,0)
        nHairToolBox.layout().addWidget(paintHairBtn, 0,1)
        nHairToolBox.layout().addWidget(mkDynCurvesBtn, 0,2)
        nHairToolBox.layout().addWidget(interactiveBtn, 0,3)
        nHairToolBox.layout().addWidget(currentPosDispBtn, 0,4)
        nHairToolBox.layout().addWidget(startPosDispBtn, 1,0)
        nHairToolBox.layout().addWidget(restPosDispBtn, 1,1)
        nHairToolBox.layout().addWidget(nCacheCreateBtn, 1,2)
        nHairToolBox.layout().addWidget(nCacheDeleteBtn, 1,3)
        # add the first column widgets to the corresponding layout
        mainTabColumn1_Layout.addWidget(rigFxGrpBox)
        mainTabColumn1_Layout.addWidget(nHairGroupsGrpBox)
        mainTabColumn1_Layout.addWidget(nucleusGroupBox)
        mainTabColumn1_Layout.addWidget(nHairToolBox)

        #----------------------------------------------------------------------------------------------------------#
        # second column for the main tab
        mainTabColumn2_Layout = QtGui.QVBoxLayout()
        mainTabColumn2_Layout.setAlignment(QtCore.Qt.AlignTop)

        # control list set
        controlsGroupBox = customGroupBox('Controls', (220, 160), self.style.objectName())
        controlList = QtGui.QListWidget()
        # add the control list to the groupbox
        controlsGroupBox.layout().addWidget(controlList)

        # dynamic node list
        dynamicNodesGroupBox = customGroupBox('Dynamic nodes', (220, 160), self.style.objectName())
        dynamicNodeList = QtGui.QListWidget()
        # add the dynamic node list to the groupbox
        dynamicNodesGroupBox.layout().addWidget(dynamicNodeList)

        # collider and constraint nodes list
        colConstGroupBox = customGroupBox('Colliders and Consraints', (220, 160), self.style.objectName())
        colConstNodeList = QtGui.QListWidget()
        # add the colliders and constraints list to the groupbox
        colConstGroupBox.layout().addWidget(colConstNodeList)

        ## force nodes list
        #forcesGroupBox = customGroupBox('Forces', (200, 140), self.style.objectName())
        #forcesNodeList = QtGui.QListWidget()
        ## add the force list to the groupbox
        #forcesGroupBox.layout().addWidget(forcesNodeList)

        # add the second column widgets to the second column
        mainTabColumn2_Layout.addWidget(controlsGroupBox)
        mainTabColumn2_Layout.addWidget(dynamicNodesGroupBox)
        mainTabColumn2_Layout.addWidget(colConstGroupBox)
        #----------------------------------------------------------------------------------------------------------#

        # add the main tab columns to the first tab
        mainControlsTab.layout().addLayout(mainTabColumn1_Layout)
        mainControlsTab.layout().addItem(QtGui.QSpacerItem(20,0))
        mainControlsTab.layout().addLayout(mainTabColumn2_Layout)

        # second tab
        secondaryControlsTab = QtGui.QWidget(innerTabs)
        innerTabs.addTab(secondaryControlsTab, 'Secondary')


    def centerWindow(self):
        """
        method that places an instance object in the center
        
        @return: NONE
        """
        framegeo = self.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        framegeo.moveCenter(center)
        self.move(framegeo.topLeft())


    def createLabeledNameField(self, labelText, placeHolder=None):
        """
        method that automates the creation of a text feild with a label placed to its left
        
        @param labelText: name for the label
        @param placeHolder: placeholder text for the field widget
        @return: horizontal layout that contains the title and field
        """
        # create horizontal layout to fit both items
        holderLayout = QtGui.QHBoxLayout()
        # create actual the fields
        label = QtGui.QLabel(labelText)
        nameField = QtGui.QLineEdit()
        if placeHolder:
            nameField.setPlaceholderText(placeHolder)

        # add widgets to layout
        holderLayout.addWidget(label)
        holderLayout.addWidget(nameField)
        return holderLayout


class customGroupBox(QtGui.QGroupBox):
    def __init__(self, title=None, dimensions=None, style=None, spacing=None, margin=None, layout=QtGui.QVBoxLayout()):
        """
        creates and sets up a custom groupBox with all the needed attributes
        
        @param title: name to show on top side of groupbox
        @param dimensions: tuple or list for width and height
        @param style: style object, will usually pass the one from the parent
        @param spacing: spacing between subwidgets inside the groupBox's main layout
        @param margin: single margin size for all 4 sides
        @param layout: QLayout object, will be verticle by default
        @return: NONE
        """
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


class customIconButton(QtGui.QToolButton):
    def __init__(self, iconPath, size=(40,40), hint=None):
        """
        quickly creates a button with an icon and tooltip
        
        @param iconPath: location for the icon
        @param size: tuple or list containg the width and height
        @param hint: label for the annotation to display while hovering over the button
        @return: NONE
        """
        super(customIconButton, self).__init__()
        self.setFixedSize(size[0],size[1])
        self.setIconSize(QtCore.QSize(100,100))
        self.setIcon(QtGui.QIcon(iconPath))
        if hint:
            self.setToolTip(hint)


# launch window
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
    nHairWindow = nHairToolset('nHairWindow', title, [520,840])
    nHairWindow.centerWindow()
    nHairWindow.show()
