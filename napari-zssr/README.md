# napari-ZSSR-plugin

<br/>
<br/>

A plugin that enables 2D image Zero Shot Super Resolution provided by Ben Gurion University.

The ZSSR plugin for napari provides an intuitive graphical user interface of ZSSR execution for 2D images. with the abilities of napari Viewer you can choose any image in png format and view the images after ZSSR improvement. The selected image will be displayed in the viewer and you can take advantage of all the functionality that napari tool is offering. The advantage of this tool is a convenient and easy-to-use interface for running an ZSSR algorithm so that it will be accessible to everyone, Knowledge of the code is not necessary.


More details about napri tool can be found at: https://github.com/napari/napari

More details about ZSSR algorithm and code can be found at https://www.weizmann.ac.il/math/irani/sites/math.irani/files/uploads/zssr_cameraready.pdf

----------------------------------


## Installation

### Step 1:

install `napari` via [pip]:

    pip install "napari[all]"

### Step 2:

after opened the project install ZSSR plugin via [pip]:

    pip install -e .

### Step 3:

open napari via terminal:
    
    napari

## Quick Start

1. go to [conf] file and change the configuration to suit your running environment.
2. Start the plugin (open napari, go to "Plugins" --> "napari-zssr:zssr plugin")
3. select the zero shot model (currently zssr is the only option).
4. Select the folder where the 2D (png) image is located.
5. Select ZSSR configurations flags, you can find info about flags [here]
6. Click "Run Zero-Shot" Super-Resolution to execute the ZSSR algorithm on the chosen data.


## Contributing

This is a initial version and the plugin and can be extended in other algorithms.
contributors are welcome.

## License

"zssr-napari-plugin" is free and open source software.

<br/>
<br/>

[conf]: https://github.com/AdirMarom/final-project-ZSSR-2.0/blob/napari_zssr/napari-zssr/napari_zssr/zssr/conf.py
[here]: https://github.com/AdirMarom/final-project-ZSSR-2.0/tree/main
[@napari]: https://github.com/napari