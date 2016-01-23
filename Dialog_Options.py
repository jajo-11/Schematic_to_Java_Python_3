from PySide import QtGui

class Dialog_Options(QtGui.QDialog):
    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)
        self.mcVersion = ""
        self.getTopSolidOrLiquidBlock = False
        self.max_file_length = 1000
        self.file_name_format = '000_Filename'
        self.components()
        self.layout()
        self.tooltipsinit()
        self.createConnects()
        self.setWindowTitle(self.tr('More Options'))

    def components(self):
        self.Group_genneral = QtGui.QGroupBox(self.tr('General'))
        self.Label_Mc_version = QtGui.QLabel(self.tr('Targeted Minecraft Version:'))
        self.ComboBox_Mc_version = QtGui.QComboBox()
        self.Checkbox_getTopSolidBlock = QtGui.QCheckBox(self.tr('Use \"world.getTopSolidOrLiquidBlock\"'))

        self.Group_split_files = QtGui.QGroupBox(self.tr('File Splitting'))
        self.Button_Done = QtGui.QPushButton(self.tr('Done'))
        self.Button_Cancel = QtGui.QPushButton(self.tr('Cancel'))
        self.Label_Max_File_size = QtGui.QLabel(self.tr('Maximal blocks per file:'))
        self.Spinbox_Max_File_size = QtGui.QSpinBox()
        self.Label_File_name_format = QtGui.QLabel(self.tr('File name format:'))
        self.ComboBox_File_name_format = QtGui.QComboBox()

    def layout(self):
        layoutgroup_general = QtGui.QVBoxLayout()

        layoutgroup_general.addWidget(self.Label_Mc_version)
        layoutgroup_general.addWidget(self.ComboBox_Mc_version)
        layoutgroup_general.addWidget(self.Checkbox_getTopSolidBlock)

        self.Group_genneral.setLayout(layoutgroup_general)

        layoutgroup_split_files = QtGui.QGridLayout()

        layoutgroup_split_files.addWidget(self.Label_Max_File_size, 0, 0)
        layoutgroup_split_files.addWidget(self.Spinbox_Max_File_size, 0, 1)
        layoutgroup_split_files.addWidget(self.Label_File_name_format, 1, 0)
        layoutgroup_split_files.addWidget(self.ComboBox_File_name_format, 1, 1)

        self.Group_split_files.setLayout(layoutgroup_split_files)

        layoutzentral = QtGui.QGridLayout()

        layoutzentral.addWidget(self.Group_genneral, 0, 0, 1, 2)
        layoutzentral.addWidget(self.Group_split_files, 1, 0, 1, 2)
        layoutzentral.addWidget(self.Button_Done, 2, 0)
        layoutzentral.addWidget(self.Button_Cancel, 2, 1)

        self.setLayout(layoutzentral)

    def preinit(self):
        print(self.mcVersion)
        self.ComboBox_Mc_version.addItems(['1.7.x'])
        self.ComboBox_Mc_version.setCurrentIndex(self.ComboBox_Mc_version.findText(self.mcVersion))
        self.Checkbox_getTopSolidBlock.setChecked(self.getTopSolidOrLiquidBlock)
        self.Spinbox_Max_File_size.setRange(100, 10000)
        self.Spinbox_Max_File_size.setSingleStep(100)
        self.Spinbox_Max_File_size.setValue(self.max_file_length)
        self.ComboBox_File_name_format.addItems(['000Filename', '000_Filename', '000.Filename', 'Filename000',
                                                 'Filename_000', 'Filename.000'])
        self.ComboBox_File_name_format.setCurrentIndex(self.ComboBox_File_name_format.findText(self.file_name_format))

    def tooltipsinit(self):
        self.Spinbox_Max_File_size.setToolTip(self.tr('The number of "setBlock" lines before starting a new File.'))
        self.ComboBox_File_name_format.setToolTip(self.tr('This sets how your file will be named in case of it' +
                                                          ' exceeding the limit above.'))
        self.Checkbox_getTopSolidBlock.setToolTip(self.tr('Your converted Structures will automatically try to spawn on'
                                                          ' the highest block'))

    def createConnects(self):
        self.Button_Done.clicked.connect(self.accept)
        self.Button_Cancel.clicked.connect(self.reject)