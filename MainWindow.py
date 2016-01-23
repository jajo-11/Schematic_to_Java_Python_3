import pickle, os
from PySide import QtCore, QtGui
from Options_Provider import OptionsProvider


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
    self.button_more_options = QtGui.QPushButton(self.tr('More Options'))

    self.group_rotation = QtGui.QGroupBox(self.tr('Rotaton'))
    self.checkbox_rotation_1 = QtGui.QCheckBox(self.tr('Default Rotation'))
    self.checkbox_rotation_2 = QtGui.QCheckBox(self.tr('Rotation by 90 degrees'))
    self.checkbox_rotation_3 = QtGui.QCheckBox(self.tr('Rotation by 180 degrees'))
    self.checkbox_rotation_4 = QtGui.QCheckBox(self.tr('Rotation by 270 degrees'))

    self.button_Start = QtGui.QPushButton(self.tr('Start'))
    self.progressbar_main = QtGui.QProgressBar()

def layout(self):
    layoutgroupoptions = QtGui.QGridLayout()

    layoutgroupoptions.addWidget(self.label_check_points, 0, 0, 1, 2)
    layoutgroupoptions.addWidget(self.combobox_check_points, 1, 0, 1, 2)
    layoutgroupoptions.addWidget(self.label_offset, 2, 0, 1, 1)
    layoutgroupoptions.addWidget(self.spinbox_offset, 2, 1, 1, 1)
    layoutgroupoptions.addWidget(self.button_manage_cbs, 3, 0, 1, 1)
    layoutgroupoptions.addWidget(self.button_manage_cl, 3, 1, 1, 1)
    layoutgroupoptions.addWidget(self.checkbox_Generate_Air, 4, 0, 1, 1)
    layoutgroupoptions.addWidget(self.button_more_options, 4, 1, 1, 1)

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
    self.button_more_options.setToolTip(self.tr('Opens a dialog to set things like a maximum file size.'))
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
    self.combobox_Package.addItems(self.option.get('package'))
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