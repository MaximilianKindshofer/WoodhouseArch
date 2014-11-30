#!/usr/bin/env python3
from PySide import QtGui, QtCore
import sys, woodhouse_functions, os

class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initui()
        QtCore.QTimer.singleShot(100, self.garbageloop)

    def initui(self):
        self.deactivatedicon = QtGui.QPixmap(
                        '/usr/share/pixmaps/woodhouse/deactive.png')
        self.activatedicon = QtGui.QPixmap(
                        '/usr/share/pixmaps/woodhouse/active.png')
        self.woodhouseicon = QtGui.QIcon(QtGui.QPixmap(
                        '/usr/share/pixmaps/woodhouse/woodhouse.png'))
        self.setWindowIcon(self.woodhouseicon)
        self.systray = QtGui.QSystemTrayIcon(self.woodhouseicon)
        self.systray.setVisible(True)
        self.systray.activated.connect(self.iconActivated)

        #Context Menu for TrayIcon
        self.contextmenu = QtGui.QMenu()
        self.quitaction = QtGui.QAction("Quit", self, triggered=QtGui.qApp.quit)
        self.restore = QtGui.QAction("Restore", self,triggered=self.showNormal)
        self.contextmenu.addAction(self.restore)
        self.contextmenu.addAction(self.quitaction)
        self.systray.setContextMenu(self.contextmenu)


        self.setWindowTitle('Woodhouse')
        self.setGeometry(300, 300, 250, 350)

        # the left side of the window with the folders
        folderbar = QtGui.QLabel('Folders')
        self.folderlist = QtGui.QListWidget(self)
        self.folderlist.SingleSelection
        #add folders from rules.conf
        for folder in woodhouse_functions.getFolders():
            QtGui.QListWidgetItem(folder, self.folderlist)
        #TODO: use the current and previouse variable to get names
        self.folderlist.currentItemChanged.connect(self.viewActiveFolderRules)

        folderaddbutton = QtGui.QPushButton('Add',self)
        folderaddbutton.clicked.connect(self.addFolder)
        folderdeletebutton = QtGui.QPushButton('Delete', self)
        folderdeletebutton.clicked.connect(self.deleteFolder)

        # the right side of the window with the rules
        rulebar = QtGui.QLabel('Rules')
        self.rulelist = QtGui.QListWidget(self)
        self.rulelist.SingleSelection
        ruleaddbutton = QtGui.QPushButton('Add', self)
        ruleaddbutton.clicked.connect(self.configRule)
        ruleviewbutton = QtGui.QPushButton('View', self)
        ruleviewbutton.clicked.connect(self.viewRule)
        ruledeletebutton = QtGui.QPushButton('Delete', self)
        ruledeletebutton.clicked.connect(self.deleteRule)
        ruletestbutton = QtGui.QPushButton('Test Rule', self)
        ruletestbutton.clicked.connect(self.ruleTest)
        self.ruleenabledbutton = QtGui.QPushButton('Enable', self)
        self.ruleenabledbutton.clicked.connect(self.togglerule)
        self.rulelist.itemPressed.connect(self.ruleenabled)
        # GridLayout

        # left side
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(folderbar, 0, 0)
        self.grid.addWidget(self.folderlist,1, 0, 1, 2)
        self.grid.addWidget(folderaddbutton, 2, 0)
        self.grid.addWidget(folderdeletebutton, 2, 1)
        # space between the lists
        self.grid.addWidget(QtGui.QLabel(''),0, 2, 1, 5)
        # right side
        self.grid.addWidget(rulebar, 0, 3)
        self.grid.addWidget(self.rulelist, 1, 3, 1, 4)
        self.grid.addWidget(ruleaddbutton, 2, 3)
        self.grid.addWidget(ruleviewbutton, 2, 4)
        self.grid.addWidget(ruledeletebutton, 2, 5)
        self.grid.addWidget(ruletestbutton, 2 , 6)
        self.grid.addWidget(self.ruleenabledbutton, 2, 7)
        self.setLayout(self.grid)
        self.show()

    def msgbox(self, title, text):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowIcon(self.woodhouseicon)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.exec_()

    def closeEvent(self, event):
        self.hide()
        msg = "The program will keep running in the system tray. To terminate the program, choose 'Quit' in the context menu of the system tray entry."
        self.systray.showMessage("Close to Tray", msg)
        event.ignore()

    def iconActivated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.show()
        else:
            self.systray.contextMenu()

    def ruleenabled(self):
        rule = self.rulelist.currentItem()
        rulename = rule.text()
        folder = rule.toolTip()
        ruleenabled = woodhouse_functions.showruleactive(folder, rulename)
        if ruleenabled == 'False':
            self.ruleenabledbutton.setText('Enable')
        else:
            self.ruleenabledbutton.setText('Disable')

    def togglerule(self):
        rule = self.rulelist.selectedItems()
        rulename = [r.text() for r in rule]
        for item in rule:
            folder = item.toolTip()
        if rulename == []:
            self.msgbox('Select a rule', 'Please select a rule')
        else:
            woodhouse_functions.toggleactivateRule(folder, rulename[0])
            item = rule[0]
            if woodhouse_functions.showruleactive(folder, rulename[0]) == "True":
                self.ruleenabledbutton.setText("Disable")
                item.setIcon(self.activatedicon)
            else:
                self.ruleenabledbutton.setText("Enable")
                item.setIcon(self.deactivatedicon)


    def addFolder(self):
        # select Folder and display it
        folderselect = QtGui.QFileDialog()
        folderselect.setWindowIcon(self.woodhouseicon)
        folderselect.setFileMode(QtGui.QFileDialog.Directory)
        folderselect.setOption(QtGui.QFileDialog.ShowDirsOnly)
        if folderselect.exec_():
            self.folder = folderselect.selectedFiles()
            # to Display the Path in the List, we first copy
            # the data in a new variable cause we want to
            # give the folder variable to an other function later
            # it has the form of
            # ['/path/to/blerg'] we slice the first 2 and the
            # last 2
            #
            # To past me: thats a weird way to select the first
            # item of a list
            
            showfolder = self.folder
            showfolder = str(showfolder)[2:-2]
            duplicates = self.folderlist.findItems(showfolder, QtCore.Qt.MatchExactly)
            if len(duplicates) == 0:
                QtGui.QListWidgetItem(showfolder, self.folderlist)


    def deleteFolder(self):
        # wow since adding was so easy i thoght removing is as well
        # but apprently not. the right methode is to takeitem()
        # https://stackoverflow.com/questions/7484699/pyqt4-remove-item-widget-from-qlistwidget
        # get all ruleitems assosiated with this folder via tooltips
        rule = []
        folders = self.folderlist.selectedItems()
        foldername = [n.text() for n in folders]
        for row in range(self.rulelist.count()):
            rule.append(self.rulelist.item(row))

        if rule != []:
            for item in rule:
                if item.toolTip() == foldername[0]:
                    woodhouse_functions.deleterules(item.toolTip(), item.text())
                    self.rulelist.takeItem(self.rulelist.row(item))

            for selectedfolder in self.folderlist.selectedItems():
                self.folderlist.takeItem(self.folderlist.row(selectedfolder))
        else:
            for selectedfolder in self.folderlist.selectedItems():
                self.folderlist.takeItem(self.folderlist.row(selectedfolder))

    def viewActiveFolderRules(self, activeFolder):
        #remove all widgetitems (but dont touch the rules)
        self.rulelist.clear()
        folder = (activeFolder.text())
        rulelist = woodhouse_functions.getRules(folder)
        for rule in rulelist:
            self.addRule(rule, activeFolder.text())

    def configRule(self):
        # Configurate Rules and calls the addRuleHelper function
        #
        # selectedItems() currentItem would also work but it raises
        # an error after the if statement... not implemented yet error.
        # well I have no clue why, it has something to to with
        # None
        foldername = self.folderlist.selectedItems()
        if foldername == []:
            self.msgbox('No selected Folder', 'Choose a Folter to apply rules to.')
        else:
            self.ruleset = QtGui.QDialog(self)
            self.ruleset.setWindowIcon(self.woodhouseicon)
            # how to get the folders humanreadabel text (label)
            # http://stackoverflow.com/questions/12087715/pyqt4-get-list-of-all-labels-in-qlistwidget
            # again this could be more elegant but since I got the list from
            # selectedItems it would be wasteful just to use it for the
            # first check. Room for improvement.
            title = [t.text() for t in foldername]
            self.ruleset.setWindowTitle(title[0] + " rule set")
            namelabel = QtGui.QLabel('Name of the rule: ')
            self.nameline = QtGui.QLineEdit()
            timelabel = QtGui.QLabel('Delete files not modified more then')
            self.time = QtGui.QLineEdit()
            self.time.setInputMask("999")
            self.timescale = QtGui.QComboBox()
            self.timescale.insertItems(0,['days','months','years'])
            self.foldercheck = QtGui.QCheckBox('Include containing folders',self)
            savebutton = QtGui.QPushButton('Save',self)
            self.rulefolder = title[0]
            savebutton.clicked.connect(self.addRuleHelper)
            closebutton = QtGui.QPushButton('Close',self)
            closebutton.clicked.connect(self.ruleset.accept)
            #Grid for the rule window
            rulegrid = QtGui.QGridLayout()
            rulegrid.addWidget(namelabel, 0, 0)
            rulegrid.addWidget(self.nameline, 0, 1)
            rulegrid.addWidget(timelabel, 1, 0)
            rulegrid.addWidget(self.time, 1, 1)
            rulegrid.addWidget(self.timescale,1, 2)
            rulegrid.addWidget(self.foldercheck, 2, 0)
            rulegrid.addWidget(savebutton, 3, 1)
            rulegrid.addWidget(closebutton, 3, 2)
            self.ruleset.setLayout(rulegrid)
            self.ruleset.exec_()

    def addRuleHelper(self):
        #get the text from configRule's QLineEdit
        if self.nameline.text() == '':
            self.msgbox('Name rule','Please name your rule')
        #check for duplicated rulenames
        elif len(self.rulelist.findItems(self.nameline.text(),
                                         QtCore.Qt.MatchExactly)) != 0:
            self.msgbox('Duplicate rule', 'Please use an other name')
        #check if time is set
        elif self.time.text() == '':
            self.msgbox('Enter a Time', 'Enter a valid Time range')
        else:
            self.ruleset.accept()
            pathobject = self.folderlist.selectedItems()
            path = [p.text() for p in pathobject]
            saved = woodhouse_functions.saverules(path[0], self.nameline.text(),
                                        self.time.text(),
                                        self.timescale.currentText(),
                                        self.foldercheck.isChecked())
            if saved == 'OK':
                self.addRule(self.nameline.text(), path[0])

    def addRule(self, name, folder):
            label = name
            newItem = QtGui.QListWidgetItem()
            newItem.setText(label)
            # I use the tooltips as a hint to wich folder the Item belongs.
            # This is important if you delete an item since if you delete
            # the item you dont select a folder. It might be handy later
            # to just show the items belonging to one folder
            newItem.setToolTip(folder)
            if woodhouse_functions.showruleactive(folder, label) == "True":
                newItem.setIcon(self.activatedicon)
            else:
                newItem.setIcon(self.deactivatedicon)
            self.rulelist.addItem(newItem)

    def viewRule(self):
        # Shows the option set in the Rules
        rule = self.rulelist.selectedItems()
        rulename = [r.text() for r in rule]
        for item in rule:
            folder = item.toolTip()
        if rulename == []:
            self.msgbox('Select a rule', 'Please select rule')
        else:
            self.ruleedit = QtGui.QDialog(self)
            self.ruleedit.setWindowIcon(self.woodhouseicon)
            namelabel = QtGui.QLabel('Name of the rule: ')
            self.namelineedit = QtGui.QLineEdit()
            self.namelineedit.setText(rulename[0])
            timelabel = QtGui.QLabel('Delete files not modified more then')
            self.timeedit = QtGui.QLineEdit()
            self.timeedit.setInputMask("999")
            self.timeedit.setText(woodhouse_functions.showruletime(folder, rulename[0]))
            self.timescaleedit = QtGui.QComboBox()
            self.timescaleedit.insertItems(0,['days','months','years'])
            item = woodhouse_functions.showruletimescale(folder, rulename[0])
            if item == 'days':
                index = 0
            elif item == 'months':
                index = 1
            elif item == 'years':
                index = 2
            self.timescaleedit.setCurrentIndex(index)
            self.foldereditcheck = QtGui.QCheckBox('Include containing folders',self)
            if woodhouse_functions.showrulesubfolder(folder, rulename[0]) == 'True':
                state = QtCore.Qt.Checked
            else:
                state = QtCore.Qt.Unchecked
            self.foldereditcheck.setCheckState(state)
            savebutton = QtGui.QPushButton('Save',self)
            self.ruleeditfolder = folder
            savebutton.clicked.connect(self.editRuleHelper)
            closebutton = QtGui.QPushButton('Close',self)
            closebutton.clicked.connect(self.ruleedit.accept)
            #Grid for the rule window
            ruleeditgrid = QtGui.QGridLayout()
            ruleeditgrid.addWidget(namelabel, 0, 0)
            ruleeditgrid.addWidget(self.namelineedit, 0, 1)
            ruleeditgrid.addWidget(timelabel, 1, 0)
            ruleeditgrid.addWidget(self.timeedit, 1, 1)
            ruleeditgrid.addWidget(self.timescaleedit,1, 2)
            ruleeditgrid.addWidget(self.foldereditcheck, 2, 0)
            ruleeditgrid.addWidget(savebutton, 3, 1)
            ruleeditgrid.addWidget(closebutton, 3, 2)
            self.ruleedit.setLayout(ruleeditgrid)
            self.ruleedit.exec_()

    def editRuleHelper(self):
        folder = self.ruleeditfolder
        name = self.namelineedit.text()
        self.deleteRule()
        self.ruleedit.accept()
        pathobject = self.folderlist.selectedItems()
        saved = woodhouse_functions.saverules(folder, name,
                                    self.timeedit.text(),
                                    self.timescaleedit.currentText(),
                                    self.foldereditcheck.isChecked())
        if saved == 'OK':
            self.addRule(name, folder)


    def deleteRule(self):

        nameobject = self.rulelist.selectedItems()
        if nameobject == []:
            self.msgbox('No rule selected', 'Please select a rule to delete.')
        else:
            name = [n.text() for n in nameobject]
            path = [n.toolTip() for n in nameobject]
            removed = woodhouse_functions.deleterules(path[0],name[0])
            if removed == 'OK':
                for selectedRule in self.rulelist.selectedItems():
                    self.rulelist.takeItem(self.rulelist.row(selectedRule))

    def garbageloop(self):
        try:
            if os.path.exists('rules.conf'):
                msg = "Woodhouse performs cleaning tasks"
                self.systray.showMessage("Cleaning", msg)
                woodhouse_functions.clean(False)
            else:
                pass
        finally:
            #Launch every 30 Minutes
            QtCore.QTimer.singleShot(1800000, self.garbageloop)
            #Launch every 30 Seconds for Testing
            #QtCore.QTimer.singleShot(30000, self.garbageloop)
    def ruleTest(self):
        rule = self.rulelist.selectedItems()
        rulename = [r.text() for r in rule]
        folder = rule[0].toolTip()
        if rulename == []:
            self.msgbox('No rule selected','Please select a rule to delete.')
        else:
            delete = woodhouse_functions.testrules(folder)
            ruledelete = []
            text = "Items that should be deleted: \n"
            for items in delete:
                if folder in items:
                    ruledelete.append(items)
            try:
                text = text + str(items) + '\n'
                #Messagebox with extras:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowIcon(self.woodhouseicon)
                msgBox.setWindowTitle('Items to delete')
                #tailing spaces since msgBox ignores setGeometry
                msgBox.setText('There are ' + str(len(ruledelete)) + ' items to be deleted                     ')
                msgBox.setDetailedText(text)
                msgBox.exec_()
            except UnboundLocalError:
                msgBox = QtGui.QMessageBox()
                msgBox.setWindowIcon(self.woodhouseicon)
                msgBox.setWindowTitle('No Items to delete')
                #tailing spaces since msgBox ignores setGeometry
                msgBox.setText('There are ' + str(len(ruledelete)) + ' items to be deleted                     ')
                msgBox.exec_()
                

def main():

    app = QtGui.QApplication(sys.argv)
    woodhouse = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
