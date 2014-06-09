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
    self.lineedit_Package = QtGui.QLineEdit()
    self.label_Genetate_on = QtGui.QLabel(self.tr('Can generate on:'))
    self.combobox_Generate_on = QtGui.QComboBox()
    self.combobox_Generate_on.setEditable(True)
    self.button_add_block = QtGui.QPushButton(self.tr('+'))
    self.button_remove_block = QtGui.QPushButton(self.tr('-'))
    self.list_Generate_on = QtGui.QListWidget()

    self.group_options = QtGui.QGroupBox(self.tr('Options'))
    self.label_check_points = QtGui.QLabel(self.tr('Where to check wether Structure can be placed or not'))
    self.combobox_check_points = QtGui.QComboBox()
    self.label_offset = QtGui.QLabel(self.tr('Height offset'))
    self.spinbox_offset = QtGui.QSpinBox()
    self.checkbox_Generate_Air = QtGui.QCheckBox(self.tr('Do not generate Air'))

    self.group_rotation = QtGui.QGroupBox(self.tr('Rotaton'))
    self.checkbox_rotation_1 = QtGui.QCheckBox(self.tr('Default Rotation'))
    self.checkbox_rotation_2 = QtGui.QCheckBox(self.tr('Rotation by 90 degrees'))
    self.checkbox_rotation_3 = QtGui.QCheckBox(self.tr('Rotation by 180 degrees'))
    self.checkbox_rotation_4 = QtGui.QCheckBox(self.tr('Rotation by 270 degrees'))

    self.button_Start = QtGui.QPushButton(self.tr('Start'))

def layout(self):
    layoutgroupoptions = QtGui.QGridLayout()

    layoutgroupoptions.addWidget(self.checkbox_Generate_Air, 0, 0, 1, 1)
    layoutgroupoptions.addWidget(self.label_check_points, 1, 0, 1, 2)
    layoutgroupoptions.addWidget(self.combobox_check_points, 2, 0, 1, 2)
    layoutgroupoptions.addWidget(self.label_offset, 3, 0, 1, 1)
    layoutgroupoptions.addWidget(self.spinbox_offset, 3, 1, 1, 1)

    self.group_options.setLayout(layoutgroupoptions)

    layoutgrouprotation = QtGui.QVBoxLayout()

    layoutgrouprotation.addWidget(self.checkbox_rotation_1)
    layoutgrouprotation.addWidget(self.checkbox_rotation_2)
    layoutgrouprotation.addWidget(self.checkbox_rotation_3)
    layoutgrouprotation.addWidget(self.checkbox_rotation_4)

    self.group_rotation.setLayout(layoutgrouprotation)

    widgetZentral = QtGui.QWidget()
    layoutZentral = QtGui.QGridLayout()
    layoutZentral.addWidget(self.label_File_in_Path, 0, 0, 1, 1)
    layoutZentral.addWidget(self.lineedit_File_in_Path, 1, 0, 1, 5)
    layoutZentral.addWidget(self.button_File_in, 1, 5, 1, 1)
    layoutZentral.addWidget(self.label_File_out_Path, 2, 0, 1, 1)
    layoutZentral.addWidget(self.lineedit_File_out_Path, 3, 0, 1, 5)
    layoutZentral.addWidget(self.button_File_out, 3, 5, 1, 1)
    layoutZentral.addWidget(self.label_Package, 4, 0, 1, 1)
    layoutZentral.addWidget(self.lineedit_Package, 5, 0, 1, 5)
    layoutZentral.addWidget(self.label_Genetate_on, 6, 0, 1, 1)
    layoutZentral.addWidget(self.combobox_Generate_on, 7, 0, 1, 4)
    layoutZentral.addWidget(self.button_add_block, 7, 4, 1, 1)
    layoutZentral.addWidget(self.button_remove_block, 7, 5, 1, 1)
    layoutZentral.addWidget(self.list_Generate_on, 8, 0, 1, 6)
    layoutZentral.addWidget(self.group_options, 9, 0, 1, 2)
    layoutZentral.addWidget(self.group_rotation, 9, 2, 1, 4)
    layoutZentral.addWidget(self.button_Start, 10, 0, 1, 6)

    widgetZentral.setLayout(layoutZentral)
    self.setCentralWidget(widgetZentral)

