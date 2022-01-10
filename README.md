# final-project-ZSSR-2.0


# Similarity configurations: 

--base_dir : 4 directories are included in the base directory: "original","downscaled","zssr result","DIP results"

# experiment configurations:

 --tiff_name : 3D image path
 
# ZSSR configurations: 

--X4 : Estimate the X4 kernel

--SR : Perform ZSSR using the estimated kernel

# Data

The Allen Cell Collection (below) now has 52 high quality-certified fluorescently tagged hiPSC lines that target 41 key cellular structures and substructures available to help your research program.

The Allen Cell Collection is available to academic researchers and commercial entities! New lines continue to be released several times a year, so stay tuned and see below for cell lines in progress.

# ZSSR

https://www.wisdom.weizmann.ac.il/~vision/zssr/

This current provided version of ZSSR actually achieves better results on benchmarks than indicated in the paper.
For example, when current version is applied to 'Set14' without use of gradual SR increments, it achieves slightly higher PSNR than specified in the paper (when 6 gradual increments are applied). When gradual increments similar to those specified in the paper are applied, then +0.3dB is obtained.

![image](https://user-images.githubusercontent.com/63256057/148786869-d933d925-1c0c-4323-a9b7-58e008503145.png)

# DPI

Deep convolutional networks have become a popular tool for image generation and restoration. Generally, their excellent performance is imputed to their ability to learn realistic image priors from a large number of example images. In this paper, we show that, on the contrary, the structure of a generator network is sufficient to capture a great deal of low-level image statistics prior to any learning. In order to do so, we show that a randomly-initialized neural network can be used as a handcrafted prior with excellent results in standard inverse problems such as denoising, super-resolution, and inpainting. Furthermore, the same prior can be used to invert deep neural representations to diagnose them, and to restore images based on flash-no flash input pairs.

Apart from its diverse applications, our approach highlights the inductive bias captured by standard generator network architectures. It also bridges the gap between two very popular families of image restoration methods: learning-based methods using deep convolutional networks and learning-free methods based on handcrafted image priors such as self-similarity.

![image](https://user-images.githubusercontent.com/63256057/148786934-24aa1385-1075-4ac0-8d10-e11cf171448a.png)


https://dmitryulyanov.github.io/deep_image_prior



