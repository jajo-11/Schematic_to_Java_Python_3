#!/usr/bin/python

import gzip
import sys

from MainWindow import *


class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        self.generate_on = []
        self.options = False
        self.cbs_file = None
        self.height = 0
        self.width = 0
        self.length = 0

        QtGui.QMainWindow.__init__(self, *args)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        components(self)
        layout(self)
        tooltipsinit(self)
        preinit(self)
        self.createConnects()
        self.setWindowTitle(self.tr('Schematic to Structure Converter'))

    # noinspection PyCallByClass
    def convertchecker(self):
        if self.lineedit_File_in_Path.text() == '':
            QtGui.QMessageBox.warning(self, self.tr('Error'), self.tr('No File Selected!'))
        elif self.lineedit_File_in_Path.text() == self.lineedit_File_out_Path.text():
            QtGui.QMessageBox.warning(self, self.tr('Error'), self.tr('In and Output are identical'))
        elif self.lineedit_File_out_Path.text() == '':
            file_out_name = self.lineedit_File_in_Path.text().rstrip('schematic') + 'java'
            self.lineedit_File_out_Path.setText(file_out_name)
            if not self.generate_on:
                QtGui.QMessageBox.warning(self, self.tr('Error'), self.tr('No blocks to generate on set!'))
            self.convert()
        elif not self.generate_on:
            QtGui.QMessageBox.warning(self, self.tr('Error'), self.tr('No blocks to generate on set!'))
        elif self.lineedit_File_in_Path.text() != '':
            self.convert()
        else:
            QtGui.QMessageBox.warning(self, self.tr('Error'),
                                      self.tr('Unexpected Error!\nPlease Contact the Devoloper (jajo_11)'))

    # noinspection PyCallByClass
    def filedialogin(self):
        file = QtGui.QFileDialog.getOpenFileName(self, u"Open File", QtGui.QDesktopServices.storageLocation(
            QtGui.QDesktopServices.DesktopLocation), 'Schematics (*.schematic)')
        if file[0] != '':
            self.lineedit_File_in_Path.setText(file[0])
            if self.lineedit_File_out_Path.text() == '':
                file2 = file[0]
                file2 = file2.rstrip('schematic') + 'java'
                self.lineedit_File_out_Path.setText(file2)

    def activate_checkbox_1(self):
        if self.checkbox_rotation_2.isChecked() or self.checkbox_rotation_3.isChecked() or self.checkbox_rotation_4.isChecked():
            self.checkbox_rotation_1.setDisabled(False)
        else:
            self.checkbox_rotation_1.setDisabled(True)
            self.checkbox_rotation_1.setChecked(True)

    def filedialogout(self):
        file = QtGui.QFileDialog.getSaveFileName(self, u"Save File", QtGui.QDesktopServices.storageLocation(
            QtGui.QDesktopServices.DesktopLocation), 'Java (*.java)')
        if file[0] != '':
            self.lineedit_File_out_Path.setText(file[0])

    def createConnects(self):
        self.button_File_in.clicked.connect(self.filedialogin)
        self.button_File_out.clicked.connect(self.filedialogout)
        self.button_add_block.clicked.connect(self.add_to_list)
        self.button_remove_block.clicked.connect(self.remove_from_list)
        self.button_Start.clicked.connect(self.convertchecker)
        self.button_manage_cbs.clicked.connect(self.open_manage_cbs)
        self.checkbox_rotation_1.stateChanged.connect(self.activate_checkbox_1)
        self.checkbox_rotation_2.stateChanged.connect(self.activate_checkbox_1)
        self.checkbox_rotation_3.stateChanged.connect(self.activate_checkbox_1)
        self.checkbox_rotation_4.stateChanged.connect(self.activate_checkbox_1)
        self.lineedit_File_out_Path.editingFinished.connect(self.enable_options)

    def done(self):
        QtGui.QMessageBox.information(self, self.tr('Done'), self.tr('Operation Completed'))

    def noschematic(self):
        QtGui.QMessageBox.warning(self, self.tr('Error'),
                                  self.tr('The selected File dose not appear to be a Schematic! \n We are Sorry :('))

    def add_to_list(self):
        if self.combobox_Generate_on.currentText() not in self.generate_on:
            self.list_Generate_on.addItem(self.combobox_Generate_on.currentText())
            self.generate_on.append(self.combobox_Generate_on.currentText())

    def remove_from_list(self):
        if self.list_Generate_on.currentItem() is not None:
            self.generate_on.remove(self.list_Generate_on.currentItem().text())
        self.list_Generate_on.takeItem(self.list_Generate_on.currentRow())

    def enable_options(self):
        if self.lineedit_File_out_Path.text() == 'options':
            print('Options enabled')
            self.options = True
            self.lineedit_File_out_Path.setText('')

    def open_manage_cbs(self):
        dialog = dialog_custom_Block_manage(self)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.cbs_file = dialog.selected

    def Tag_Number(self, number_size):
        skip = int.from_bytes(file_in.read(2), 'big')
        string = bytes.decode(file_in.read(skip), 'utf-8', 'strict')
        number = int.from_bytes(file_in.read(number_size), 'big')
        # print(string + ' = ' + str(number))
        if string == 'Height':
            self.height = number
        if string == 'Length':
            self.length = number
        if string == 'Width':
            self.width = number

    def convert(self):
        list_size = [0]  # length of lists, sorted in order of creation, entry will be removed when list
        # is finished
        list_Tagid = [0]  # tag id of lists, sorted in order of creation, entry will be removed when list
        # is finished
        list_depth = 0  # determines how many lists are stacked on to each other currently
        tag_depth = 0  # determines how many tags are stacked on to each other currently
        list_in_tag_Compound = [False]  # contains entrys for each list in a tag compound
        litC_depth = 0  # [list in tag Compound depth] determines how many lists in a tag compound are
        # stacked on to each other currently
        block_list = bytearray()
        meta_data_list = bytearray()
        self.height = 0
        self.length = 0
        self.width = 0
        x = 0
        y = 0
        z = 0
        size = 0  # blocks in the struckture
        block_id = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
                    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
                    77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                    101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
                    121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140,
                    141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160,
                    162, 163, 164, 165, 166, 167, 170, 171, 172, 173, 174,
                    175]  # all the ids currently used in the game
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
                      'double_plant']  # list of blocks ids are stored in list block_id with the same index number
        non_solid_blocks = ['torch', 'ladder', 'wall_sign', 'lever', 'unlit_redstone_torch', 'redstone_torch',
                            'stone_button']  # list of blocks wich could pop of the wall
        blocks_placed_last = []  # a list of blocks wich are placed after all the other blocks to prevent them from poping of the walls
        chest = False
        g = 0  # counts up to 1500 to split the methode
        c = 1  # counts the total number of "setblock" methodes
        rotations = []  # list contains checked rotations
        rotationscount = 0  # counts the total items in rotations[]
        custom_block = ''  # name of the custom block (modded) handled last
        custom_blocks = []  # contains all the custom block names assigned
        custom_blocks_id = []  # All the custom ids. Index matching names in custom_blocks list
        new_custom_block = False  # is set to True if there was an unknown custom block in the schematic, to ask afterwards for saving the custom block name
        additional_packages = []  # list stores all the additional imports for custom blocks
        package = ''  # stores last custom blocks package import
        File_out_rew = []  # If there are packages for custom blocks that have to be loaded the file has to be read in edited and written again this list will contain all the lines of File out
        index_imports = 0  # index of the last import line (import net.minecraft.world.gen.feature.WorldGenerator;\n)
        additional_packages_cbs = [] # all from the cbs loaded packages in this additional list to prevent unnecessary imports
        custom_blocks_id_cbs = [] # all from the cbs loaded ids in this additional list to prevent unnecessary imports
        custom_blocks_cbs = [] # all from the cbs loaded names in this additional list to prevent unnecessary imports

        if self.cbs_file is not None:
            if self.cbs_file[0] == True:
                file = open(os.path.dirname(os.path.realpath(__file__)) + '/customblocksets/' + self.cbs_file[1], 'rb')
            else:
                file = open(self.cbs_file[1])
            custom_blocks_cbs = pickle.load(file)
            custom_blocks_id_cbs = pickle.load(file)
            additional_packages_cbs = pickle.load(file)
            file.close()

        global file_in
        file_in = gzip.open(self.lineedit_File_in_Path.text(), 'rb')
        file_out = open(self.lineedit_File_out_Path.text(), 'w')
        do_not_generate_air = self.checkbox_Generate_Air.isChecked()

        if file_in.read(12) == bytearray.fromhex('0A0009536368656D61746963'):
            # print("It's a schematic!")
            while True:

                tag = list_Tagid[list_depth]

                if tag_depth == 0 and list_depth != 0:
                    if list_size[list_depth] != 0:
                        list_size[list_depth] -= 1
                    else:
                        del list_size[list_depth]
                        del list_Tagid[list_depth]
                        list_depth -= 1
                        # print('list end')
                        tag = file_in.read(1)
                elif tag_depth != 0 and litC_depth != 0:
                    if list_size[list_depth] != 0:
                        list_size[list_depth] -= 1
                    else:
                        del list_size[list_depth]
                        del list_Tagid[list_depth]
                        del list_in_tag_Compound[litC_depth]
                        litC_depth -= 1
                        list_depth -= 1
                        # print('list end')
                        tag = file_in.read(1)
                else:
                    tag = file_in.read(1)

                # TAG_Byte
                if tag == bytearray.fromhex('01'):
                    self.Tag_Number(1)
                # TAG_Short
                if tag == bytearray.fromhex('02'):
                    self.Tag_Number(2)
                # TAG_Int
                if tag == bytearray.fromhex('03'):
                    self.Tag_Number(4)
                # TAG_Long
                if tag == bytearray.fromhex('04'):
                    self.Tag_Number(8)
                # TAG_Float
                if tag == bytearray.fromhex('05'):
                    self.Tag_Number(4)
                # TAG_Double
                if tag == bytearray.fromhex('06'):
                    self.Tag_Number(8)
                # TAG_Byte_Array
                if tag == bytearray.fromhex('07'):
                    skip = int.from_bytes(file_in.read(2), 'big')
                    # print 'skip = ' + str(skip)
                    string = bytes.decode(file_in.read(skip), 'utf-8', 'strict')
                    array_legnth = int.from_bytes(file_in.read(4), 'big')
                    if string == 'Blocks':
                        block_list = bytearray(file_in.read(array_legnth))
                        # print('Blocks')
                    elif string == 'Data':
                        meta_data_list = bytearray(file_in.read(array_legnth))
                        # print('Data')
                    else:
                        byte_aray = file_in.read(array_legnth)
                        # print('byte array: ' + string)
                # TAG_String
                if tag == bytearray.fromhex('08'):
                    skip = int.from_bytes(file_in.read(2), 'big')
                    # print 'skip = ' + str(skip)
                    string = bytes.decode(file_in.read(skip), 'utf-8', 'strict')
                    string_length = int.from_bytes(file_in.read(2), 'big')
                    content = bytes.decode(file_in.read(string_length), 'utf-8', 'strict')
                    # print = (string + ' = ' + content)
                    if 'Chest' in content:
                        Chest = True
                # TAG_List
                if tag == bytearray.fromhex('09'):
                    list_depth += 1
                    skip = int.from_bytes(file_in.read(2), 'big')
                    # print 'skip = ' + str(skip)
                    string = bytes.decode(file_in.read(skip), 'utf-8', 'strict')
                    list_Tagid.insert(list_depth, file_in.read(1))
                    list_size.insert(list_depth, int.from_bytes(file_in.read(4), 'big'))
                    # print('List: ' + string + ' | Tag Id: ' + str(int.from_bytes([list_depth], 'big')))
                    if tag_depth != 0:
                        litC_depth += 1
                        list_in_tag_Compound.insert(litC_depth, True)
                # TAG_Compound
                if tag == bytearray.fromhex('0A'):
                    tag_depth += 1
                    # print('Tag_Compound')
                # TAG_Int_Array
                if tag == bytearray.fromhex('0B'):
                    #print('array')
                    break
                #TAG_End
                if tag == bytearray.fromhex('00'):
                    if tag_depth != 0:
                        tag_depth -= 1
                        #print('Tag_Compound End')
                        if list_Tagid[list_depth] == bytearray.fromhex('0A'):
                            tag = list_Tagid[list_depth]
                    else:
                        #print('End of File')
                        break

            size = self.height * self.length * self.width  # calculate block count

            # print(self.length)
            # print(self.width)
            # print('Writing file')

            file_out.write(
                '//Schematic to java Structure by jajo_11 | inspired by "MITHION\'S .SCHEMATIC TO JAVA CONVERTING TOOL"\n' +
                '\npackage ' + self.combobox_Package.currentText() +
                ';\n\nimport java.util.Random;\n' +
                '\nimport net.minecraft.block.Block;\n' +
                'import net.minecraft.block.material.Material;\n' +
                'import net.minecraft.init.Blocks;\n' +
                'import net.minecraft.world.World;\n' +
                'import net.minecraft.world.gen.feature.WorldGenerator;\n\n' +
                'public class ' + os.path.splitext(os.path.basename(self.lineedit_File_out_Path.text()))[0] +
                ' extends WorldGenerator\n' +
                '{\n	protected Block[] GetValidSpawnBlocks()\n' +
                '	{\n		return new Block[]\n' +
                '		{\n')

            for block in self.generate_on:
                file_out.write('			' + block + ',\n')

            if self.checkbox_rotation_1.isChecked():
                rotations.append('generate_r0')
            if self.checkbox_rotation_2.isChecked():
                rotations.append('generate_r1')
            if self.checkbox_rotation_3.isChecked():
                rotations.append('generate_r2')
            if self.checkbox_rotation_4.isChecked():
                rotations.append('generate_r3')
            for i in rotations:
                rotationscount += 1

            file_out.write \
                (
                    '		};\n	}\n\n' + \
                    '	public boolean LocationIsValidSpawn(World world, int x, int y, int z)\n' + \
                    '	{\n		int distanceToAir = 0;\n' + \
                    '		Block checkBlock = world.getBlock(x, y, z);\n\n' + \
                    '		while (checkBlock != Blocks.air)\n		{\n' + \
                    '			distanceToAir++;\n' + \
                    '			checkBlock = world.getBlock(x, y + distanceToAir, z);\n		}\n\n' + \
                    '		if (distanceToAir > 1)\n		{\n			return false;\n		}\n\n' + \
                    '		y += distanceToAir - 1;\n\n' + \
                    '		Block block = world.getBlock(x, y, z);\n' + \
                    '		Block blockAbove = world.getBlock(x, y + 1, z);\n' + \
                    '		Block blockBelow = world.getBlock(x, y - 1, z);\n\n' + \
                    '		for (Block i : GetValidSpawnBlocks())\n		{\n' + \
                    '			if (blockAbove != Blocks.air)\n			{\n' + \
                    '				return false;\n			}\n' + \
                    '			if (block == i)\n			{\n				return true;\n			}\n' + \
                    '			else if (block == Blocks.snow_layer && blockBelow == i)\n' + \
                    '			{\n				return true;\n			}\n' + \
                    '			else if (block.getMaterial() == Material.plants && blockBelow == i)\n' + \
                    '			{\n				return true;\n			}\n		}\n' + \
                    '		return false;\n	}\n\n' + \
                    '	public boolean generate(World world, Random rand, int x, int y, int z)\n' + \
                    '	{\n		' + \
                    'int i = rand.nextInt(' + str(rotationscount) + ');\n\n' \
                    )

            # generates code for random decision of the rotation
            for i in range(0, rotationscount):
                file_out.write('		if(i == ' + str(i) + ')\n		{\n		    ' + rotations[
                    i] + '(world, rand, x, y, z);\n		}\n\n')
            file_out.write('       return true;\n\n	}\n\n')

            # checks for advanced options
            if self.options == True:

                # same as obove only that this one is alredy called with a certain rotation disabeld by default
                file_out.write(
                    '	public boolean generate(World world, Random rand, int x, int y, int z, int i)\n	{\n\n')
                for i in range(0, rotationscount):
                    file_out.write('		if(i == ' + str(i) + ')\n		{\n		    ' + rotations[
                        i] + '(world, rand, x, y, z);\n		}\n\n')
                file_out.write('       return true;\n\n	}\n\n')

                # creates funcion for geting the count of rotations disabeld by default
                file_out.write(
                    '	public int getrotations()\n	{\n\n		return ' + str(rotationscount) + ';\n\n    }\n\n')

            # generates the code witch checks fore valid spawn locations
            for rotations in rotations:

                if rotations == 'generate_r0' or rotations == 'generate_r2':

                    if self.combobox_check_points.currentText() == 'Corners':
                        file_out.write \
                            (
                                '	public boolean ' + rotations + '(World world, Random rand, int x, int y, int z)\n' + \
                                '	{\n		' + \
                                'if(!LocationIsValidSpawn(world, x, y, z) ||' + \
                                ' !LocationIsValidSpawn(world, x + ' + str(self.width - 1) + ', y, z) ||' + \
                                ' !LocationIsValidSpawn(world, x + ' + str(self.width - 1) + ', y, z + ' + str(
                                    self.length - 1) + ') ||' + \
                                ' !LocationIsValidSpawn(world, x, y, z + ' + str(self.length - 1) + '))\n' + \
                                '		{\n			return false;\n		}\n\n'
                            )
                    elif self.combobox_check_points.currentText() == 'Center':
                        file_out.write \
                            (
                                '	public boolean ' + rotations + '(World world, Random rand, int x, int y, int z)\n' + \
                                '	{\n		' + \
                                'if(!LocationIsValidSpawn(world, x + ' + str(self.width // 2) + ', y, z + ' + str(
                                    self.length // 2) + '))\n' + \
                                '		{\n			return false;\n		}\n\n' \
                                )
                    else:
                        file_out.write \
                            (
                                '	public boolean ' + rotations + '(World world, Random rand, int x, int y, int z)\n' + \
                                '	{\n		' + \
                                'if(!LocationIsValidSpawn\n		(\n' \
                                )
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
                                        z) + ')\n	    	)\n\n')
                            else:
                                file_out.write(
                                    '		    !LocationIsValidSpawn(world, x + ' + str(x) + ', y, z +' + str(
                                        z) + ' ||\n')

                if rotations == 'generate_r1' or rotations == 'generate_r3':

                    if self.combobox_check_points.currentText() == 'Corners':
                        file_out.write \
                            (
                                '	public boolean ' + rotations + '(World world, Random rand, int x, int y, int z)\n' + \
                                '	{\n		' + \
                                'if(!LocationIsValidSpawn(world, x, y, z) ||' + \
                                ' !LocationIsValidSpawn(world, x + ' + str(self.length - 1) + ', y, z) ||' + \
                                ' !LocationIsValidSpawn(world, x + ' + str(self.length - 1) + ', y, z + ' + str(
                                    self.width - 1) + ') ||' + \
                                ' !LocationIsValidSpawn(world, x, y, z + ' + str(self.width - 1) + '))\n' + \
                                '		{\n			return false;\n		}\n\n'
                            )
                    elif self.combobox_check_points.currentText() == 'Center':
                        file_out.write \
                            (
                                '	public boolean ' + rotations + '(World world, Random rand, int x, int y, int z)\n' + \
                                '	{\n		' + \
                                'if(!LocationIsValidSpawn(world, x + ' + str(self.length // 2) + ', y, z + ' + str(
                                    self.width // 2) + '))\n' + \
                                '		{\n			return false;\n		}\n\n' \
                                )
                    else:
                        file_out.write \
                            (
                                '	public boolean ' + rotations + '(World world, Random rand, int x, int y, int z)\n' + \
                                '	{\n		' + \
                                'if(!LocationIsValidSpawn\n		(\n' \
                                )
                        for blocks in range(0, self.width * self.length):

                            if z == 0:
                                x += 1
                                z = z = self.width
                            if blocks != 0:
                                z -= 1
                            else:
                                x = 0
                                z = self.width - 1

                            if blocks == ((self.width * self.length) - 1):
                                file_out.write(
                                    '		    !LocationIsValidSpawn(world, x + ' + str(x) + ', y, z +' + str(
                                        z) + ')\n	    	)\n\n')
                            else:
                                file_out.write(
                                    '		    !LocationIsValidSpawn(world, x + ' + str(x) + ', y, z +' + str(
                                        z) + ' ||\n')

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

                    if block_list[i] == 0 and do_not_generate_air == True:
                        g -= 1
                    elif block_list[i] not in block_id:

                        if block_list[i] in custom_blocks_id:
                            custom_block = custom_blocks[custom_blocks_id.index(block_list[i])]
                        elif block_list[i] in custom_blocks_id_cbs:
                            custom_block = custom_blocks_cbs[custom_blocks_id_cbs.index(block_list[i])]
                            if additional_packages_cbs[custom_blocks_id_cbs.index(block_list[i])] not in additional_packages:
                                additional_packages.append(additional_packages_cbs[custom_blocks_id_cbs.index(block_list[i])])
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

                        file_out.write('		world.setBlock(x + ' + str(x) + ', y + ' + str(
                            y + int(self.spinbox_offset.text())) + ', z + ' + str(z) + ', ' + custom_block + ', ' + str(
                            meta_data_list[i]) + ', ' + '3' + ');\n')
                    elif str(block_name[block_id.index(block_list[i])]) in non_solid_blocks:
                        blocks_placed_last.append('		world.setBlock(x + ' + str(x) + ', y + ' + str(
                            y + int(self.spinbox_offset.text())) + ', z + ' + str(z) + ', Blocks.' + str(
                            block_name[block_id.index(block_list[i])]) + ', ' + str(
                            meta_data_list[i]) + ', ' + '3' + ');\n')
                    else:
                        file_out.write('		world.setBlock(x + ' + str(x) + ', y + ' + str(
                            y + int(self.spinbox_offset.text())) + ', z + ' + str(z) + ', Blocks.' + str(
                            block_name[block_id.index(block_list[i])]) + ', ' + str(
                            meta_data_list[i]) + ', ' + '3' + ');\n')

                    g += 1
                    if g == 1500:
                        c += 1
                        file_out.write('\n		' + rotations + str(c) + '(world, rand, x, y, z);\n' + \
                                       '		return true;\n\n	}\n' + \
                                       '	public boolean ' + rotations + str(c) + \
                                       '(World world, Random rand, int x, int y, int z)\n' + \
                                       '	{\n\n')
                        g = 0
                    if i == size - 1:
                        for j in blocks_placed_last:
                            file_out.write(j)
                        blocks_placed_last.clear()

                file_out.write('		return true;\n\n	}\n')

            file_out.write('\n}')

            # writes additional imports for custom blocks
            if additional_packages:

                # reading in file to rewrite it
                file_out.close()
                file_out = open(self.lineedit_File_out_Path.text(), 'r')
                File_out_rew = file_out.readlines()
                file_out.close()

                file_out = open(self.lineedit_File_out_Path.text(), 'w')
                index_imports = File_out_rew.index('import net.minecraft.world.gen.feature.WorldGenerator;\n')
                i = 0  # just for counting lines
                for Import in additional_packages:
                    i += 1
                    File_out_rew.insert(index_imports + i, 'import ' + Import + ';\n')
                File_out_rew.insert(index_imports + len(additional_packages), '\n')
                file_out.seek(0)
                file_out.writelines(File_out_rew)

            # print('Done! ;)')
            self.done()
            save_package(self)
            if new_custom_block == True:
                dialog = dialog_custom_Block_save(self, custom_blocks, custom_blocks_id, additional_packages)
                dialog.exec_()
        else:

            # print("This isn't a schematic! Exiting...")
            self.noschematic()
        file_in.close()
        file_out.close()


def main(argv):
    app = QtGui.QApplication(argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
