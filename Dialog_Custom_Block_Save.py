from PySide import QtGui
import pickle, os


class Dialog_Custom_Block_Save(QtGui.QDialog):
    def __init__(self, parent, names, ids, packages):
        super(Dialog_Custom_Block_Save, self).__init__(parent)
        self.names = names
        self.ids = ids
        self.packages = packages
        self.createComponents()
        self.createLayout()
        self.createConnects()
        self.setWindowTitle(self.tr('Save Coustom Block Set'))

    def createComponents(self):
        self.label = QtGui.QLabel(
            self.tr('There were some unknown blocks in this schematic do you want to save their names for the future?'))
        self.button_cancel = QtGui.QPushButton(self.tr('Don\'t Save'))
        self.button_add = QtGui.QPushButton(self.tr('Add to existing Save'))
        self.button_save = QtGui.QPushButton(self.tr('Save'))

    def createLayout(self):
        layoutDialog = QtGui.QVBoxLayout()
        layoutDialog.addWidget(self.label)

        layoutDialog2 = QtGui.QHBoxLayout()
        layoutDialog2.addWidget(self.button_cancel)
        layoutDialog2.addWidget(self.button_add)
        layoutDialog2.addWidget(self.button_save)

        layoutDialog.addLayout(layoutDialog2)
        self.setLayout(layoutDialog)

    def createConnects(self):
        self.button_cancel.clicked.connect(self.reject)
        self.button_add.clicked.connect(self.filedialog_save_add)
        self.button_save.clicked.connect(self.filedialog_save)

    def filedialog_save(self):
        file = QtGui.QFileDialog.getSaveFileName(self, 'Save Custom Block Set',
                                                 os.path.dirname(os.path.realpath(__file__)) + '/customblocksets',
                                                 'Custom Block Set (*.cbs)')
        if file[0]:
            save_file = open(file[0], 'wb')
            pickle.dump(self.names, save_file)
            pickle.dump(self.ids, save_file)
            pickle.dump(self.packages, save_file)
            save_file.close()
        self.accept()

    def filedialog_save_add(self):
        if not os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + '/customblocksets'):
            os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/customblocksets')
        file = QtGui.QFileDialog.getOpenFileName(self, 'Add to Custom Block Set',
                                                 os.path.dirname(os.path.realpath(__file__)) + '/customblocksets',
                                                 'Custom Block Set (*.cbs)')
        if file[0]:
            save_file = open(file[0], 'rb')
            names_saved = []
            ids_saved = []
            all_yes = False
            all_no = False
            names_saved = pickle.load(save_file)
            ids_saved = pickle.load(save_file)
            packages_saved = pickle.load(save_file)
            for entry in self.ids:
                if entry in ids_saved and all_yes == True:
                    names_saved[ids_saved.index(entry)] = self.names[self.ids.index(entry)]
                    packages_saved[ids_saved.index(entry)] = self.packages[self.ids.index(entry)]
                if entry in ids_saved and all_yes == False and all_no == False:
                    overwrite_Dialog = QtGui.QMessageBox()
                    overwrite_Dialog.setWindowTitle(self.tr('Duplicate ids'))
                    overwrite_Dialog.setText(self.tr(
                        'The Block \"' + self.names[self.ids.index(entry)] + '\" alredy exists as \"' + names_saved[
                            ids_saved.index(entry)] + '\"'))
                    overwrite_Dialog.setInformativeText(self.tr('Do you want to overwrite it?'))
                    overwrite_Dialog.setStandardButtons(
                        QtGui.QMessageBox.No | QtGui.QMessageBox.NoAll | QtGui.QMessageBox.YesAll |
                        QtGui.QMessageBox.Yes)
                    overwrite_Dialog.setDefaultButton(QtGui.QMessageBox.Yes)
                    overwrite_Dialog.setEscapeButton(QtGui.QMessageBox.No)
                    overwrite_Dialog.setIcon(QtGui.QMessageBox.Question)
                    ret = overwrite_Dialog.exec_()
                    if ret == QtGui.QMessageBox.Yes:
                        names_saved[ids_saved.index(entry)] = self.names[self.ids.index(entry)]
                        packages_saved[ids_saved.index(entry)] = self.packages[self.ids.index(entry)]
                    if ret == QtGui.QMessageBox.YesAll:
                        all_yes = True
                        names_saved[ids_saved.index(entry)] = self.names[self.ids.index(entry)]
                        packages_saved[ids_saved.index(entry)] = self.packages[self.ids.index(entry)]
                    if ret == QtGui.QMessageBox.NoAll:
                        all_yes = True
                else:
                    ids_saved.append(entry)
                    names_saved.append(self.names[self.ids.index(entry)])
                    packages_saved.append(self.packages[self.ids.index(entry)])
            save_file.close()
            save_file = open(file[0], 'wb')
            pickle.dump(names_saved, save_file)
            pickle.dump(ids_saved, save_file)
            pickle.dump(packages_saved, save_file)
            save_file.close()
        self.accept()