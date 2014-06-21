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