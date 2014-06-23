def rotate_meta_data(rotation, block, meta_data):
    if block == 'torch' or block == 'unlit_redstone_torch' or block == 'redstone_torch':
        if rotation == 'generate_r1':
            if meta_data == 1:
                meta_data = 4
            elif meta_data == 2:
                meta_data = 3
            elif meta_data == 3:
                meta_data = 1
            elif meta_data == 4:
                meta_data = 2
        elif rotation == 'generate_r2':
            if meta_data == 1:
                meta_data = 2
            elif meta_data == 2:
                meta_data = 1
            elif meta_data == 3:
                meta_data = 4
            elif meta_data == 4:
                meta_data = 3
        elif rotation == 'generate_r3':
            if meta_data == 1:
                meta_data = 3
            elif meta_data == 2:
                meta_data = 4
            elif meta_data == 3:
                meta_data = 2
            elif meta_data == 4:
                meta_data = 1
        return meta_data

    if block == 'log' or block == 'log2':
        if rotation == 'generate_r1' or rotation == 'generate_r3':
            if meta_data == 4:
                meta_data = 8
            elif meta_data == 5:
                meta_data = 9
            elif meta_data == 6:
                meta_data = 10
            elif meta_data == 7:
                meta_data = 11
            elif meta_data == 8:
                meta_data = 4
            elif meta_data == 9:
                meta_data = 5
            elif meta_data == 10:
                meta_data = 6
            elif meta_data == 11:
                meta_data = 7
            return meta_data

    if block in ['oak_stairs', 'stone_stairs', 'brick_stairs', 'stone_brick_stairs', 'nether_brick_stairs',
                 'sandstone_stairs', 'spruce_stairs', 'birch_stairs', 'jungle_stairs', 'quartz_stairs', 'acacia_stairs',
                 'dark_oak_stairs']:
        if rotation == 'generate_r1':
            if meta_data == 0:
                meta_data = 3
            elif meta_data == 1:
                meta_data = 2
            elif meta_data == 2:
                meta_data = 0
            elif meta_data == 3:
                meta_data = 1
            elif meta_data == 4:
                meta_data = 7
            elif meta_data == 5:
                meta_data = 6
            elif meta_data == 6:
                meta_data = 4
            elif meta_data == 7:
                meta_data = 5
        elif rotation == 'generate_r2':
            if meta_data == 0:
                meta_data = 1
            elif meta_data == 1:
                meta_data = 0
            elif meta_data == 2:
                meta_data = 3
            elif meta_data == 3:
                meta_data = 2
            elif meta_data == 4:
                meta_data = 5
            elif meta_data == 5:
                meta_data = 4
            elif meta_data == 6:
                meta_data = 7
            elif meta_data == 7:
                meta_data = 6
        elif rotation == 'generate_r3':
            if meta_data == 0:
                meta_data = 2
            elif meta_data == 1:
                meta_data = 3
            elif meta_data == 2:
                meta_data = 1
            elif meta_data == 3:
                meta_data = 0
            elif meta_data == 4:
                meta_data = 6
            elif meta_data == 5:
                meta_data = 7
            elif meta_data == 6:
                meta_data = 5
            elif meta_data == 7:
                meta_data = 4
        return meta_data
