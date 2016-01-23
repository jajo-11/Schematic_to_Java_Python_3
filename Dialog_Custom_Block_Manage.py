from PySide import QtGui, QtCore
import os, pickle

class Dialog_Custom_Block_Manage(QtGui.QDialog):
    def __init__(self, parent):
        super(Dialog_Custom_Block_Manage, self).__init__(parent)
        self.current_names = []
        self.current_ids = []
        self.current_packages = []
        self.customFile = ''
        self.createComponents()
        self.createLayout()
        self.tooltips()
        self.preinit()
        #self.list_blocks_in_table()
        #self.createConnects()
        self.setWindowTitle(self.tr('Manage Coustom Block Set'))

    def createComponents(self):
        self.label = QtGui.QLabel(self.tr('Select and/or edit a custom block set'))
        self.combobox_sets = QtGui.QComboBox()
        self.button_add = QtGui.QPushButton(self.tr('Open Set'))
        self.table_blocks = QtGui.QTableWidget(0, 3, self)
        self.button_cancel = QtGui.QPushButton(self.tr('Cancel'))
        self.button_accept = QtGui.QPushButton(self.tr('Accept'))

    def createLayout(self):
        layoutDialog = QtGui.QVBoxLayout()
        layoutDialog.addWidget(self.label)

        layoutDialog2 = QtGui.QHBoxLayout()
        layoutDialog2.addWidget(self.combobox_sets)
        layoutDialog2.addWidget(self.button_add)
        layoutDialog.addLayout(layoutDialog2)

        layoutDialog.addWidget(self.table_blocks)

        layoutDialog3 = QtGui.QHBoxLayout()
        layoutDialog3.addWidget(self.button_cancel)
        layoutDialog3.addWidget(self.button_accept)
        layoutDialog.addLayout(layoutDialog3)

        self.setLayout(layoutDialog)

    def tooltips(self):
        self.combobox_sets.setToolTip(self.tr('Select a custom block set here.'))
        self.button_add.setToolTip(self.tr('Open a custom block set from another location.'))

    def preinit(self):
        if not os.path.isdir('customblocksets'):
            os.mkdir('customblocksets')
        for file in os.listdir('customblocksets'):
            if file.endswith('.cbs2'):
                self.combobox_sets.addItem(os.path.splitext(file)[0])
        self.table_blocks.setHorizontalHeaderLabels(['Ids', 'Names', 'Package'])
        self.table_blocks.verticalHeader().setVisible(False)
        self.table_blocks.horizontalHeader().ResizeMode(
            QtGui.QHeaderView.ResizeToContents)  # .setStretchLastSection(True)
        self.table_blocks.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.table_blocks.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def createConnects(self):
        self.button_accept.clicked.connect(self.save_cbs)
        self.button_cancel.clicked.connect(self.reject)
        self.combobox_sets.currentIndexChanged.connect(self.list_blocks_in_table)
        self.button_add.clicked.connect(self.add_cbs)
        self.table_blocks.customContextMenuRequested.connect(self.context_menu_table)

    def list_blocks_in_table(self):
        if 'Custom File' == self.combobox_sets.currentText():
            if os.path.isfile(self.customFile):
                file = open(self.customFile, 'rb')
            else:
                file = open(self.customFile, 'wb')
                for i in range(0, 3):
                    pickle.dump([], file)
                file.close()
                file = open(self.customFile, 'rb')
        elif self.combobox_sets.currentText():
            if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) +
                    '/customblocksets/' + self.combobox_sets.currentText() + '.cbs'):
                file = open(os.path.dirname(os.path.realpath(__file__)) +
                            '/customblocksets/' + self.combobox_sets.currentText() + '.cbs', 'rb')
            else:
                file = open(os.path.dirname(os.path.realpath(__file__)) +
                            '/customblocksets/' + self.combobox_sets.currentText() + '.cbs', 'wb')
                for i in range(0, 3):
                    pickle.dump([], file)
                file.close()
                file = open(os.path.dirname(os.path.realpath(__file__)) +
                            '/customblocksets/' + self.combobox_sets.currentText() + '.cbs', 'rb')

        self.current_names = pickle.load(file)
        self.current_ids = pickle.load(file)
        self.current_packages = pickle.load(file)
        file.close()

        self.table_blocks.setRowCount(0)

        for thing in self.current_ids:
            Qid = QtGui.QTableWidgetItem()
            Qid.setData(QtCore.Qt.DisplayRole, thing)
            Qname = QtGui.QTableWidgetItem(self.current_names[self.current_ids.index(thing)])
            Qpackage = QtGui.QTableWidgetItem(self.current_packages[self.current_ids.index(thing)])
            self.table_blocks.insertRow(self.table_blocks.rowCount())
            self.table_blocks.setItem(self.current_ids.index(thing), 0, Qid)
            self.table_blocks.setItem(self.current_ids.index(thing), 1, Qname)
            self.table_blocks.setItem(self.current_ids.index(thing), 2, Qpackage)

    def add_cbs(self):
        file = QtGui.QFileDialog.getOpenFileName(self, 'Add to Custom Block Set',
                                                 os.path.dirname(os.path.realpath(__file__)),
                                                 'Custom Block Set (*.cbs)')
        if file[0]:
            self.combobox_sets.insertItem(0, 'Custom File')
            self.combobox_sets.setCurrentIndex(0)
            self.customFile = file[0]
            self.list_blocks_in_table()

    def context_menu_table(self):
        menu = QtGui.QMenu()
        menu.addAction('New cbs', self.new_cbs)
        menu.addAction('Delete cbs', self.delete_cbs)
        menu.addSeparator()
        menu.addAction('Add Row', self.add_row_to_list)
        menu.addAction('Delete Row', self.remove_row_from_list)
        menu.exec_(QtGui.QCursor.pos())

    def add_row_to_list(self):
        self.table_blocks.insertRow(self.table_blocks.rowCount())
        qintobj = QtGui.QTableWidgetItem()
        qintobj.setData(QtCore.Qt.DisplayRole, 0)
        self.table_blocks.setItem(self.table_blocks.rowCount() - 1, 0, qintobj)

    def remove_row_from_list(self):
        if self.table_blocks.currentRow() or self.table_blocks.currentRow() == 0:
            self.table_blocks.removeRow(self.table_blocks.currentRow())

    def save_cbs(self):
        ids = []
        names = []
        package = []
        for i in range(0, self.table_blocks.rowCount()):
            ids.append(self.table_blocks.item(i, 0).text())
            names.append(self.table_blocks.item(i, 1).text())
            package.append(self.table_blocks.item(i, 2).text())
        if self.combobox_sets.currentText() and self.combobox_sets.currentText() != 'Custom File':
            file = open(os.path.dirname(os.path.realpath(__file__)) +
                        '/customblocksets/' + self.combobox_sets.currentText() + '.cbs', 'wb')
        elif self.combobox_sets.currentText():
            file = open(self.customFile, 'wb')
        else:
            pass  # file dialog for creating new cbs here
        pickle.dump(names, file)
        pickle.dump(ids, file)
        pickle.dump(package, file)
        file.close()
        self.accept()

    def new_cbs(self):
        file = QtGui.QFileDialog.getSaveFileName(self, u"New Custom Block Set",
                                                 os.path.dirname(os.path.realpath(__file__)) +
                                                 '/customblocksets/', 'Custom Block Set (*.cbs)')
        if file[0]:
            if os.path.samefile(os.path.realpath(os.path.dirname(file[0])),
                                os.path.dirname(os.path.realpath(__file__)) +
                                        '\\customblocksets'):
                self.combobox_sets.insertItem(0, os.path.splitext(os.path.basename(file[0]))[0])
                self.combobox_sets.setCurrentIndex(0)
                self.list_blocks_in_table()
            else:
                self.customFile = file[0]
                self.combobox_sets.insertItem(0, 'Custom File')
                self.combobox_sets.setCurrentIndex(0)
                self.list_blocks_in_table()

    def delete_cbs(self):
        dialog = QtGui.QMessageBox.question(self, self.tr('Delete Custom Block Set?'),
                                            self.tr('Do you rally want to delete \"' +
                                                    self.combobox_sets.currentText() + '.cbs\"?'),
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if dialog == QtGui.QMessageBox.Yes:
            if self.combobox_sets.currentText() and self.combobox_sets.currentText() != 'Custom File':
                os.remove(os.path.dirname(os.path.realpath(__file__)) +
                          '\\customblocksets\\' + self.combobox_sets.currentText() + '.cbs')
            elif self.combobox_sets.currentText():
                os.remove(self.customFile)
            self.combobox_sets.removeItem(self.combobox_sets.currentIndex())
            self.combobox_sets.setCurrentIndex(0)

    @property
    def selected(self):
        if self.combobox_sets.currentText() and self.combobox_sets.currentText() != 'Custom File':
            return [True, self.combobox_sets.currentText() + '.cbs']  # True means its in /customblocksets/
        elif self.combobox_sets.currentText():
            return [False, self.customFile]  # False means its not in /customblocksets/