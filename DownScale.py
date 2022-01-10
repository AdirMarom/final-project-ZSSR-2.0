
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def pil_to_np(img_PIL):
    '''Converts image in PIL format to np.array.

    From W x H x C [0...255] to C x W x H [0..1]
    '''
    ar = np.array(img_PIL)

    if len(ar.shape) == 3:
        ar = ar.transpose(2, 0, 1)
    else:
        ar = ar[None, ...]

    return ar.astype(np.float32) / 255.


def load(path):
    """Load PIL image."""
    img = Image.open(path)
    return img


def get_image(path, imsize=-1):
    """Load an image and resize to a cpecific size.

    Args:
        path: path to image
        imsize: tuple or scalar with dimensions; -1 for `no resize`
    """
    img = load(path)

def load_LR_HR_imgs_sr(fname, imsize, factor, enforse_div32=None):
    '''Loads an image, resizes it, center crops and downscales.

    Args:
        fname: path to the image
        imsize: new size for the image, -1 for no resizing
        factor: downscaling factor
        enforse_div32: if 'CROP' center crops an image, so that its dimensions are divisible by 32.
    '''
    img_orig_pil, img_orig_np = get_image(fname, -1)

    if imsize != -1:
        img_orig_pil, img_orig_np = get_image(fname, imsize)

    # For comparison with GT
    if enforse_div32 == 'CROP':
        new_size = (img_orig_pil.size[0] - img_orig_pil.size[0] % 32,
                    img_orig_pil.size[1] - img_orig_pil.size[1] % 32)

        bbox = [
            (img_orig_pil.size[0] - new_size[0]) / 2,
            (img_orig_pil.size[1] - new_size[1]) / 2,
            (img_orig_pil.size[0] + new_size[0]) / 2,
            (img_orig_pil.size[1] + new_size[1]) / 2,
        ]

        img_HR_pil = img_orig_pil.crop(bbox)
        img_HR_np = pil_to_np(img_HR_pil)
    else:
        img_HR_pil, img_HR_np = img_orig_pil, img_orig_np

    LR_size = [
        img_HR_pil.size[0] // factor,
        img_HR_pil.size[1] // factor
    ]

    img_LR_pil = img_HR_pil.resize(LR_size, Image.ANTIALIAS)
    img_LR_np = pil_to_np(img_LR_pil)

    print('HR and LR resolutions: %s, %s' % (str(img_HR_pil.size), str(img_LR_pil.size)))

    return {
        'orig_pil': img_orig_pil,
        'orig_np': img_orig_np,
        'LR_pil': img_LR_pil,
        'LR_np': img_LR_np,
        'HR_pil': img_HR_pil,
        'HR_np': img_HR_np
    }


def get_baselines(img_LR_pil, img_HR_pil):
    '''Gets `bicubic`, sharpened bicubic and `nearest` baselines.'''
    img_bicubic_pil = img_LR_pil.resize(img_HR_pil.size, Image.BICUBIC)
    img_bicubic_np = pil_to_np(img_bicubic_pil)

    img_nearest_pil = img_LR_pil.resize(img_HR_pil.size, Image.NEAREST)
    img_nearest_np = pil_to_np(img_nearest_pil)

    img_bic_sharp_pil = img_bicubic_pil.filter(PIL.ImageFilter.UnsharpMask())
    img_bic_sharp_np = pil_to_np(img_bic_sharp_pil)

    return img_bicubic_np, img_bic_sharp_np, img_nearest_np


def downgrade(path_img, path_to_save):
    imsize = -1
    path_to_image = path_img
    factor = 4
    enforse_div32 = 'CROP'

    imgs = load_LR_HR_imgs_sr(path_to_image, imsize, factor, enforse_div32)
    imgs['bicubic_np'], imgs['sharp_np'], imgs['nearest_np'] = get_baselines(imgs['LR_pil'], imgs['HR_pil'])
    # use only downgraded images
    tmp = imgs['bicubic_np']
    tmp = tmp.swapaxes(0, 1)
    tmp = tmp.swapaxes(1, 2)
    print("In down grade function the path to save downgraded images is: " + str(path_to_save))
    plt.imsave(path_to_save, tmp)




if __name__ == "__main__":
    path_to_image = "/home/dor2/KernalGan-Master/tiff_images/AICS-11_336.ome.tif"
    path_to_save = "/home/dor2/KernalGan-Master/tiff_images/downscaled"
    downgrade(path_to_image, path_to_save)