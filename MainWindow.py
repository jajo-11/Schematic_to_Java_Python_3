import pickle, os
from PySide import QtCore, QtGui


def components(self):
    self.label_File_in_Path = QtGui.QLabel(self.tr('Path to .schematic'))
    self.lineedit_File_in_Path = QtGui.QLineEdit()
    self.button_File_in = QtGui.QPushButton(self.tr('Browse...'))
    self.label_File_out_Path = QtGui.QLabel(self.tr('Path to .java'))
    self.lineedit_File_out_Path = QtGui.QLineEdit()
    self.button_File_out = QtGui.QPushButton(self.tr('Browse...'))
    self.label_Package = QtGui.QLabel(self.tr('Package:'))
    self.combobox_Package = QtGui.QComboBox()
    self.label_Genetate_on = QtGui.QLabel(self.tr('Can generate on:'))
    self.combobox_Generate_on = QtGui.QComboBox()
    self.button_add_block = QtGui.QPushButton(self.tr('+'))
    self.button_remove_block = QtGui.QPushButton(self.tr('-'))
    self.list_Generate_on = QtGui.QListWidget()

    self.group_options = QtGui.QGroupBox(self.tr('Options'))
    self.label_check_points = QtGui.QLabel(self.tr('Where to check wether Structure can be placed or not'))
    self.combobox_check_points = QtGui.QComboBox()
    self.label_offset = QtGui.QLabel(self.tr('Height offset'))
    self.spinbox_offset = QtGui.QSpinBox()
    self.checkbox_Generate_Air = QtGui.QCheckBox(self.tr('Do not generate Air'))
    self.button_manage_cbs = QtGui.QPushButton(self.tr('Custom Block Sets'))
    self.button_manage_cl = QtGui.QPushButton(self.tr('Chest Loot'))

    self.group_rotation = QtGui.QGroupBox(self.tr('Rotaton'))
    self.checkbox_rotation_1 = QtGui.QCheckBox(self.tr('Default Rotation'))
    self.checkbox_rotation_2 = QtGui.QCheckBox(self.tr('Rotation by 90 degrees'))
    self.checkbox_rotation_3 = QtGui.QCheckBox(self.tr('Rotation by 180 degrees'))
    self.checkbox_rotation_4 = QtGui.QCheckBox(self.tr('Rotation by 270 degrees'))

    self.button_Start = QtGui.QPushButton(self.tr('Start'))
    self.progressbar_main = QtGui.QProgressBar()


def layout(self):
    layoutgroupoptions = QtGui.QGridLayout()

    layoutgroupoptions.addWidget(self.checkbox_Generate_Air, 0, 0, 1, 1)
    layoutgroupoptions.addWidget(self.label_check_points, 1, 0, 1, 2)
    layoutgroupoptions.addWidget(self.combobox_check_points, 2, 0, 1, 2)
    layoutgroupoptions.addWidget(self.label_offset, 3, 0, 1, 1)
    layoutgroupoptions.addWidget(self.spinbox_offset, 3, 1, 1, 1)
    layoutgroupoptions.addWidget(self.button_manage_cbs, 4, 0, 1, 1)
    layoutgroupoptions.addWidget(self.button_manage_cl, 4, 1, 1, 1)

    self.group_options.setLayout(layoutgroupoptions)

    layoutgrouprotation = QtGui.QVBoxLayout()

    layoutgrouprotation.addWidget(self.checkbox_rotation_1)
    layoutgrouprotation.addWidget(self.checkbox_rotation_2)
    layoutgrouprotation.addWidget(self.checkbox_rotation_3)
    layoutgrouprotation.addWidget(self.checkbox_rotation_4)

    self.group_rotation.setLayout(layoutgrouprotation)

    widgetzentral = QtGui.QWidget()
    layoutzentral = QtGui.QGridLayout()
    layoutzentral.addWidget(self.label_File_in_Path, 0, 0, 1, 1)
    layoutzentral.addWidget(self.lineedit_File_in_Path, 1, 0, 1, 5)
    layoutzentral.addWidget(self.button_File_in, 1, 5, 1, 1)
    layoutzentral.addWidget(self.label_File_out_Path, 2, 0, 1, 1)
    layoutzentral.addWidget(self.lineedit_File_out_Path, 3, 0, 1, 5)
    layoutzentral.addWidget(self.button_File_out, 3, 5, 1, 1)
    layoutzentral.addWidget(self.label_Package, 4, 0, 1, 1)
    layoutzentral.addWidget(self.combobox_Package, 5, 0, 1, 5)
    layoutzentral.addWidget(self.label_Genetate_on, 6, 0, 1, 1)
    layoutzentral.addWidget(self.combobox_Generate_on, 7, 0, 1, 4)
    layoutzentral.addWidget(self.button_add_block, 7, 4, 1, 1)
    layoutzentral.addWidget(self.button_remove_block, 7, 5, 1, 1)
    layoutzentral.addWidget(self.list_Generate_on, 8, 0, 1, 6)
    layoutzentral.addWidget(self.group_options, 9, 0, 1, 2)
    layoutzentral.addWidget(self.group_rotation, 9, 2, 1, 4)
    layoutzentral.addWidget(self.button_Start, 10, 0, 1, 6)
    layoutzentral.addWidget(self.progressbar_main, 10, 0, 1, 6)

    widgetzentral.setLayout(layoutzentral)
    self.setCentralWidget(widgetzentral)


