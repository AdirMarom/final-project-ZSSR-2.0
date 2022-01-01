import os
import sys
import datetime
import numpy as np

#current_python_path = "C:\\Users\\benro\\PycharmProjects\\aics-segmentation"
#
#sys.path.insert(0,current_python_path)

# package for 3d visualization
from itkwidgets import view
from aicssegmentation.core.visual import seg_fluo_side_by_side,  single_fluorescent_view, segmentation_quick_view
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [16, 12]

# package for io
from aicsimageio import AICSImage
from aicsimageio.writers import OmeTiffWriter

BASE_DIR = "C:\\Users\\adirm\\Desktop\\cell_Image\\AICS-12-part10\\AICS-12\\"

fov_path = os.path.join(BASE_DIR,'AICS-12_871.ome.tif')
if not os.path.exists(fov_path):
    print("boo no file")

reader = AICSImage(fov_path)
img = reader.data

#0-original
#1 down

img = np.squeeze(img)
img = np.squeeze(img)
#removing dummy dimensions

N_CHANNELS = img.shape[0]
MID_SLICE = np.int64(0.5 * img.shape[1])

# fig size * dpi cannot be more than 2^16 = 65536
# original was 2040px_1356px_220dpi

fig, ax = plt.subplots(1, N_CHANNELS, figsize=(2040 / 60, 1356 / 80), dpi=220, facecolor='w', edgecolor='k') # fig size is in inches

# ax[5].axis('off')
# ax[5].imshow(img[5,MID_SLICE,:,:], cmap=plt.cm.gray)
lst_matrix = []
count=0
if N_CHANNELS > 1:
    for channel in range(N_CHANNELS):
        count+=1
        if count>4:
            break
        if channel>4:
            break
        ax[channel].axis('off')
        print(ax[channel])
        pic = ax[channel].imshow(img[channel, MID_SLICE, :, :], cmap='viridis')

        # Save the subplot.
        bbox = ax[channel].get_tightbbox(fig.canvas.get_renderer())
        fig.savefig("3d_slice\\subplot{}.jpeg".format(channel), bbox_inches=bbox.transformed(fig.dpi_scale_trans.inverted()))

        # imsave(x, "{}.png".format(channel))
        pic_matrix = pic.get_array()
        lst_matrix.append(pic_matrix)
        # print(lst_matrix)
        print(type(pic_matrix))
        print(pic_matrix.shape)
else:
    ax.axis('off')
    ax.imshow(img[0, MID_SLICE, :, :], cmap=plt.cm.gray)
    print("down")

# only 4 channels have infomration in them (brightfield/and 3 fluorescent chaannels )

#####################
structure_channel = 3
#####################

struct_img0 = img[structure_channel,:,:]
view(single_fluorescent_view(struct_img0))
#switch to z-plane


#####################
brightfield_channel = 6
#####################

bright_img0 = img[brightfield_channel,:,:]
view(single_fluorescent_view(bright_img0))
#switch to z-plane

