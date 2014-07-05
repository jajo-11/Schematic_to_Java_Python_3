def rotate_meta_data(rotation, block, meta_data):
    if block in ['torch', 'unlit_redstone_torch', 'redstone_torch'] and meta_data in range(0, 5):
        if rotation == 'generate_r1':
            meta_data_list = [0, 4, 3, 1, 2]
            meta_data = meta_data_list[meta_data]
        elif rotation == 'generate_r2':
            meta_data_list = [0, 2, 1, 4, 3]
            meta_data = meta_data_list[meta_data]
        elif rotation == 'generate_r3':
            meta_data_list = [0, 3, 4, 2, 1]
            meta_data = meta_data_list[meta_data]

    elif block == 'log' or block == 'log2':
        if rotation == 'generate_r1' or rotation == 'generate_r3':
            meta_data_list = [0, 1, 2, 3, 8, 9, 10, 11, 4, 5, 6, 7, 12, 13, 14, 15]
            meta_data = meta_data_list[meta_data]

    elif block in ['oak_stairs', 'stone_stairs', 'brick_stairs', 'stone_brick_stairs', 'nether_brick_stairs',
                 'sandstone_stairs', 'spruce_stairs', 'birch_stairs', 'jungle_stairs', 'quartz_stairs', 'acacia_stairs',
                 'dark_oak_stairs'] and meta_data in range(0, 8):
        if rotation == 'generate_r1':
            meta_data_list = [3, 2, 0, 1, 7, 6, 4, 5]
            meta_data = meta_data_list[meta_data]
        elif rotation == 'generate_r2':
            meta_data_list = [1, 0, 3, 2, 5, 4, 7, 6]
            meta_data = meta_data_list[meta_data]
        elif rotation == 'generate_r3':
            meta_data_list = [2, 3, 1, 0, 6, 7, 5, 4]
            meta_data = meta_data_list[meta_data]
    elif block in ['piston', 'sticky_piston']:
        if rotation == 'generate_r1':
            meta_data_list = [0, 1, 4, 5, 3, 2, 6, 7, 8, 9, 12, 13, 11, 10, 14, 15]
            meta_data = meta_data_list[meta_data]
        if rotation == 'generate_r2':
            meta_data_list = [0, 1, 3, 2, 5, 4, 6, 7, 8, 9, 11, 10, 13, 12, 14, 15]
            meta_data = meta_data_list[meta_data]
        if rotation == 'generate_r3':
            meta_data_list = [0, 1, 5, 4, 2, 3, 6, 7, 8, 9, 13, 12, 10, 11, 14, 15]
            meta_data = meta_data_list[meta_data]
    return meta_data
