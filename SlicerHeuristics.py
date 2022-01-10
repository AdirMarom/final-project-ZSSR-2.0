import os
import sys
import datetime
from pathlib import Path
import logging
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from aicsimageio import AICSImage

BASE_DIR = "/home/dor2/KernalGan-Master/tiff_images"

def load_and_slice(tiff_file_name):
    logging.info('trying to get tiff folder...')
    fov_path = os.path.join(BASE_DIR, tiff_file_name)
    if not os.path.exists(fov_path):
        print(fov_path)
        print("boo no file")
        print(tiff_file_name)

    print("tiff file found...")
    print("start slicing...")
    reader = AICSImage(fov_path)
    img = reader.data
    print(img.shape)
    img = np.squeeze(img)
    img = np.squeeze(img)
    # removing dummy dimensions
    print(img.shape)
    N_CHANNELS = img.shape[0]
    MID_SLICE = np.int(0.5 * img.shape[1])
    fig, ax = plt.subplots(1, N_CHANNELS, figsize=(2040 / 30, 1356 / 40), dpi=150, facecolor='w', edgecolor='k')

    # ax[5].axis('off')
    # ax[5].imshow(img[5,MID_SLICE,:,:], cmap=plt.cm.gray)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    splitted_dt = dt_string.split(' ')
    date, time = splitted_dt[0], splitted_dt[1]

    tmp_path = "/home/dor2/KernalGan-Master/tiff_images/original"
    tmp_path_downgrade = "/home/dor2/KernalGan-Master/tiff_images/downscaled"
    Path(tmp_path).mkdir(parents=True, exist_ok=True)
    Path(tmp_path_downgrade).mkdir(parents=True, exist_ok=True)

    pic_dir_downgrade_path = tmp_path_downgrade + "/" + tiff_file_name
    Path(pic_dir_downgrade_path).mkdir(parents=True, exist_ok=True)

    print("deep image prior directory is:" + str(tmp_path))
    print("zssr directory is:" + str(tmp_path_downgrade))
    full_image_path = None
    lst_matrix = []

    name_of_file = "{0}.png".format(str(tiff_file_name).split(".")[0])


    if N_CHANNELS > 1:
        for channel in range(N_CHANNELS):
            # check if subplot is relevnt and not trash
            image_path = tmp_path + "\subplot{}.png".format(channel)
            image = plt.imread(image_path)
            tmp = image.mean()
            if tmp < 0.5 or tmp > 0.7:
                continue
            ax[channel].axis('off')
            print(ax[channel])
            pic = ax[channel].imshow(img[channel, MID_SLICE, :, :], cmap='turbo')

            # Save the subplot.
            bbox = ax[channel].get_tightbbox(fig.canvas.get_renderer())
            full_image_path = tmp_path + "/{0}.png".format(str(tiff_file_name).split(".")[0])

            fig.savefig(full_image_path, bbox_inches=bbox.transformed(fig.dpi_scale_trans.inverted()))

            pic_matrix = pic.get_array()
            lst_matrix.append(pic_matrix)

    else:
            ax.axis('off')
            ax.imshow(img[0, MID_SLICE, :, :], cmap=plt.cm.gray)
            print("down")
    print("successfully slicing, the images inside 'slicer_output' folder")
    return full_image_path, pic_dir_downgrade_path
    # only 4 channels have infomration in them (brightfield/and 3 fluorescent chaannels )


load_and_slice("AICS-11_336.ome.tif")
