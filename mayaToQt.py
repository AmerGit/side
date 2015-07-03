import maya.OpenMayaUI as apiUI
from PyQt4 import QtGui, QtCore
import sip

def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

def toQtObject(mayaName):
    '''
    Given the name of a Maya UI element of any type,
    return the corresponding QWidget or QAction.
    If the object does not exist, returns None
    '''
    ptr = apiUI.MQtUtil.findControl(mayaName)
    if ptr is None:
        ptr = apiUI.MQtUtil.findLayout(mayaName)
    if ptr is None:
        ptr = apiUI.MQtUtil.findMenuItem(mayaName)
    if ptr is not None:
        return sip.wrapinstance(long(ptr), QtCore.QObject)

class MayaSubWindow(QtGui.QMainWindow):
    def __init__(self, parent=getMayaWindow()):
        super(MayaSubWindow, self).__init__(parent)
        self.executer = cmds.cmdScrollFieldExecuter(sourceType="python")
        qtObj = toQtObject(self.executer)
        #Fill the window, could use qtObj.setParent
        #and then add it to a layout.
        self.setCentralWidget(qtObj)

myWindow = MayaSubWindow()
myWindow.show()
