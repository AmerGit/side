import sys
from PySide import QtGui


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

  wid = QtGui.QWidget()
  grid = QtGui.QGridLayout(wid)
  wid.setLayout(grid)
  
  # setting the inner widget and layout
  grid_inner = QtGui.QGridLayout(wid)
  wid_inner = QtGui.QWidget(wid)
  wid_inner.setLayout(grid_inner)
  
  # add the inner widget to the outer layout
  grid.addWidget(wid_inner)
  
  # add tab frame to widget
  wid_inner.tab = QtGui.QTabWidget(wid_inner)
  grid_inner.addWidget(wid_inner.tab)
  
  # create tab
  new_tab = QtGui.QWidget(wid_inner.tab)
  grid_tab = QtGui.QGridLayout(new_tab)
  grid_tab.setSpacing(10)
  new_tab.setLayout(grid_tab)
  new_tab.tab_name_private = "test1"
  wid_inner.tab.addTab(new_tab, "test1")
  
  # create tab 2
  new_tab2 = QtGui.QWidget(wid_inner.tab)
  new_tab2.setLayout(grid_tab)
  wid_inner.tab.addTab(new_tab2, "test2")
  
  wid.show()
  app.exec_()