def tooltipsinit(self):
    self.lineedit_File_in_Path.setToolTip(
        self.tr('Enter the path to the .schematic file you want to convert or press \"Browse...\" to select a file.'))
    self.button_File_in.setToolTip(self.tr('Opens a window where you can select a .schematic file.'))
    self.lineedit_File_out_Path.setToolTip(self.tr(
        'Enter the path where the .java file should be outputted to or press \"Browse...\" to select a destination.' +
        '\nNotice that the class name depends on the name of the output file.'))
    self.button_File_out.setToolTip(
        self.tr('Opens a window where you can select a destination for the outputed .java file.'))
    self.combobox_Package.setToolTip(self.tr(
        'Enter the package name where your .java file will be in your mod.\nUsually looks like yourname.modname.\n' +
        'Packages used before will appear here.'))
    self.checkbox_Generate_Air.setToolTip(self.tr('When enabled all the air blocks in the structure will be ignored.'))
    self.combobox_Generate_on.setToolTip(self.tr(
        'Select or enter blocks on which the structure can generate.\nPress \"+\" to add your block to the list' +
        ' below.\nNotice that only blocks in the list will be added to the valid spawn blocks.'))
    self.button_add_block.setToolTip(self.tr('Adds the current block from the box on the left to the list below.'))
    self.button_remove_block.setToolTip(self.tr('Removes the selected item from the list below.'))
    self.list_Generate_on.setToolTip(self.tr('List of blocks considered as valid spawn blocks.'))
    self.combobox_check_points.setToolTip(
        self.tr('Sets where the function will look for the blocks selected above.\nCorners is recommended.'))
    self.spinbox_offset.setToolTip(
        self.tr('Set a height offset for your structure to make it fly or sink into the ground'))
    self.button_manage_cbs.setToolTip(self.tr('Opens a window where you can manage your custom block sets.'))
    self.button_manage_cl.setToolTip(self.tr('Opens a window where you can manage your random chest loot.'))
    self.checkbox_rotation_1.setToolTip(self.tr(
        'If checked the Structure will be spawn unrotated.\nIf you select multiple rotations the rotation will be' +
        ' decided randomly every time the structure is generated,\nwhich rotation to choose.'))
    self.checkbox_rotation_2.setToolTip(self.tr(
        'If checked the Structure will be spawn rotated by 90 degrees.\nIf you select multiple rotations the' +
        ' rotation will be decided randomly every time the structure is generated,\nwhich rotation to choose.'))
    self.checkbox_rotation_3.setToolTip(self.tr(
        'If checked the Structure will be spawn rotated by 180 degrees.\nIf you select multiple rotations the' +
        ' rotation will be decided randomly every time the structure is generated,\nwhich rotation to choose.'))
    self.checkbox_rotation_4.setToolTip(self.tr(
        'If checked the Structure will be spawn rotated by 270 degrees.\nIf you select multiple rotations the' +
        ' rotation will be decided randomly every time the structure is generated,\nwhich rotation to choose.'))
    self.button_Start.setToolTip(self.tr('Starts the converting process.'))
    self.progressbar_main.setToolTip(self.tr('Shows the progress of the conversion of the current file.'))
    self.setToolTip(
        self.tr('Schematic to Java Structure by jajo_11 inspired by "MITHION\'S .SCHEMATIC TO JAVA CONVERTING TOOL"'))


