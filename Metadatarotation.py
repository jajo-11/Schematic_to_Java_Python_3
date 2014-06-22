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
    if block == 'log':
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