def tooltipsinit(self):
    self.lineedit_File_in_Path.setToolTip(self.tr('Enter the path to the .schematic file you want to convert or press \"Browse...\" to select a file.'))
    self.button_File_in.setToolTip(self.tr('Opens a window where you can select a .schematic file.'))
    self.lineedit_File_out_Path.setToolTip(self.tr('Enter the path where the .java file should be outputted to or press \"Browse...\" to select a destination.\nNotice that the class name depends on the name of the output file.'))
    self.button_File_out.setToolTip(self.tr('Opens a window where you can select a destination for the outputed .java file.'))
    self.lineedit_Package.setToolTip(self.tr('Enter the package name where your .java file will be in your mod.\nUsually looks like yourname.modname.'))
    self.checkbox_Generate_Air.setToolTip(self.tr('When enabled all the air blocks in the structure will be ignored.'))
    self.combobox_Generate_on.setToolTip(self.tr('Select or enter blocks on which the structure can generate.\nPress \"+\" to add your block to the list below.\nNotice that only blocks in the list will be added to the valid spawn blocks.'))
    self.button_add_block.setToolTip(self.tr('Adds the current block from the box on the left to the list below.'))
    self.button_remove_block.setToolTip(self.tr('Removes the selected item from the list below.'))
    self.list_Generate_on.setToolTip(self.tr('List of blocks considered as valid spawn blocks.'))
    self.combobox_check_points.setToolTip(self.tr('Sets where the function will look for the blocks selected above.\nCorners is recommended.'))
    self.spinbox_offset.setToolTip(self.tr('Set a height offset for your structure to make it fly or sink into the ground'))
    self.checkbox_rotation_1.setToolTip(self.tr('If checked the Structure will be spawn unrotated.\nIf you select multiple rotations the rotation will be decided randomly every time the structure is generated,\nwhich rotation to choose.'))
    self.checkbox_rotation_2.setToolTip(self.tr('If checked the Structure will be spawn rotated by 90 degrees.\nIf you select multiple rotations the rotation will be decided randomly every time the structure is generated,\nwhich rotation to choose.'))
    self.checkbox_rotation_3.setToolTip(self.tr('If checked the Structure will be spawn rotated by 180 degrees.\nIf you select multiple rotations the rotation will be decided randomly every time the structure is generated,\nwhich rotation to choose.'))
    self.checkbox_rotation_4.setToolTip(self.tr('If checked the Structure will be spawn rotated by 270 degrees.\nIf you select multiple rotations the rotation will be decided randomly every time the structure is generated,\nwhich rotation to choose.'))
    self.button_Start.setToolTip(self.tr('Starts the converting process.'))
    self.setToolTip(self.tr('Schematic to Java Structure by jajo_11 inspired by "MITHION\'S .SCHEMATIC TO JAVA CONVERTING TOOL"'))

