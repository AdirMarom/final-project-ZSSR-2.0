import xlwt
from xlwt import Workbook
from math import log10, sqrt
from skimage.metrics import structural_similarity
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--base_dir",action = "store",required=True, type=str)
args = parser.parse_args()

base_dir = args.base_dir


original_path = str(base_dir)+"original/"
downgrade_path= str(base_dir)+"downscaled/"
ZSSR_output_path = str(base_dir)+"zssr_result/"
DIP_output_path = str(base_dir)+"DIP_results/"
file_name = "similarity_result "


def PSNR(original, compressed):
    original = cv2.imread(original)
    compressed = cv2.imread(compressed)
    d = (original.shape[1], original.shape[0])
    compressed = cv2.resize(compressed, d)

    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def DICE(img, img2):
    img = cv2.imread(img)
    img2 = cv2.imread(img2)
    d = (img.shape[1], img.shape[0])
    img2 = cv2.resize(img2, d)
    if img.shape != img2.shape:
        raise ValueError("Shape mismatch: img and img2 must have to be of the same shape.")
    else:
        lenIntersection = 0
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if (np.array_equal(img[i][j], img2[i][j])):
                    lenIntersection += 1
#
        lenimg = img.shape[0] * img.shape[1]
        lenimg2 = img2.shape[0] * img2.shape[1]
        value = (2. * lenIntersection / (lenimg + lenimg2))
    return value

def SSIM(imageA,imageB):


    imageA = cv2.imread(imageA)
    #imageB = cv2.imread(imageB)

    d=(imageA.shape[1],imageA.shape[0])
    #imageB=cv2.resize(imageB,d)
    im = Image.open(imageB)
    if(d[0]!=im.size[0] and d[0]!=im.size[0]):
        im = im.resize(d, Image.ANTIALIAS)
        im.save(imageB)

    imageB = cv2.imread(imageB)

    # 4. Convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    # 6. You can print only the score if you want
    return score

def generate_ZSSR_result(wb,original_path, downgrade_path, ZSSR_output_path, file_name):
    original_files = [f for f in listdir(original_path) if isfile(join(original_path, f))]
    ZSSR_files = [f for f in listdir(ZSSR_output_path) if isfile(join(ZSSR_output_path, f))]
    downgrade_files = [f for f in listdir(downgrade_path) if isfile(join(downgrade_path, f))]
    SSIM_ZSSR_result=[]
    DICE_ZSSR_result=[]
    PSNR_ZSSR_result=[]
    SSIM_downgrade_result=[]
    DICE_downgrade_result=[]
    PSNR_downgrade_result=[]
    for i in range(len(ZSSR_files)):
        original_full_path= original_path + original_files[i]
        zssr_full_path = ZSSR_output_path + ZSSR_files[i]
        downgrade_full_path= downgrade_path + downgrade_files[i]
        #ZSSR and original
        SSIM_ZSSR_result.append(SSIM(original_full_path, zssr_full_path))
        DICE_ZSSR_result.append(DICE(original_full_path, zssr_full_path))
        PSNR_ZSSR_result.append(PSNR(original_full_path, zssr_full_path))
        #downgrade and original
        SSIM_downgrade_result.append(SSIM(original_full_path, downgrade_full_path))
        DICE_downgrade_result.append(DICE(original_full_path, downgrade_full_path))
        PSNR_downgrade_result.append(PSNR(original_full_path, downgrade_full_path))


    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('ZSSR')

    sheet1.write(0, 1, 'ZSSR- SSIM')
    sheet1.write(0, 2, 'Downgrade- SSIM')
    sheet1.write(0, 3, 'ZSSR- PSNR')
    sheet1.write(0, 4, 'Downgrade- PSNR')
    sheet1.write(0, 5, 'ZSSR -DICE')
    sheet1.write(0, 6, 'Downgrade -DICE')

    for i in range(1,11):
        sheet1.write(i, 0, 'Image {}'.format(i))

    for i in range(len(SSIM_ZSSR_result)):
        sheet1.write(i+1,1,SSIM_ZSSR_result[i])
        sheet1.write(i+1,2,SSIM_downgrade_result[i])
        sheet1.write(i+1,3,PSNR_ZSSR_result[i])
        sheet1.write(i+1,4,PSNR_downgrade_result[i])
        sheet1.write(i+1,5,DICE_downgrade_result[i])
        sheet1.write(i+1,6,DICE_ZSSR_result[i])



def generate_DIP_result(wb,original_path, downgrade_path, ZSSR_output_path, file_name):
    original_files = [f for f in listdir(original_path) if isfile(join(original_path, f))]
    ZSSR_files = [f for f in listdir(ZSSR_output_path) if isfile(join(ZSSR_output_path, f))]
    downgrade_files = [f for f in listdir(downgrade_path) if isfile(join(downgrade_path, f))]
    SSIM_ZSSR_result=[]
    DICE_ZSSR_result=[]
    PSNR_ZSSR_result=[]
    SSIM_downgrade_result=[]
    DICE_downgrade_result=[]
    PSNR_downgrade_result=[]
    for i in range(len(ZSSR_files)):
        original_full_path= original_path + original_files[i]
        zssr_full_path = ZSSR_output_path + ZSSR_files[i]
        downgrade_full_path= downgrade_path + downgrade_files[i]
        #ZSSR and original
        SSIM_ZSSR_result.append(SSIM(original_full_path, zssr_full_path))
        DICE_ZSSR_result.append(DICE(original_full_path, zssr_full_path))
        PSNR_ZSSR_result.append(PSNR(original_full_path, zssr_full_path))
        #downgrade and original
        SSIM_downgrade_result.append(SSIM(original_full_path, downgrade_full_path))
        DICE_downgrade_result.append(DICE(original_full_path, downgrade_full_path))
        PSNR_downgrade_result.append(PSNR(original_full_path, downgrade_full_path))

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('DIP')

    sheet1.write(0, 1, 'DIP- SSIM')
    sheet1.write(0, 2, 'Downgrade- SSIM')
    sheet1.write(0, 3, 'DIP- PSNR')
    sheet1.write(0, 4, 'Downgrade- PSNR')
    sheet1.write(0, 5, 'DIP -DICE')
    sheet1.write(0, 6, 'Downgrade -DICE')

    for i in range(1,11):
        sheet1.write(i, 0, 'Image {}'.format(i))

    for i in range(len(SSIM_ZSSR_result)):
        sheet1.write(i+1,1,SSIM_ZSSR_result[i])
        sheet1.write(i+1,2,SSIM_downgrade_result[i])
        sheet1.write(i+1,3,PSNR_ZSSR_result[i])
        sheet1.write(i+1,4,PSNR_downgrade_result[i])
        sheet1.write(i+1,5,DICE_downgrade_result[i])
        sheet1.write(i+1,6,DICE_ZSSR_result[i])

    wb.save(file_name+'.xls')




# Workbook is created
wb = Workbook()
print("Created WorkBook! ")
generate_ZSSR_result(wb,original_path,downgrade_path,ZSSR_output_path,file_name)
generate_DIP_result(wb,original_path,downgrade_path,DIP_output_path,file_name)
print("Finished Running all! ")
