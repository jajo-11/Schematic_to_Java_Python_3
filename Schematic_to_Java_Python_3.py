#!/usr/bin/python

import gzip
import sys

from MainWindow import *
from Metadatarotation import rotate_meta_data
from Options_Provider import OptionsProvider

DEBUGGING = True


class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args):

        self.generate_on = []
        self.cbs_file = None

        self.height = 0
        self.width = 0
        self.length = 0

        self.option = OptionsProvider()

        self.option.new_option('getTopSolidOrLiquidBlock', False)
        self.option.new_option('max_file_length', 1000)
        self.option.new_option('file_name_format', '000_Filename')
        self.option.new_option('mcVersion', '1.7.x')
        self.option.new_option('package', ['yourname.modname'])

        # actually its file x of x files in a format like this (1/10) as string for the progressbar text
        self.number_of_files = '(x/x)'

        QtGui.QMainWindow.__init__(self, *args)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        components(self)
        layout(self)
        tooltipsinit(self)
        preinit(self)
        self.createconnects()
        self.setWindowTitle(self.tr('Schematic to Structure Converter'))

    def createconnects(self):
        self.button_File_in.clicked.connect(self.file_dialog_in)
        self.button_File_out.clicked.connect(self.file_dialog_out)
        self.button_add_block.clicked.connect(self.add_to_list)
        self.button_remove_block.clicked.connect(self.remove_from_list)
        self.button_Start.clicked.connect(self.convert_checker)
        self.button_manage_cbs.clicked.connect(self.open_manage_cbs)
        self.button_more_options.clicked.connect(self.more_options)
        self.checkbox_rotation_1.stateChanged.connect(self.activate_checkbox_1)
        self.checkbox_rotation_2.stateChanged.connect(self.activate_checkbox_1)
        self.checkbox_rotation_3.stateChanged.connect(self.activate_checkbox_1)
        self.checkbox_rotation_4.stateChanged.connect(self.activate_checkbox_1)

    def activate_checkbox_1(self):
        if (self.checkbox_rotation_2.isChecked() or self.checkbox_rotation_3.isChecked() or
                self.checkbox_rotation_4.isChecked()):
            self.checkbox_rotation_1.setDisabled(False)
        else:
            self.checkbox_rotation_1.setDisabled(True)
            self.checkbox_rotation_1.setChecked(True)

    def file_dialog_in(self):
        file = QtGui.QFileDialog.getOpenFileNames(self, u"Open File", QtGui.QDesktopServices.storageLocation(
            QtGui.QDesktopServices.DesktopLocation), 'Schematics (*.schematic)')
        if file[0]:
            file_string = ''
            for paths in file[0]:
                file_string = file_string + '"' + paths + '" '
            self.lineedit_File_in_Path.setText(file_string)
            if self.lineedit_File_out_Path.text() == '':
                path = ''
                for paths in file[0]:
                    path = path + '"' + paths.rstrip('schematic') + 'java' + '" '
                self.lineedit_File_out_Path.setText(path)

    def file_dialog_out(self):
        file = QtGui.QFileDialog.getSaveFileName(self, u"Save File", QtGui.QDesktopServices.storageLocation(
            QtGui.QDesktopServices.DesktopLocation), 'Java (*.java)')
        if file[0]:
            self.lineedit_File_out_Path.setText(file[0])

    def add_to_list(self):
        if self.combobox_Generate_on.currentText() not in self.generate_on:
            self.list_Generate_on.addItem(self.combobox_Generate_on.currentText())
            self.generate_on.append(self.combobox_Generate_on.currentText())

    def remove_from_list(self):
        if self.list_Generate_on.currentItem() is not None:
            self.generate_on.remove(self.list_Generate_on.currentItem().text())
        self.list_Generate_on.takeItem(self.list_Generate_on.currentRow())

    def open_manage_cbs(self):
        dialog = dialog_custom_Block_manage(self)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.cbs_file = dialog.selected

    def more_options(self):
        dialog = dialog_options(self)
        dialog.mcVersion = self.option.get('mcVersion')
        dialog.getTopSolidOrLiquidBlock = self.option.get('getTopSolidOrLiquidBlock')
        dialog.max_file_length = self.option.get('max_file_length')
        dialog.file_name_format = self.option.get('file_name_format')
        dialog.preinit()
        result = dialog.exec()
        if result == QtGui.QDialog.Accepted:
            self.option.set('mcVersion', dialog.ComboBox_Mc_version.currentText())
            self.option.set('getTopSolidOrLiquidBlock', dialog.Checkbox_getTopSolidBlock.isChecked())
            self.option.set('max_file_length', dialog.Spinbox_Max_File_size.value())
            self.option.set('file_name_format', dialog.ComboBox_File_name_format.currentText())

    def convert_checker(self):

        # preaparing a list of all files to convert
        file_list_in = self.lineedit_File_in_Path.text().rstrip('" ').lstrip('" ').split('" "')
        file_list_out = self.lineedit_File_out_Path.text().rstrip('" ').lstrip('" ').split('" "')

        if file_list_in == ['']:
            QtGui.QMessageBox.warning(self, self.tr('Error'), self.tr('No File Selected!'))
        elif file_list_in == file_list_out:
            QtGui.QMessageBox.warning(self, self.tr('Error'), self.tr('In and Output are identical'))
        elif not self.generate_on:
            QtGui.QMessageBox.warning(self, self.tr('Error'), self.tr('No blocks to generate on set!'))
        else:
            if len(file_list_in) != len(file_list_out):
                if len(file_list_in) != 1:
                    for file in range(0, len(file_list_in)):
                        if not file_list_out[file]:
                            file_list_out[file] = file_list_in[file].rstrip('schematic') + 'java'
                            if file == 0:
                                self.lineedit_File_out_Path.setText(self.lineedit_File_out_Path.text() +
                                                                    file_list_out[file])
                            else:
                                self.lineedit_File_out_Path.setText(self.lineedit_File_out_Path.text() +
                                                                    ' "' + file_list_out[file]) + '"'
                else:
                    file_list_out[0] = file_list_in[0].rstrip('schematic') + 'java'
                    self.lineedit_File_out_Path.setText(file_list_in[0])
            self.button_Start.setVisible(False)
            self.progressbar_main.setVisible(True)
            self.progressbar_main.setMaximum(len(file_list_in) * 100)
            self.progressbar_main.setValue(0)
            for file in range(0, len(file_list_in)):
                self.number_of_files = '(' + str(file + 1) + '/' + str(len(file_list_in)) + ')'
                self.convert(file_list_in[file], file_list_out[file])
            self.done()

    def convert(self, arg_file_in, arg_file_out):

        # first the tag id of the items in the list and than the list size or a zero for tag compounds
        tag_container = [[0, 0]]

        # array with all the blocks and corresponding meta data
        block_list = bytearray()
        meta_data_list = bytearray()

        # height, length and width of the structure saved as a short in the schematic (2 bytes long)
        self.height = 0
        self.length = 0
        self.width = 0

        # x, y and z of the current block. Size is defined later and is the product of x, y, and z.
        x = 0
        y = 0
        z = 0

        # all the ids in use in Minecraft 1.7 and the corresponding string names
        block_id = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
                    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
                    77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                    101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
                    121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140,
                    141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160,
                    162, 163, 164, 165, 166, 167, 170, 171, 172, 173, 174,
                    175]
        block_name = ['air', 'stone', 'grass', 'dirt', 'cobblestone', 'planks', 'sapling', 'bedrock', 'flowing_water',
                      'water', 'flowing_lava', 'lava', 'sand', 'gravel', 'gold_ore', 'iron_ore', 'coal_ore', 'log',
                      'leaves', 'sponge', 'glass', 'lapis_ore', 'lapis_block', 'dispenser', 'sandstone', 'note', 'bed',
                      'golden_rail', 'detector_rail', 'sticky_piston', 'web', 'tallgrass', 'deadbush', 'piston',
                      'piston_head', 'wool', 'piston_extension', 'yellow_flower', 'red_flower', 'brown_mushroom',
                      'red_mushroom', 'gold_block', 'iron_block', 'double_stone_slab', 'stone_slab', 'brick_block',
                      'tnt', 'bookshelf', 'mossy_cobblestone', 'obsidian', 'torch', 'fire', 'mob_spawner', 'oak_stairs',
                      'chest', 'redstone_wire', 'diamond_ore', 'diamond_block', 'crafting_table', 'red_mushroom',
                      'farmland', 'furnace', 'lit_furnace', 'standing_sign', 'wooden_door', 'ladder', 'rail',
                      'stone_stairs', 'wall_sign', 'lever', 'stone_pressure_plate', 'iron_door',
                      'wooden_pressure_plate', 'redstone_ore', 'lit_redstone_ore', 'unlit_redstone_torch',
                      'redstone_torch', 'stone_button', 'snow_layer', 'ice', 'snow', 'cactus', 'clay', 'reeds',
                      'jukebox', 'fence', 'pumpkin', 'netherrack', 'soul_sand', 'glowstone', 'portal', 'lit_pumpkin',
                      'cake', 'unpowered_repeater', 'powered_repeater', 'stained_glass', 'trapdoor', 'monster_egg',
                      'stonebrick', 'brown_mushroom_block', 'red_mushroom_block', 'iron_bars', 'glass_pane',
                      'melon_block', 'pumpkin_stem', 'melon_stem', 'vine', 'fence_gate', 'brick_stairs',
                      'stone_brick_stairs', 'Myceliummycelium', 'waterlily', 'nether_brick', 'nether_brick_fence',
                      'nether_brick_stairs', 'nether_wart', 'enchanting_table', 'brewing_stand', 'cauldron',
                      'end_portal', 'end_portal_frame', 'end_stone', 'dragon_egg', 'redstone_lamp', 'lit_redstone_lamp',
                      'double_wooden_slab', 'wooden_slab', 'cocoa', 'sandstone_stairs', 'emerald_ore', 'ender_chest',
                      'tripwire_hook', 'tripwire', 'emerald_block', 'spruce_stairs', 'birch_stairs', 'jungle_stairs',
                      'command_block', 'beacon', 'cobblestone_wall', 'flower_pot', 'carrots', 'potatoes',
                      'wooden_button', 'skull', 'anvil', 'trapped_chest', 'light_weighted_pressure_plate',
                      'heavy_weighted_pressure_plate', 'unpowered_comparator', 'powered_comparator',
                      'daylight_detector', 'redstone_block', 'quartz_ore', 'hopper', 'quartz_block', 'quartz_stairs',
                      'activator_rail', 'dropper', 'stained_hardened_clay', 'stained_glass', 'log2', 'acacia_stairs',
                      'dark_oak_stairs', 'slime_block', 'barrier', 'iron_trapdoor', 'hay_block', 'carpet',
                      'hardened_clay', 'coal_block', 'packed_ice',
                      'double_plant']

        # all the blocks that have to be placed last because they could drop as an item instantly
        non_solid_blocks = ['torch', 'ladder', 'wall_sign', 'lever', 'unlit_redstone_torch', 'redstone_torch',
                            'stone_button']

        # a list of all the lines to spawn in the blocks from the list non_solid_blocks
        blocks_placed_last = []

        g = 0  # counts up to 1500 to split the methode
        c = 1  # counts the total number of "setblock" methodes
        file_counter = 0  # counts the total number of files

        # rotation
        rotations = []  # list contains checked rotations
        rotations_count = 0  # counts the total items in rotations[]
        blocks_to_rotate = [50, 75, 76, 17, 53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 162, 164, 29, 33, 34,
                            69, 77, 143, 63, 68, 23, 170]
        meta_data_rotated = None  # Contains the last metadata rotated by metadata

        # custom blocks
        custom_block = ''  # name of the custom block (modded) handled last
        custom_blocks = []  # contains all the custom block names set by the user
        custom_blocks_id = []  # All the custom ids. Index matching names in custom_blocks list
        custom_blocks_id_cbs = []  # all from the cbs loaded ids
        custom_blocks_cbs = []  # all from the cbs loaded names
        new_custom_block = False  # is set to True if there was an unknown custom block in the schematic

        # additional packages for custom blocks
        additional_packages = []  # list stores all the additional imports for custom blocks
        package = ''  # stores last custom blocks package import
        additional_packages_cbs = []  # all from the cbs loaded packages
        file_out_rew = []  # if the file needs to be rewritten this list will contain all the lines of the file.
        index_imports = 0  # index of the last import line (import net.minecraft.world.gen.feature.WorldGenerator;\n)

        if self.cbs_file is not None:
            if self.cbs_file[0]:
                file = open(os.path.dirname(os.path.realpath(__file__)) + '/customblocksets/' + self.cbs_file[1], 'rb')
            else:
                file = open(self.cbs_file[1])
            custom_blocks_cbs = pickle.load(file)
            custom_blocks_id_cbs = pickle.load(file)
            additional_packages_cbs = pickle.load(file)
            file.close()

        global file_in
        file_in = gzip.open(arg_file_in, 'rb')
        do_not_generate_air = self.checkbox_Generate_Air.isChecked()

        if file_in.read(12) == bytearray.fromhex('0A0009536368656D61746963'):
            debug_print("It's a schematic!")
            self.progressbar_main.setFormat('Reading File (%p%) ' + self.number_of_files)
            debug_print(self.progressbar_main.value())
            self.progressbar_main.setValue(self.progressbar_main.value() + 1)

            while True:

                if tag_container[-1][0] != 0:
                    if tag_container[-1][1] != 0:
                        tag_container[-1][1] -= 1
                        tag = tag_container[-1][0]
                    else:
                        del tag_container[-1]
                        tag = file_in.read(1)
                else:
                    tag = file_in.read(1)

                # TAG_Byte
                if tag == bytearray.fromhex('01'):
                    self.read_tag_name('Byte', tag_container[-1][0])
                    debug_print(int.from_bytes(file_in.read(1), 'big'))
                # TAG_Short
                elif tag == bytearray.fromhex('02'):
                    name = self.read_tag_name('Short', tag_container[-1][0])
                    number = int.from_bytes(file_in.read(2), 'big')
                    debug_print(number)
                    if name == 'Height':
                        self.height = number
                        self.progressbar_main.setValue(self.progressbar_main.value() + 1)
                    elif name == 'Length':
                        self.length = number
                        self.progressbar_main.setValue(self.progressbar_main.value() + 1)
                    elif name == 'Width':
                        self.width = number
                        self.progressbar_main.setValue(self.progressbar_main.value() + 1)
                # TAG_Int
                elif tag == bytearray.fromhex('03'):
                    self.read_tag_name('Int', tag_container[-1][0])
                    debug_print(int.from_bytes(file_in.read(4), 'big'))
                # TAG_Long
                elif tag == bytearray.fromhex('04'):
                    self.read_tag_name('Long', tag_container[-1][0])
                    debug_print(int.from_bytes(file_in.read(8), 'big'))
                # TAG_Float
                elif tag == bytearray.fromhex('05'):
                    self.read_tag_name('Float', tag_container[-1][0])
                    debug_print(int.from_bytes(file_in.read(4), 'big'))
                # TAG_Double
                elif tag == bytearray.fromhex('06'):
                    self.read_tag_name('Double', tag_container[-1][0])
                    debug_print(int.from_bytes(file_in.read(8), 'big'))
                # TAG_Byte_Array
                elif tag == bytearray.fromhex('07'):
                    name = self.read_tag_name('Byte Array', tag_container[-1][0])
                    array_length = int.from_bytes(file_in.read(4), 'big')
                    if name == 'Blocks':
                        block_list = bytearray(file_in.read(array_length))
                        self.progressbar_main.setValue(self.progressbar_main.value() + 3)
                    elif name == 'Data':
                        meta_data_list = bytearray(file_in.read(array_length))
                        self.progressbar_main.setValue(self.progressbar_main.value() + 3)
                    else:
                        file_in.read(array_length)
                    debug_print('Won\'t print Byte Array')
                # TAG_String
                elif tag == bytearray.fromhex('08'):
                    self.read_tag_name('String', tag_container[-1][0])
                    string_length = int.from_bytes(file_in.read(2), 'big')
                    string = bytes.decode(file_in.read(string_length), 'utf-8', 'strict')
                    debug_print(string)
                # TAG_List
                elif tag == bytearray.fromhex('09'):
                    self.read_tag_name('List', tag_container[-1][0])
                    tag_container.append([file_in.read(1), int.from_bytes(file_in.read(4), 'big')])
                    debug_print('Won\'t print list | Tag Id: ' + str(int.from_bytes(tag_container[-1][0], 'big')) +
                                ' | Length: ' + str(tag_container[-1][1]))
                # TAG_Compound
                elif tag == bytearray.fromhex('0A'):
                    self.read_tag_name('Tag Compound', tag_container[-1][0])
                    tag_container.append([0, 0])
                    debug_print('Tag Compounds don\'t have a Value')
                # TAG_End
                elif tag == bytearray.fromhex('00'):
                    if tag_container[-1][0] == 0 and len(tag_container) > 1:
                        del tag_container[-1]
                        debug_print('Tag_Compound End')
                    else:
                        debug_print('End of File')
                        break
                else:
                    debug_print('Well that went unexpectedly...\nUnknown tag type: ' + str(int.from_bytes(tag, 'big')))
                    QtGui.QMessageBox.information(self, self.tr('Error'), self.tr('Well that went unexpectedly...\n' +
                                                                                  'Unknown tag type: ' +
                                                                                  str(int.from_bytes(tag, 'big'))))
                    sys.exit(int.from_bytes(tag, 'big'))

            size = self.height * self.length * self.width  # calculate block count

            debug_print(self.length)
            debug_print(self.width)
            debug_print('Writing file')
            self.progressbar_main.setFormat('Writing File (%p%) ' + self.number_of_files)

            if size > self.option.get('max_file_length'):
                file_out_000 = os.path.dirname(arg_file_out) + '//' + self.option.get('file_name_format').replace(
                    'Filename', os.path.basename(arg_file_out))
            else:
                file_out_000 = arg_file_out

            file_out = open(file_out_000, 'w')

            file_out.write(
                '//Schematic to java Structure by jajo_11 | inspired by "MITHION\'S .SCHEMATIC TO JAVA CONVERTING' +
                'TOOL"\n\npackage ' + self.combobox_Package.currentText() +
                ';\n\nimport java.util.Random;\n' +
                '\nimport net.minecraft.block.Block;\n' +
                'import net.minecraft.block.material.Material;\n' +
                'import net.minecraft.init.Blocks;\n' +
                'import net.minecraft.world.World;\n' +
                'import net.minecraft.world.gen.feature.WorldGenerator;\n\n' +
                'public class ' + os.path.splitext(os.path.basename(arg_file_out))[0] +
                ' extends WorldGenerator\n' +
                '{\n	protected Block[] GetValidSpawnBlocks()\n' +
                '	{\n		return new Block[]\n' +
                '		{\n')

            for block in self.generate_on:
                file_out.write('			' + block + ',\n')

            self.progressbar_main.setValue(self.progressbar_main.value() + 1)

            if self.checkbox_rotation_1.isChecked():
                rotations.append('generate_r0')
            if self.checkbox_rotation_2.isChecked():
                rotations.append('generate_r1')
            if self.checkbox_rotation_3.isChecked():
                rotations.append('generate_r2')
            if self.checkbox_rotation_4.isChecked():
                rotations.append('generate_r3')
            rotations_count = len(rotations)

            file_out.write('		};\n	}\n\n' +
                           '	public boolean LocationIsValidSpawn(World world, int x, int y, int z)\n {\n' +
                           '\n		Block checkBlock = world.getBlock(x, y - 1, z);\n' +
                           '		Block blockAbove = world.getBlock(x, y , z);\n' +
                           '		Block blockBelow = world.getBlock(x, y - 2, z);\n\n' +
                           '		for (Block i : GetValidSpawnBlocks())\n		{\n' +
                           '			if (blockAbove != Blocks.air)\n			{\n' +
                           '				return false;\n			}\n' +
                           '			if (checkBlock == i)\n			{\n				return true;\n			}\n' +
                           '			else if (checkBlock == Blocks.snow_layer && blockBelow == i)\n' +
                           '			{\n				return true;\n			}\n' +
                           '			else if (checkBlock.getMaterial() == Material.plants && blockBelow == i)\n' +
                           '			{\n				return true;\n			}\n		}\n' +
                           '		return false;\n	}\n\n')

            if rotations_count != 1:
                # generates code for random decision of the rotation
                file_out.write('	public boolean generate(World world, Random rand, int x, int y, int z)\n' +
                               '	{\n		int i = rand.nextInt(' + str(rotations_count) + ');\n\n')
                for i in range(0, rotations_count):
                    file_out.write('		if(i == ' + str(i) + ')\n		{\n		    ' + rotations[
                        i] + '(world, rand, x, y, z);\n		}\n\n')
                file_out.write('       return true;\n\n	}\n\n')

            self.progressbar_main.setValue(self.progressbar_main.value() + 4)

            # generates the code witch checks fore valid spawn locations
            for rotations in rotations:

                if rotations_count == 1:
                    file_out.write('	public boolean generate(World world, Random rand, int x, int y, int z)\n'
                                   '	{\n		if')
                else:
                    file_out.write('	public boolean {}(World world, Random rand, int x, int y, int z)\n'
                                   '	{{\n		if'.format(rotations))

                if rotations == 'generate_r0' or rotations == 'generate_r2':

                    if self.combobox_check_points.currentText() == 'Corners':
                        file_out.write('(!LocationIsValidSpawn(world, x, y, z) ||' +
                                       ' !LocationIsValidSpawn(world, x + ' + str(self.width - 1) + ', y, z) ||' +
                                       ' !LocationIsValidSpawn(world, x + ' + str(self.width - 1) + ', y, z + ' +
                                       str(self.length - 1) + ') || !LocationIsValidSpawn(world, x, y, z + ' +
                                       str(self.length - 1) + '))\n		{\n			return false;\n		}\n\n')
                    elif self.combobox_check_points.currentText() == 'Center':
                        file_out.write('(!LocationIsValidSpawn(world, x + ' +
                                       str(self.width // 2) + ', y, z + ' + str(self.length // 2) +
                                       '))\n		{\n			return false;\n		}\n\n')
                    else:
                        file_out.write('		(\n')
                        for blocks in range(0, self.width * self.length):

                            if x == self.width - 1:
                                z += 1
                                x = -1
                            if blocks != 0:
                                x += 1
                            else:
                                x = 0
                                z = 0

                            if blocks == ((self.width * self.length) - 1):
                                file_out.write(
                                    '		    !LocationIsValidSpawn(world, x + ' + str(x) + ', y, z +' + str(
                                        z) + ')\n       )\n\n')
                            else:
                                file_out.write(
                                    '		    !LocationIsValidSpawn(world, x + ' + str(x) + ', y, z +' + str(
                                        z) + ') ||\n')

                if rotations == 'generate_r1' or rotations == 'generate_r3':

                    if self.combobox_check_points.currentText() == 'Corners':
                        file_out.write('(!LocationIsValidSpawn(world, x, y, z) ||' +
                                       ' !LocationIsValidSpawn(world, x + ' + str(self.length - 1) + ', y, z) ||' +
                                       ' !LocationIsValidSpawn(world, x + ' + str(self.length - 1) + ', y, z + ' +
                                       str(self.width - 1) + ') || !LocationIsValidSpawn(world, x, y, z + ' +
                                       str(self.width - 1) + '))\n		{\n			return false;\n		}\n\n')
                    elif self.combobox_check_points.currentText() == 'Center':
                        file_out.write('(!LocationIsValidSpawn(world, x + ' + str(self.length // 2) +
                                       ', y, z + ' + str(self.width // 2) + '))\n' +
                                       '		{\n			return false;\n		}\n\n')
                    else:
                        file_out.write('		(\n')
                        for blocks in range(0, self.width * self.length):

                            if z == 0:
                                x += 1
                                z = self.width
                            if blocks != 0:
                                z -= 1
                            else:
                                x = 0
                                z = self.width - 1

                            if blocks == ((self.width * self.length) - 1):
                                file_out.write(
                                    '		    !LocationIsValidSpawn(world, x + ' + str(x) + ', y, z +' + str(
                                        z) + ')\n	    )\n\n')
                            else:
                                file_out.write(
                                    '		    !LocationIsValidSpawn(world, x + ' + str(x) + ', y, z +' + str(
                                        z) + ') ||\n')

                if rotations_count == 1:
                    rotations = 'generate'

                for i in range(0, size):

                    if rotations == 'generate_r0':
                        if x == self.width - 1:
                            if z == self.length - 1:
                                y += 1
                                z = 0
                            else:
                                z += 1
                            x = -1
                        if i != 0:
                            x += 1
                        else:
                            x = 0
                            y = 0
                            z = 0

                    if rotations == 'generate_r1':

                        if z == 0:
                            if x == self.length - 1:
                                y += 1
                                x = 0
                            else:
                                x += 1
                            z = self.width
                        if i != 0:
                            z -= 1
                        else:
                            x = 0
                            y = 0
                            z = self.width - 1

                    if rotations == 'generate_r2':

                        if x == 0:
                            if z == 0:
                                y += 1
                                z = self.length - 1
                            else:
                                z -= 1
                            x = self.width
                        if i != 0:
                            x -= 1
                        else:
                            x = self.width - 1
                            y = 0
                            z = self.length - 1

                    if rotations == 'generate_r3':

                        if z == self.width - 1:
                            if x == 0:
                                y += 1
                                x = self.length - 1
                            else:
                                x -= 1
                            z = -1
                        if i != 0:
                            z += 1
                        else:
                            x = self.length - 1
                            y = 0
                            z = 0

                    # rotates blocks via metadata if necessary
                    if block_list[i] in blocks_to_rotate:
                        meta_data_rotated = rotate_meta_data(rotations, block_name[block_id.index(block_list[i])],
                                                             meta_data_list[i])

                    # skips air blocks if enabled and prevents the block from being counted
                    if block_list[i] == 0 and do_not_generate_air is True:
                        g -= 1

                    # handels modded blocks also will handel blocks added to Minecraft I didn't know about
                    elif block_list[i] not in block_id:

                        if block_list[i] in custom_blocks_id:
                            custom_block = custom_blocks[custom_blocks_id.index(block_list[i])]
                        elif block_list[i] in custom_blocks_id_cbs:
                            custom_block = custom_blocks_cbs[custom_blocks_id_cbs.index(block_list[i])]
                            if additional_packages_cbs[custom_blocks_id_cbs.index(
                                    block_list[i])] not in additional_packages:
                                additional_packages.append(
                                    additional_packages_cbs[custom_blocks_id_cbs.index(block_list[i])])
                        else:
                            dialog = dialog_custom_Block(self, x, y, z, block_list[i])
                            dialog.exec_()
                            custom_block = dialog.input_name
                            custom_blocks_id.append(block_list[i])
                            custom_blocks.append(custom_block)
                            new_custom_block = True
                            package = dialog.input_package
                            if package not in additional_packages:
                                additional_packages.append(package)

                        file_out.write('		world.setBlock(x + ' + str(x) + ', y + ' +
                                       str(y + int(self.spinbox_offset.text())) + ', z + ' +
                                       str(z) + ', ' + custom_block + ', ' + str(meta_data_list[i]) +
                                       ', ' + '3' + ');\n')

                    # adds blocks witch can pop of the wall to the end of a list witch is written to the file later
                    elif str(block_name[block_id.index(block_list[i])]) in non_solid_blocks:
                        if meta_data_rotated is not None:
                            blocks_placed_last.append('		world.setBlock(x + ' + str(x) + ', y + ' +
                                                      str(y + int(self.spinbox_offset.text())) +
                                                      ', z + ' + str(z) + ', Blocks.' +
                                                      str(block_name[block_id.index(block_list[i])]) +
                                                      ', ' + str(meta_data_rotated) + ', ' + '3' + ');\n')
                            meta_data_rotated = None
                        else:
                            blocks_placed_last.append('		world.setBlock(x + ' + str(x) + ', y + ' +
                                                      str(y + int(self.spinbox_offset.text())) +
                                                      ', z + ' + str(z) + ', Blocks.' +
                                                      str(block_name[block_id.index(block_list[i])]) +
                                                      ', ' + str(meta_data_list[i]) + ', ' + '3' + ');\n')

                    # generates setBlock command for normal blocks
                    else:
                        if meta_data_rotated is not None:
                            file_out.write('		world.setBlock(x + ' + str(x) +
                                           ', y + ' + str(y + int(self.spinbox_offset.text())) +
                                           ', z + ' + str(z) + ', Blocks.' +
                                           str(block_name[block_id.index(block_list[i])]) +
                                           ', ' + str(meta_data_rotated) + ', 3);\n')
                            meta_data_rotated = None
                        else:
                            file_out.write('		world.setBlock(x + ' + str(x) +
                                           ', y + ' + str(y + int(self.spinbox_offset.text())) +
                                           ', z + ' + str(z) + ', Blocks.' +
                                           str(block_name[block_id.index(block_list[i])]) +
                                           ', ' + str(meta_data_list[i]) + ', 3);\n')

                    # counts to 1500 and splits the method after that so the methods can't exceed the byte limit in Java
                    g += 1
                    if g + (c - 1) * 1500 == self.option.get('max_file_length'):
                        g = 0
                        c = 0
                        file_counter += 1
                        file_name = self.option.get('file_name_format').replace(
                            'Filename', os.path.basename(arg_file_out.rstrip('.java'))).replace(
                            '000', (3 - len(str(file_counter))) * '0' + str(file_counter))
                        file_out.write('\n		new ' + file_name + '().' + rotations + str(c) +
                                       '(world, rand, x, y, z);\n		return true;\n\n	}\n}')
                        file_out.close()
                        file_out = open(os.path.dirname(arg_file_out) + '//' + file_name + '.java', 'w')
                        file_header = ('//Schematic to java Structure by jajo_11 | inspired by "MITHION\'S'
                                       '.SCHEMATIC TO JAVA CONVERTINGTOOL"\n\npackage {};\n\nimport '
                                       'java.util.Random;\n\nimport net.minecraft.block.Block;\nimport'
                                       ' net.minecraft.init.Blocks;\nimport net.minecraft.world.World;'
                                       '\n\npublic class {}\n{{\n	public boolean {}'
                                       '(World world, Random rand, int x, int y, int z)\n    {{\n')
                        file_out.write(file_header.format(self.combobox_Package.currentText(), file_name,
                                                          rotations + str(c)))
                    if g == 1500:
                        c += 1
                        file_out.write('\n		' + rotations + str(c) + '(world, rand, x, y, z);\n' +
                                       '		return true;\n\n	}\n' +
                                       '	public boolean ' + rotations + str(c) +
                                       '(World world, Random rand, int x, int y, int z)\n' +
                                       '	{\n\n')
                        g = 0

                    # writes all the blocks witch could pop of the wall
                    if i == size - 1 and blocks_placed_last != []:
                        c += 1
                        g = 0
                        file_out.write('\n		' + rotations + str(c) + '_last' + '(world, rand, x, y, z);\n' +
                                       '		return true;\n\n	}\n' +
                                       '	public boolean ' + rotations + str(c) + '_last' +
                                       '(World world, Random rand, int x, int y, int z)\n' +
                                       '	{\n\n')
                        for j in blocks_placed_last:
                            g += 1
                            if g % 1500 == 0:
                                file_out.write(
                                    '\n		' + rotations + str(c) + '_last' + '(world, rand, x, y, z);\n' +
                                    '		return true;\n\n	}\n' +
                                    '	public boolean ' + rotations + str(c) + '_last' +
                                    '(World world, Random rand, int x, int y, int z)\n' +
                                    '	{\n\n')
                            file_out.write(j)
                        blocks_placed_last.clear()

                    if size < 80:
                        self.progressbar_main.setValue(self.progressbar_main.value() + 80 // size)
                        if i == size - 1:
                            self.progressbar_main.setValue(self.progressbar_main.value() + 80 % size)
                    else:
                        if i % (size // 80) == 0 and i != 0:
                            self.progressbar_main.setValue(self.progressbar_main.value() + 1)

                file_out.write('		return true;\n\n	}\n')

            file_out.write('\n}')

            # writes additional imports for custom blocks
            if additional_packages:

                # reading in file to rewrite it
                file_out.close()
                file_out = open(arg_file_out, 'r')
                file_out_rew = file_out.readlines()
                file_out.close()

                file_out = open(arg_file_out, 'w')
                index_imports = file_out_rew.index('import net.minecraft.world.gen.feature.WorldGenerator;\n')
                i = 0  # just for counting lines
                for Import in additional_packages:
                    i += 1
                    file_out_rew.insert(index_imports + i, 'import ' + Import + ';\n')
                file_out_rew.insert(index_imports + len(additional_packages), '\n')
                file_out.seek(0)
                file_out.writelines(file_out_rew)
            debug_print('Done! ;)')
            self.progressbar_main.setFormat('Done (%p%) ' + self.number_of_files)
            self.progressbar_main.setValue(self.progressbar_main.value() + 5)
            current_packages = self.option.get('package')
            current_package = self.combobox_Package.currentText()
            if current_package not in current_packages:
                current_packages.append(current_package)
                self.option.set('package', current_packages)
            if new_custom_block is True:
                dialog = dialog_custom_Block_save(self, custom_blocks, custom_blocks_id, additional_packages)
                dialog.exec_()
        else:

            debug_print("This isn't a schematic! Exiting...")
            self.noschematic()
        file_in.close()
        file_out.close()

    def noschematic(self):
        QtGui.QMessageBox.warning(self, self.tr('Error'),
                                  self.tr('The selected File dose not appear to be a Schematic! \n We are Sorry :('))

    def read_tag_name(self, tag_type, tag_container):
        if tag_container == 0:
            name_length = int.from_bytes(file_in.read(2), 'big')
            name = bytes.decode(file_in.read(name_length), 'utf-8', 'strict')
            debug_print(tag_type + ' | Name: ' + name + '| Value:', True)
            return name
        else:
            debug_print(tag_type + ' | Value:', True)
            return None

    def done(self):
        debug_print("Done with everything! ;)")
        QtGui.QMessageBox.information(self, self.tr('Done'), self.tr('Operation Completed'))
        self.progressbar_main.setVisible(False)
        self.button_Start.setVisible(True)


def debug_print(string, args=False):
    if DEBUGGING:
        if args:
            print(string, end=' ')
        else:
            print(string)


def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