def preinit(self):
    self.lineedit_Package.setPlaceholderText('yourname.modname')
    self.spinbox_offset.setRange( -255, 255)
    self.combobox_check_points.addItems(['Corners', 'Center', 'Everywhere'])
    self.combobox_Generate_on.addItems([u'Blocks.air', u'Blocks.stone', u'Blocks.grass', u'Blocks.dirt', u'Blocks.cobblestone', u'Blocks.planks', u'Blocks.sapling', u'Blocks.bedrock', u'Blocks.flowing_water', u'Blocks.water', u'Blocks.flowing_lava', u'Blocks.lava', u'Blocks.sand', u'Blocks.gravel', u'Blocks.gold_ore', u'Blocks.iron_ore', u'Blocks.coal_ore', u'Blocks.log', u'Blocks.leaves', u'Blocks.sponge', u'Blocks.glass', u'Blocks.lapis_ore', u'Blocks.lapis_block', u'Blocks.dispenser', u'Blocks.sandstone', u'Blocks.note', u'Blocks.bed', u'Blocks.golden_rail', u'Blocks.detector_rail', u'Blocks.sticky_piston', u'Blocks.web', u'Blocks.tallgrass', u'Blocks.deadbush', u'Blocks.piston', u'Blocks.piston_head', u'Blocks.wool', u'Blocks.piston_extension', u'Blocks.yellow_flower', u'Blocks.red_flower', u'Blocks.brown_mushroom', u'Blocks.red_mushroom', u'Blocks.gold_block', u'Blocks.iron_block', u'Blocks.double_stone_slab', u'Blocks.stone_slab', u'Blocks.brick_block', u'Blocks.tnt', u'Blocks.bookshelf', u'Blocks.mossy_cobblestone', u'Blocks.obsidian', u'Blocks.torch', u'Blocks.fire', u'Blocks.mob_spawner', u'Blocks.oak_stairs', u'Blocks.chest', u'Blocks.redstone_wire', u'Blocks.diamond_ore', u'Blocks.diamond_block', u'Blocks.crafting_table', u'Blocks.wheat', u'Blocks.farmland', u'Blocks.furnace', u'Blocks.lit_furnace', u'Blocks.standing_sign', u'Blocks.wooden_door', u'Blocks.ladder', u'Blocks.rail', u'Blocks.stone_stairs', u'Blocks.wall_sign', u'Blocks.lever', u'Blocks.stone_pressure_plate', u'Blocks.iron_door', u'Blocks.wooden_pressure_plate', u'Blocks.redstone_ore', u'Blocks.lit_redstone_ore', u'Blocks.unlit_redstone_torch', u'Blocks.redstone_torch', u'Blocks.stone_button', u'Blocks.snow_layer', u'Blocks.ice', u'Blocks.snow', u'Blocks.cactus', u'Blocks.clay', u'Blocks.reeds', u'Blocks.jukebox', u'Blocks.fence', u'Blocks.pumpkin', u'Blocks.netherrack', u'Blocks.soul_sand', u'Blocks.glowstone', u'Blocks.portal', u'Blocks.lit_pumpkin', u'Blocks.cake', u'Blocks.unpowered_repeater', u'Blocks.powered_repeater', u'Blocks.stained_glass', u'Blocks.trapdoor', u'Blocks.monster_egg', u'Blocks.stonebrick', u'Blocks.brown_mushroom_block', u'Blocks.red_mushroom_block', u'Blocks.iron_bars', u'Blocks.glass_pane', u'Blocks.melon_block', u'Blocks.pumpkin_stem', u'Blocks.melon_stem', u'Blocks.vine', u'Blocks.fence_gate', u'Blocks.brick_stairs', u'Blocks.stone_brick_stairs', u'Blocks.Myceliummycelium', u'Blocks.waterlily', u'Blocks.nether_brick', u'Blocks.nether_brick_fence', u'Blocks.nether_brick_stairs', u'Blocks.nether_wart', u'Blocks.enchanting_table', u'Blocks.brewing_stand', u'Blocks.cauldron', u'Blocks.end_portal', u'Blocks.end_portal_frame', u'Blocks.end_stone', u'Blocks.dragon_egg', u'Blocks.redstone_lamp', u'Blocks.lit_redstone_lamp', u'Blocks.double_wooden_slab', u'Blocks.wooden_slab', u'Blocks.cocoa', u'Blocks.sandstone_stairs', u'Blocks.emerald_ore', u'Blocks.ender_chest', u'Blocks.tripwire_hook', u'Blocks.tripwire', u'Blocks.emerald_block', u'Blocks.spruce_stairs', u'Blocks.birch_stairs', u'Blocks.jungle_stairs', u'Blocks.command_block', u'Blocks.beacon', u'Blocks.cobblestone_wall', u'Blocks.flower_pot', u'Blocks.carrots', u'Blocks.potatoes', u'Blocks.wooden_button', u'Blocks.skull', u'Blocks.anvil', u'Blocks.trapped_chest', u'Blocks.light_weighted_pressure_plate', u'Blocks.heavy_weighted_pressure_plate', u'Blocks.unpowered_comparator', u'Blocks.powered_comparator', u'Blocks.daylight_detector', u'Blocks.redstone_block', u'Blocks.quartz_ore', u'Blocks.hopper', u'Blocks.quartz_block', u'Blocks.quartz_stairs', u'Blocks.activator_rail', u'Blocks.dropper', u'Blocks.stained_hardened_clay', u'Blocks.stained_glass', u'Blocks.log2', u'Blocks.acacia_stairs', u'Blocks.dark_oak_stairs', u'Blocks.slime_block', u'Blocks.barrier', u'Blocks.iron_trapdoor', u'Blocks.hay_block', u'Blocks.carpet', u'Blocks.hardened_clay', u'Blocks.coal_block', u'Blocks.packed_ice', u'Blocks.double_plant'])
    self.combobox_Generate_on.setCurrentIndex(self.combobox_Generate_on.findText('Blocks.grass'))
    self.checkbox_rotation_1.setDisabled(True)
    self.checkbox_rotation_1.setChecked(True)

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
        self.label = QtGui.QLabel(self.tr('There is a unknown Block with the id ') + str(self.id) + self.tr(' at x: ') + str(self.x) + self.tr(' y: ') + str(self.y) + self.tr(' z: ') + str(self.z) + self.tr('\n You have to enter a name for the block here.'))
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
    def __init__(self, parent, names, ids):
        super(dialog_custom_Block_save, self).__init__(parent)
        self.names = names
        self.ids = ids
        self.createComponents()
        self.createLayout()
        self.createConnects()
        self.setWindowTitle(self.tr('Save Coustom Block Set'))

    def createComponents(self):
        self.label = QtGui.QLabel(self.tr('There were some unknown blocks in this schematic do you want to save their names for the future?'))
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
        file = QtGui.QFileDialog.getSaveFileName(self, u"Save Custom Block Set", os.path.dirname(os.path.realpath(__file__)) , 'Custom Block Set (*.cbs)')
        if file[0] != '':
            save_file = open(file[0], 'wb')
            pickle.dump(self.names, save_file)
            pickle.dump(self.ids, save_file)
            save_file.close()
        self.accept()

    def filedialog_save_add(self):
        file = QtGui.QFileDialog.getOpenFileName(self, u"Add to Custom Block Set", os.path.dirname(os.path.realpath(__file__)) , 'Custom Block Set (*.cbs)')
        if file[0] != '':
            save_file = open(file[0], 'rb')
            names_saved = []
            ids_saved = []
            all_yes = False
            all_no = False
            names_saved = pickle.load(save_file)
            ids_saved = pickle.load(save_file)
            for entry in self.ids:
                if entry in ids_saved and all_yes == True:
                    names_saved[ids_saved.index(entry)] = self.names[self.ids.index(entry)]
                if entry in ids_saved and all_yes == False and all_no == False:
                    overwrite_Dialog = QtGui.QMessageBox()
                    overwrite_Dialog.setWindowTitle(self.tr('Duplicate ids'))
                    overwrite_Dialog.setText(self.tr('The Block \"' + self.names[self.ids.index(entry)] + '\" alredy exists as \"'  + names_saved[ids_saved.index(entry)] + '\"'))
                    overwrite_Dialog.setInformativeText(self.tr('Do you want to override it?'))
                    overwrite_Dialog.setStandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.NoAll | QtGui.QMessageBox.YesAll | QtGui.QMessageBox.Yes)
                    overwrite_Dialog.setDefaultButton(QtGui.QMessageBox.Yes)
                    overwrite_Dialog.setEscapeButton(QtGui.QMessageBox.No)
                    overwrite_Dialog.setIcon(QtGui.QMessageBox.Question)
                    ret = overwrite_Dialog.exec_()
                    if ret == QtGui.QMessageBox.Yes:
                        names_saved[ids_saved.index(entry)] = self.names[self.ids.index(entry)]
                    if ret == QtGui.QMessageBox.YesAll:
                        all_yes = True
                        names_saved[ids_saved.index(entry)] = self.names[self.ids.index(entry)]
                    if ret == QtGui.QMessageBox.NoAll:
                        all_yes = True
                else:
                    ids_saved.append(entry)
                    names_saved.append(self.names[self.ids.index(entry)])
            save_file.close()
            save_file = open(file[0], 'wb')
            pickle.dump(names_saved, save_file)
            pickle.dump(ids_saved, save_file)
            save_file.close()
        self.accept()