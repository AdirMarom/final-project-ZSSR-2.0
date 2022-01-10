import os
import sys
import datetime
from os import listdir
import torch
import cv2
import torchvision
from aicsimageio import AICSImage
from aicsimageio.writers import OmeTiffWriter
from pathlib import Path
from csbdeep.data import RawData, create_patches
from csbdeep.data.transform import anisotropic_distortions
from PIL import Image as im
import numpy as np
import logging
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import io
from new_utils import load_LR_HR_imgs_sr, get_baselines
from PIL import Image
import argparse
from datetime import datetime

from matplotlib._cm_listed import cmaps


def get_image_grid(images_np, nrow=8):
    '''Creates a grid from a list of images by concatenating them.'''
    images_torch = [torch.from_numpy(x) for x in images_np]
    torch_grid = torchvision.utils.make_grid(images_torch, nrow)
    return torch_grid.numpy()


def plot_image_grid(images_np, nrow=8, factor=1, interpolation='lanczos'):
    """Draws images in a grid

    Args:
        images_np: list of images, each image is np.array of size 3xHxW of 1xHxW
        nrow: how many images will be in one row
        factor: size if the plt.figure
        interpolation: interpolation used in plt.imshow
    """

    n_channels = max(x.shape[0] for x in images_np)
    # assert (n_channels == 3) or (n_channels == 1), "images should have 1 or 3 channels"

    images_np = [x if (x.shape[0] == n_channels) else np.concatenate([x, x, x], axis=0) for x in images_np]

    count = 0
    #    for image in images_np:
    # print(image)
    # plt.imshow(image, interpolation=interpolation)
    # plt.savefig("/home/dor2/results/{0}.png".format(count))
    # count += 1

    grid = get_image_grid(images_np, nrow)

    plt.figure(figsize=(len(images_np) + factor, 12 + factor))

    if images_np[0].shape[0] == 1:
        plt.imshow(grid[0], cmap='gray', interpolation=interpolation)
    else:
        plt.imshow(grid.transpose(1, 2, 0), interpolation=interpolation)

    plt.show()

    return grid


current_python_path = "aics-segmentation"
sys.path.insert(0, current_python_path)
# package for 3d visualization
from itkwidgets import view
from aicssegmentation.core.visual import seg_fluo_side_by_side, single_fluorescent_view, segmentation_quick_view
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [16, 12]
# package for io

BASE_DIR = "/home/dor2/KernalGan-Master/tiff_images"


# tiff_file_name = "AICS-11_335.ome.tif"


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
    date = date.replace("/", "-")
    time = time.replace(":", "-")
    # tmp_path = "/home/dor2/KernalGan-Master/tiff_images/slicer_output/" + str(date)+ "_" + str(time)+ "_" + str(tiff_file_name).split(".")[0]
    # tmp_path_downgrade = "/home/dor2/KernalGan-Master/tiff_images/slicer_output_downgraded/" + str(date)+ "_" + str(time)+ "_" + str(tiff_file_name).split(".")[0]

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
    completeName = os.path.join(pic_dir_downgrade_path, name_of_file)

    if N_CHANNELS > 1:
        for channel in range(N_CHANNELS):
            if channel != 2:
                continue
            ax[channel].axis('off')
            print(ax[channel])
            pic = ax[channel].imshow(img[channel, MID_SLICE, :, :], cmap='turbo')

            # Save the subplot.
            bbox = ax[channel].get_tightbbox(fig.canvas.get_renderer())
            full_image_path = tmp_path + "/{0}.png".format(str(tiff_file_name).split(".")[0])
            fig.savefig(full_image_path, bbox_inches=bbox.transformed(fig.dpi_scale_trans.inverted()))

            # check if subplot is relevnt and not trash
            image_path = tmp_path + "\subplot{}.png".format(channel)
            image = plt.imread(image_path)
            tmp_mean = image.mean()

            pic_matrix = pic.get_array()
            lst_matrix.append(pic_matrix)

            def downgrade(channel, path):
                imsize = -1
                path_to_image = path
                factor = 4
                enforse_div32 = 'CROP'

                imgs = load_LR_HR_imgs_sr(path_to_image, imsize, factor, enforse_div32)
                imgs['bicubic_np'], imgs['sharp_np'], imgs['nearest_np'] = get_baselines(imgs['LR_pil'], imgs['HR_pil'])
                # use only downgraded images
                tmp = imgs['bicubic_np']
                tmp = tmp.swapaxes(0, 1)
                tmp = tmp.swapaxes(1, 2)
                print("In down grade function the path to save downgraded images is: " + str(completeName))
                plt.imsave(completeName, tmp)
                print("\n")
                print("Succesfully downgraded {} Image and Saved! ".format(name_of_file))
                print("\n")
                return completeName

            path_to_image = tmp_path + "/{0}.png".format(str(tiff_file_name).split(".")[0])
            if 0.5 > tmp_mean or 0.7 < tmp_mean:
                os.remove(tmp_path + "\subplot{}.png".format(channel))
            else:
                new_path = downgrade(channel, path_to_image)
                downgrade(channel, new_path)

    else:
        ax.axis('off')
        ax.imshow(img[0, MID_SLICE, :, :], cmap=plt.cm.gray)
        print("down")
    print("successfully slicing, the images inside 'slicer_output' folder")
    return full_image_path, pic_dir_downgrade_path

    # only 4 channels have infomration in them (brightfield/and 3 fluorescent chaannels )


def zssr(zssr_path, output_dir):
    try:
        os.system(
            "python /home/dor2/KernalGan-Master/train.py --input-dir {0} --output-dir {1} --X4 --SR --real".format(
                zssr_path, output_dir))
        print("input dir to ZSSR is" + str(zssr_path))

    except OSError as e:
        print("Error Running ZSSR! \n")
        print(e)


def deep_image_prior(dip_path):
    print("path to dip is: {}".format(dip_path))
    try:
        os.system('python KernalGan-Master/pythonProject/main.py --image_path {}'.format(dip_path))
    except OSError as e:
        print(e)


# run slicer and downgrading algorithms

if __name__ == "__main__":
    prog = argparse.ArgumentParser()
    prog.add_argument('--tiff_name', '-i', type=str, default='', help='the name of the tiff file')
    args = prog.parse_args()
    tiff_file_name = args.tiff_name
    output_dir = "/home/dor2/KernalGan-Master/tiff_images/zssr_result"
    # abs_src = os.path.abspath(args.src)

    dip_path, zssr_path = load_and_slice(tiff_file_name)
    print("starting Slicing...")
    print("starting ZSSR...")
    zssr(zssr_path, output_dir)
    print("finished ZSSR! \n")
    print("started dip")

    deep_image_prior(dip_path)
    print("Finished Running both algorithms")

