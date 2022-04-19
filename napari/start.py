from skimage import data
import napari

viewer = napari.view_image(data.cells3d(), channel_axis=1, ndisplay=3)
napari.run()  # start the "event loop" and show the viewer
# conda create -y -n napari-env -c conda-forge python=3.9
# conda activate napari-env
# python -m pip install "napari[all]"
#