def preinit(self):
    self.combobox_Generate_on.setEditable(True)
    self.combobox_Package.setEditable(True)
    if os.path.isfile('options') and os.path.getsize('options') > 0:
        packages_file = open('options', 'rb')
        packages = pickle.load(packages_file)
        packages_file.close()
        self.combobox_Package.addItems(packages)
    else:
        packages_file = open('options', 'wb')
        packages = []
        pickle.dump(packages, packages_file)
        packages_file.close()
    self.combobox_Package.addItem('yourname.modname')
    self.spinbox_offset.setRange(-255, 255)
    self.combobox_check_points.addItems(['Corners', 'Center', 'Everywhere'])
    self.combobox_Generate_on.addItems(
        ['Blocks.air', 'Blocks.stone', 'Blocks.grass', 'Blocks.dirt', 'Blocks.cobblestone', 'Blocks.planks',
         'Blocks.sapling', 'Blocks.bedrock', 'Blocks.flowing_water', 'Blocks.water', 'Blocks.flowing_lava',
         'Blocks.lava', 'Blocks.sand', 'Blocks.gravel', 'Blocks.gold_ore', 'Blocks.iron_ore', 'Blocks.coal_ore',
         'Blocks.log', 'Blocks.leaves', 'Blocks.sponge', 'Blocks.glass', 'Blocks.lapis_ore', 'Blocks.lapis_block',
         'Blocks.dispenser', 'Blocks.sandstone', 'Blocks.note', 'Blocks.bed', 'Blocks.golden_rail',
         'Blocks.detector_rail', 'Blocks.sticky_piston', 'Blocks.web', 'Blocks.tallgrass', 'Blocks.deadbush',
         'Blocks.piston', 'Blocks.piston_head', 'Blocks.wool', 'Blocks.piston_extension', 'Blocks.yellow_flower',
         'Blocks.red_flower', 'Blocks.brown_mushroom', 'Blocks.red_mushroom', 'Blocks.gold_block', 'Blocks.iron_block',
         'Blocks.double_stone_slab', 'Blocks.stone_slab', 'Blocks.brick_block', 'Blocks.tnt', 'Blocks.bookshelf',
         'Blocks.mossy_cobblestone', 'Blocks.obsidian', 'Blocks.torch', 'Blocks.fire', 'Blocks.mob_spawner',
         'Blocks.oak_stairs', 'Blocks.chest', 'Blocks.redstone_wire', 'Blocks.diamond_ore', 'Blocks.diamond_block',
         'Blocks.crafting_table', 'Blocks.wheat', 'Blocks.farmland', 'Blocks.furnace', 'Blocks.lit_furnace',
         'Blocks.standing_sign', 'Blocks.wooden_door', 'Blocks.ladder', 'Blocks.rail', 'Blocks.stone_stairs',
         'Blocks.wall_sign', 'Blocks.lever', 'Blocks.stone_pressure_plate', 'Blocks.iron_door',
         'Blocks.wooden_pressure_plate', 'Blocks.redstone_ore', 'Blocks.lit_redstone_ore',
         'Blocks.unlit_redstone_torch', 'Blocks.redstone_torch', 'Blocks.stone_button', 'Blocks.snow_layer',
         'Blocks.ice', 'Blocks.snow', 'Blocks.cactus', 'Blocks.clay', 'Blocks.reeds', 'Blocks.jukebox', 'Blocks.fence',
         'Blocks.pumpkin', 'Blocks.netherrack', 'Blocks.soul_sand', 'Blocks.glowstone', 'Blocks.portal',
         'Blocks.lit_pumpkin', 'Blocks.cake', 'Blocks.unpowered_repeater', 'Blocks.powered_repeater',
         'Blocks.stained_glass', 'Blocks.trapdoor', 'Blocks.monster_egg', 'Blocks.stonebrick',
         'Blocks.brown_mushroom_block', 'Blocks.red_mushroom_block', 'Blocks.iron_bars', 'Blocks.glass_pane',
         'Blocks.melon_block', 'Blocks.pumpkin_stem', 'Blocks.melon_stem', 'Blocks.vine', 'Blocks.fence_gate',
         'Blocks.brick_stairs', 'Blocks.stone_brick_stairs', 'Blocks.mycelium', 'Blocks.waterlily',
         'Blocks.nether_brick', 'Blocks.nether_brick_fence', 'Blocks.nether_brick_stairs', 'Blocks.nether_wart',
         'Blocks.enchanting_table', 'Blocks.brewing_stand', 'Blocks.cauldron', 'Blocks.end_portal',
         'Blocks.end_portal_frame', 'Blocks.end_stone', 'Blocks.dragon_egg', 'Blocks.redstone_lamp',
         'Blocks.lit_redstone_lamp', 'Blocks.double_wooden_slab', 'Blocks.wooden_slab', 'Blocks.cocoa',
         'Blocks.sandstone_stairs', 'Blocks.emerald_ore', 'Blocks.ender_chest', 'Blocks.tripwire_hook',
         'Blocks.tripwire', 'Blocks.emerald_block', 'Blocks.spruce_stairs', 'Blocks.birch_stairs',
         'Blocks.jungle_stairs', 'Blocks.command_block', 'Blocks.beacon', 'Blocks.cobblestone_wall',
         'Blocks.flower_pot', 'Blocks.carrots', 'Blocks.potatoes', 'Blocks.wooden_button', 'Blocks.skull',
         'Blocks.anvil', 'Blocks.trapped_chest', 'Blocks.light_weighted_pressure_plate',
         'Blocks.heavy_weighted_pressure_plate', 'Blocks.unpowered_comparator', 'Blocks.powered_comparator',
         'Blocks.daylight_detector', 'Blocks.redstone_block', 'Blocks.quartz_ore', 'Blocks.hopper',
         'Blocks.quartz_block', 'Blocks.quartz_stairs', 'Blocks.activator_rail', 'Blocks.dropper',
         'Blocks.stained_hardened_clay', 'Blocks.stained_glass', 'Blocks.log2', 'Blocks.acacia_stairs',
         'Blocks.dark_oak_stairs', 'Blocks.slime_block', 'Blocks.barrier', 'Blocks.iron_trapdoor', 'Blocks.hay_block',
         'Blocks.carpet', 'Blocks.hardened_clay', 'Blocks.coal_block', 'Blocks.packed_ice', 'Blocks.double_plant'])
    self.combobox_Generate_on.setCurrentIndex(self.combobox_Generate_on.findText('Blocks.grass'))
    self.checkbox_rotation_1.setDisabled(True)
    self.checkbox_rotation_1.setChecked(True)
    self.button_manage_cl.setDisabled(True)
    self.progressbar_main.setVisible(False)
    self.progressbar_main.setAlignment(QtCore.Qt.AlignCenter)


