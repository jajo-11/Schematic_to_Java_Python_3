from PySide import QtGui

class Dialog_Custom_Block(QtGui.QDialog):
    def __init__(self, parent, x, y, z, id, name):
        super(Dialog_Custom_Block, self).__init__(parent)
        self.x = x
        self.y = y
        self.z = z
        self.id = id
        self.createComponents()
        self.createLayout()
        self.createInfo()
        self.createConnects()
        self.setWindowTitle(self.tr('Unknown Block ' + name))

    def createComponents(self):
        self.label = QtGui.QLabel(
            self.tr('There is a unknown Block with the id ') + str(self.id) + self.tr(' at x: ') + str(
                self.x) + self.tr(' y: ') + str(self.y) + self.tr(' z: ') + str(self.z) + self.tr(
                '\n You have to enter a name for the block here.'))
        self.lineedit = QtGui.QLineEdit()
        self.label_package = QtGui.QLabel(self.tr('Name of the Package where the block is registerd:'))
        self.lineedit_package = QtGui.QLineEdit()
        self.button_done = QtGui.QPushButton(self.tr('Done'))

    def createLayout(self):
        layoutDialog = QtGui.QVBoxLayout()
        layoutDialog.addWidget(self.label)
        layoutDialog.addWidget(self.lineedit)
        layoutDialog.addWidget(self.label_package)
        layoutDialog.addWidget(self.lineedit_package)
        layoutDialog.addWidget(self.button_done)
        self.setLayout(layoutDialog)

    def createInfo(self):
        self.lineedit.setPlaceholderText(self.tr('Modname.BlockName'))
        self.lineedit.setToolTip(self.tr('Insert block name here (looks similar this: Modname.BlockName)'))
        self.lineedit_package.setPlaceholderText(self.tr('Yourname.ModName.ModName'))
        self.lineedit_package.setToolTip(self.tr('Insert package here (looks similar this: Yourname.ModName.ModName)'))

    def createConnects(self):
        self.button_done.clicked.connect(self.accept)

    @property
    def input_name(self):
        return self.lineedit.text()

    @property
    def input_package(self):
        return self.lineedit_package.text()