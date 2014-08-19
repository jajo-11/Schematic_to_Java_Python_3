__author__ = 'Joschka'

import gzip
import PySide
import sys

DEBUGGING = False


def debug_print(string, args=False):
    if DEBUGGING:
        if args:
            print(string, end=' ')
        else:
            print(string)

def read_tag_name_alt(self, tag_type, tag_container):
    if tag_container == 0:
        name_length = int.from_bytes(schematic.read(2), 'big')
        name = bytes.decode(schematic.read(name_length), 'utf-8', 'strict')
        debug_print(tag_type + ' | Name: ' + name + '| Value:', True)
        return name
    else:
        debug_print(tag_type + ' | Value:', True)
        return None

def convert_alt(self, file_in, file_out, file_2_out):

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

        # first the tag id of the items in the list and than the list size or a zero for tag compounds
        tag_container = [[0, 0]]

        # array with all the blocks and corresponding meta data
        block_list = bytearray()
        meta_data_list = bytearray()

        # height, length and width of the structure saved as a short in the schematic (2 bytes long)
        self.height = 0
        self.length = 0
        self.width = 0

        # will contain block name in the order of the 'id' in the outputted file
        # for example in the file there is a 4 the fifth item in legend[] is the name of the block
        legend = []

        #array with all the blocks but with new id
        block_list_2 = bytearray()

        global schematic
        schematic = gzip.open(file_in, 'rb')


        if file_in.read(12) == bytearray.fromhex('0A0009536368656D61746963'):
            debug_print("It's a schematic!")
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
                    elif name == 'Length':
                        self.length = number
                    elif name == 'Width':
                        self.width = number
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
                    elif name == 'Data':
                        meta_data_list = bytearray(file_in.read(array_length))
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
                    PySide.QtGui.QMessageBox.information(self, self.tr('Error'),
                                                         self.tr('Well that went unexpectedly...\n' +
                                                                 'Unknown tag type: ' + str(
                        int.from_bytes(tag, 'big'))))
                    sys.exit(int.from_bytes(tag, 'big'))

        for byte in block_list:
            if block_list[block_id.index(int.from_bytes(byte))] in legend:
                block_list_2.append(str(bytearray.legend.index(block_list[block_id.index(int.from_bytes(byte))]))
                                    .encode('ascii'))


        block_file = open(file_2_out, 'wb')
        block_file.write(block_list_2)