def save_package(self):
    packages_file = open('options', 'rb')
    packages = pickle.load(packages_file)
    packages_file.close()
    packages_file = open('options', 'wb')
    if self.combobox_Package.currentText() not in packages and self.combobox_Package.currentText() != 'yourname.modname':
        packages.append(self.combobox_Package.currentText())
        pickle.dump(packages, packages_file)
    packages_file.close()


class dialog_custom_Block(QtGui.QDialog):
    def __init__(self, parent, x, y, z, id):
        super(dialog_custom_Block, self).__init__(parent)
        self.x = x
        self.y = y
        self.z = z
        self.id = id
        self.createComponents()
        self.createLayout()
        self.createInfo()
        self.createConnects()
        self.setWindowTitle(self.tr('Custom Block Name'))

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
        self.lineedit.setToolTip(self.tr('Insert package here (looks similar this: Yourname.ModName.ModName)'))

    def createConnects(self):
        self.button_done.clicked.connect(self.accept)

    @property
    def input_name(self):
        return self.lineedit.text()

    @property
    def input_package(self):
        return self.lineedit_package.text()


class dialog_custom_Block_save(QtGui.QDialog):
    def __init__(self, parent, names, ids, packages):
        super(dialog_custom_Block_save, self).__init__(parent)
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
                        QtGui.QMessageBox.No | QtGui.QMessageBox.NoAll | QtGui.QMessageBox.YesAll | QtGui.QMessageBox.Yes)
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


class dialog_custom_Block_manage(QtGui.QDialog):
    def __init__(self, parent):
        super(dialog_custom_Block_manage, self).__init__(parent)
        self.current_names = []
        self.current_ids = []
        self.current_packages = []
        self.customFile = ''
        self.createComponents()
        self.createLayout()
        self.tooltips()
        self.preinit()
        self.list_blocks_in_table()
        self.createConnects()
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
        if not os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + '/customblocksets'):
            os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/customblocksets')
        for file in os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/customblocksets'):
            if file.endswith('.cbs'):
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